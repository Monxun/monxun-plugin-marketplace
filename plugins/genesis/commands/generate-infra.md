---
name: generate-infra
description: Generate Infrastructure as Code (Terraform, Pulumi, Kubernetes)
allowed-tools: Read, Write, Edit, Bash
argument-validation: optional
---

# Generate Infrastructure Command

Generate production-ready Infrastructure as Code based on project requirements.

## Usage

```
/genesis:generate-infra [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target <path>` | Target project path | `.` |
| `--provider <name>` | IaC provider (terraform, pulumi, kubernetes) | terraform |
| `--cloud <name>` | Cloud provider (aws, gcp, azure) | aws |
| `--services <list>` | Services to provision | auto-detect |
| `--environments <list>` | Environments (dev,staging,prod) | dev,prod |

## Supported Providers

### Terraform
- Modular structure (modules/ + environments/)
- S3 backend configuration
- Variable validation
- Output values

### Pulumi
- TypeScript components
- Stack configurations
- Cross-stack references
- Transformations

### Kubernetes
- Deployments, Services, Ingress
- ConfigMaps, Secrets
- HPA, PDB, NetworkPolicy
- Kustomize overlays

## Service Detection

Auto-detects from project:
- **API Service** → ECS/Cloud Run/Kubernetes
- **Database** → RDS/Cloud SQL/PlanetScale
- **Cache** → ElastiCache/Memorystore
- **Storage** → S3/GCS/Azure Blob

## Examples

```bash
# Generate Terraform for AWS
/genesis:generate-infra --provider terraform --cloud aws

# Generate Kubernetes manifests
/genesis:generate-infra --provider kubernetes

# Generate for multiple environments
/genesis:generate-infra --provider terraform \
  --environments dev,staging,prod \
  --services ecs,rds,elasticache
```

## Output

### Terraform
```
terraform/
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── environments/
    ├── dev/
    └── prod/
```

### Pulumi
```
pulumi/
├── index.ts
├── components/
├── Pulumi.yaml
└── Pulumi.dev.yaml
```

### Kubernetes
```
kubernetes/
├── base/
└── overlays/
    ├── dev/
    └── prod/
```

## Injected Skills

- `infrastructure-as-code` - IaC patterns and best practices

## Delegates To

- `infra-architect` agent for infrastructure generation
