# Terraform Patterns Reference

Complete guide to Terraform module design and best practices.

## Module Structure

### Standard Module Layout
```
modules/
├── api-service/
│   ├── main.tf           # Resources
│   ├── variables.tf      # Input variables
│   ├── outputs.tf        # Output values
│   ├── versions.tf       # Provider requirements
│   └── README.md         # Documentation
```

### Root Module Layout
```
environments/
├── dev/
│   ├── main.tf           # Module calls
│   ├── variables.tf      # Environment variables
│   ├── terraform.tfvars  # Variable values
│   ├── backend.tf        # State configuration
│   └── providers.tf      # Provider config
├── staging/
└── prod/
```

## Variable Patterns

### Input Variables
```hcl
# Required variable
variable "name" {
  type        = string
  description = "Service name"
}

# Optional with default
variable "instance_count" {
  type        = number
  default     = 1
  description = "Number of instances"
}

# Complex type
variable "tags" {
  type        = map(string)
  default     = {}
  description = "Resource tags"
}

# With validation
variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# Sensitive variable
variable "database_password" {
  type        = string
  sensitive   = true
  description = "Database password"
}
```

### Local Values
```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = merge(var.tags, {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  })

  is_production = var.environment == "prod"
}
```

## Resource Patterns

### Conditional Resources
```hcl
resource "aws_cloudwatch_log_group" "main" {
  count = var.enable_logging ? 1 : 0

  name              = "/aws/ecs/${local.name_prefix}"
  retention_in_days = local.is_production ? 365 : 30
}
```

### Dynamic Blocks
```hcl
resource "aws_security_group" "main" {
  name        = "${local.name_prefix}-sg"
  description = "Security group for ${var.name}"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}
```

### For Each
```hcl
resource "aws_s3_bucket" "buckets" {
  for_each = toset(var.bucket_names)

  bucket = "${local.name_prefix}-${each.key}"
  tags   = local.common_tags
}
```

## Module Patterns

### Module Definition
```hcl
# modules/api-service/main.tf
resource "aws_ecs_task_definition" "main" {
  family                   = var.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name  = var.name
      image = var.image
      portMappings = [
        {
          containerPort = var.port
          protocol      = "tcp"
        }
      ]
      environment = [
        for k, v in var.environment : {
          name  = k
          value = v
        }
      ]
      logConfiguration = var.enable_logging ? {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.main[0].name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = var.name
        }
      } : null
    }
  ])
}

resource "aws_ecs_service" "main" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.main.id]
    assign_public_ip = var.assign_public_ip
  }

  dynamic "load_balancer" {
    for_each = var.target_group_arn != null ? [1] : []
    content {
      target_group_arn = var.target_group_arn
      container_name   = var.name
      container_port   = var.port
    }
  }
}
```

### Module Usage
```hcl
# environments/prod/main.tf
module "api" {
  source = "../../modules/api-service"

  name          = "api"
  image         = "myapp:${var.image_tag}"
  port          = 8080
  cpu           = 512
  memory        = 1024
  desired_count = 3

  cluster_id       = module.ecs_cluster.id
  subnet_ids       = module.vpc.private_subnet_ids
  target_group_arn = module.alb.target_group_arn

  environment = {
    DATABASE_URL = var.database_url
    LOG_LEVEL    = "info"
  }

  enable_logging = true
  tags           = local.common_tags
}
```

## State Management

### S3 Backend
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Data Sources for State
```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "my-terraform-state"
    key    = "shared/vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use: data.terraform_remote_state.vpc.outputs.vpc_id
```

## Outputs

```hcl
output "service_name" {
  value       = aws_ecs_service.main.name
  description = "ECS service name"
}

output "service_url" {
  value       = "https://${var.domain}"
  description = "Service URL"
  sensitive   = false
}

output "task_definition_arn" {
  value       = aws_ecs_task_definition.main.arn
  description = "Task definition ARN"
}
```
