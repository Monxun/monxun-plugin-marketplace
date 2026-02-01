# Monorepo Structures Reference

Patterns for organizing IaC in monorepo environments.

## Terraform Monorepo

### Directory Structure
```
infrastructure/
├── terraform/
│   ├── modules/                    # Reusable modules
│   │   ├── networking/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── ecs-service/
│   │   ├── rds/
│   │   └── s3/
│   │
│   ├── shared/                     # Shared infrastructure
│   │   ├── vpc/
│   │   │   ├── main.tf
│   │   │   ├── backend.tf
│   │   │   └── outputs.tf
│   │   └── dns/
│   │
│   └── services/                   # Per-service infrastructure
│       ├── api/
│       │   ├── dev/
│       │   │   ├── main.tf
│       │   │   ├── terraform.tfvars
│       │   │   └── backend.tf
│       │   ├── staging/
│       │   └── prod/
│       └── worker/
│
├── kubernetes/                     # K8s manifests
│   ├── base/
│   └── overlays/
│
└── .github/
    └── workflows/
        └── terraform.yml
```

### State Organization
```
# S3 bucket structure for state
s3://terraform-state/
├── shared/
│   ├── vpc/terraform.tfstate
│   └── dns/terraform.tfstate
├── services/
│   ├── api/
│   │   ├── dev/terraform.tfstate
│   │   ├── staging/terraform.tfstate
│   │   └── prod/terraform.tfstate
│   └── worker/
│       ├── dev/terraform.tfstate
│       └── prod/terraform.tfstate
```

### Path-Based CI/CD
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  push:
    paths:
      - 'infrastructure/terraform/**'
  pull_request:
    paths:
      - 'infrastructure/terraform/**'

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.changes.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: changes
        run: |
          # Detect which services changed
          CHANGED=$(git diff --name-only ${{ github.event.before }} ${{ github.sha }} | \
            grep '^infrastructure/terraform/services/' | \
            cut -d/ -f4-5 | sort -u)
          # Create matrix JSON
          MATRIX=$(echo "$CHANGED" | jq -R -s -c 'split("\n") | map(select(length > 0))')
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  terraform:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.matrix != '[]' }}
    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-changes.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        working-directory: infrastructure/terraform/services/${{ matrix.service }}
        run: terraform init

      - name: Terraform Plan
        working-directory: infrastructure/terraform/services/${{ matrix.service }}
        run: terraform plan -out=tfplan

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        working-directory: infrastructure/terraform/services/${{ matrix.service }}
        run: terraform apply -auto-approve tfplan
```

## Pulumi Monorepo

### Directory Structure
```
infrastructure/
├── pulumi/
│   ├── packages/                   # Shared components
│   │   ├── networking/
│   │   │   ├── package.json
│   │   │   ├── index.ts
│   │   │   └── tsconfig.json
│   │   └── database/
│   │
│   ├── shared/                     # Shared infrastructure
│   │   ├── vpc/
│   │   │   ├── Pulumi.yaml
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   └── dns/
│   │
│   └── services/                   # Per-service
│       ├── api/
│       │   ├── Pulumi.yaml
│       │   ├── Pulumi.dev.yaml
│       │   ├── Pulumi.prod.yaml
│       │   ├── index.ts
│       │   └── package.json
│       └── worker/
│
└── pnpm-workspace.yaml
```

### Workspace Configuration
```yaml
# pnpm-workspace.yaml
packages:
  - 'infrastructure/pulumi/packages/*'
  - 'infrastructure/pulumi/shared/*'
  - 'infrastructure/pulumi/services/*'
```

### Shared Package
```typescript
// packages/networking/index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

export interface VpcArgs {
  name: string;
  cidrBlock?: string;
  availabilityZones?: number;
}

export class Vpc extends pulumi.ComponentResource {
  public readonly vpcId: pulumi.Output<string>;
  public readonly publicSubnetIds: pulumi.Output<string>[];
  public readonly privateSubnetIds: pulumi.Output<string>[];

  constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
    super("myorg:networking:Vpc", name, {}, opts);
    // Implementation
  }
}
```

### Service Using Shared
```typescript
// services/api/index.ts
import * as pulumi from "@pulumi/pulumi";
import { Vpc } from "@myorg/networking";
import { Database } from "@myorg/database";

const config = new pulumi.Config();
const stack = pulumi.getStack();

// Reference shared VPC
const vpcRef = new pulumi.StackReference(`myorg/shared-vpc/${stack}`);
const vpcId = vpcRef.getOutput("vpcId");

// Create service resources
// ...
```

## Multi-Environment Strategy

### Environment Promotion
```
Workflow:
1. PR → plan all environments
2. Merge to main → apply to dev
3. Tag release → apply to staging
4. Manual approval → apply to prod
```

### Terragrunt for DRY Config
```
infrastructure/
├── terragrunt.hcl                  # Root config
├── modules/
└── environments/
    ├── terragrunt.hcl              # Common env config
    ├── dev/
    │   ├── terragrunt.hcl
    │   └── api/
    │       └── terragrunt.hcl
    ├── staging/
    └── prod/
```

```hcl
# environments/dev/api/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

include "env" {
  path = "${dirname(find_in_parent_folders())}/environments/terragrunt.hcl"
}

terraform {
  source = "../../../modules/api-service"
}

inputs = {
  environment   = "dev"
  instance_count = 1
}
```

## Best Practices

### 1. Module Versioning
```hcl
module "api" {
  source  = "github.com/myorg/terraform-modules//api-service?ref=v1.2.0"
}
```

### 2. State Isolation
- One state file per service per environment
- Shared infrastructure in separate state
- Use remote state data sources for cross-references

### 3. Change Detection
- Use path filters in CI/CD
- Only plan/apply changed components
- Separate pipelines for shared vs service infrastructure

### 4. Secrets Management
- Use external secret stores (Vault, AWS Secrets Manager)
- Never commit secrets to repo
- Inject at runtime via CI/CD
