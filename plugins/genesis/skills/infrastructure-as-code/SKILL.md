---
name: infrastructure-as-code
description: |
  IaC patterns for Terraform, Pulumi, and Kubernetes.
  Use when: generating infrastructure templates, cloud resources,
  K8s manifests, "create terraform", "generate infra", "pulumi component",
  "kubernetes manifest", module generation, cloud deployment.
  Supports: AWS, GCP, Azure, Kubernetes, multi-cloud.
allowed-tools: Read, Write, Edit, Bash
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Infrastructure as Code Skill

Generate production-ready IaC using Terraform, Pulumi, and Kubernetes patterns.

## Terraform Module Structure

```
terraform/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   └── database/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
```

## Terraform Module Pattern

```hcl
# modules/api-service/variables.tf
variable "name" {
  type        = string
  description = "Service name"
}

variable "environment" {
  type        = string
  description = "Environment (dev, staging, prod)"
}

# modules/api-service/main.tf
resource "aws_ecs_service" "api" {
  name            = "${var.name}-${var.environment}"
  cluster         = var.cluster_id
  desired_count   = var.environment == "prod" ? 3 : 1
}

# modules/api-service/outputs.tf
output "service_name" {
  value = aws_ecs_service.api.name
}
```

## Terraform Environment Usage

```hcl
# environments/dev/main.tf
module "api" {
  source      = "../../modules/api-service"
  name        = "my-api"
  environment = "dev"
  cluster_id  = module.ecs.cluster_id
}
```

## Pulumi Component Pattern

```typescript
// components/api-service.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface ApiServiceArgs {
  name: string;
  environment: string;
  cpu?: number;
  memory?: number;
}

export class ApiService extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(name: string, args: ApiServiceArgs, opts?: pulumi.ComponentResourceOptions) {
    super("genesis:aws:ApiService", name, {}, opts);

    const service = new aws.ecs.Service(`${name}-service`, {
      // ... configuration
    }, { parent: this });

    this.url = pulumi.interpolate`https://${args.name}.example.com`;
    this.registerOutputs({ url: this.url });
  }
}
```

## Kubernetes Manifests

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ project_name }}
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: {{ project_name }}
          image: {{ image }}
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
```

### Service + Ingress
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ project_name }}
spec:
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ project_name }}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [{{ domain }}]
      secretName: {{ project_name }}-tls
```

## Cloud Provider Selection

| Scenario | Tool | Why |
|----------|------|-----|
| Multi-cloud, mature team | Terraform | HCL, large ecosystem |
| TypeScript team | Pulumi | Native language |
| AWS-only | AWS CDK | AWS-native constructs |
| K8s-native | Helm/Kustomize | K8s ecosystem |

## Backend Configuration

### Terraform S3 Backend
```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Pulumi Backend
```yaml
# Pulumi.yaml
name: my-project
runtime: nodejs
backend:
  url: s3://my-pulumi-state
```

## Detailed References

- [Terraform Patterns](references/terraform-patterns.md) - Module design
- [Pulumi Patterns](references/pulumi-patterns.md) - Component authoring
- [Kubernetes Manifests](references/kubernetes-manifests.md) - K8s resources
- [Monorepo Structures](references/monorepo-structures.md) - Multi-project IaC
