---
name: generate-workflows
description: Generate GitHub Actions CI/CD workflows for a project
allowed-tools: Read, Write, Edit, WebSearch
argument-validation: optional
---

# Generate Workflows Command

Generate production-ready GitHub Actions workflows based on project analysis.

## Usage

```
/genesis:generate-workflows [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--target <path>` | Target project path | `.` |
| `--type <types>` | Workflow types (ci,cd,security,release) | ci |
| `--reusable` | Create reusable workflows | false |
| `--matrix` | Include matrix builds | false |

## Workflow Types

### CI (Continuous Integration)
- Linting
- Testing
- Building
- Coverage reporting

### CD (Continuous Deployment)
- Environment deployments (staging, production)
- Docker builds
- Cloud deployments (AWS, GCP, Azure)

### Security
- Dependency auditing
- CodeQL analysis
- Secret scanning
- Container scanning

### Release
- Semantic versioning
- Changelog generation
- Package publishing
- GitHub releases

## Examples

```bash
# Generate basic CI workflow
/genesis:generate-workflows --target ./my-project --type ci

# Generate full CI/CD pipeline
/genesis:generate-workflows --type ci,cd,security --matrix

# Generate reusable workflows
/genesis:generate-workflows --type ci,cd --reusable
```

## Output

Creates in `.github/workflows/`:
- `ci.yml` - CI pipeline
- `cd.yml` - Deployment pipeline
- `security.yml` - Security scanning
- `release.yml` - Release automation

If `--reusable`:
- `reusable-ci.yml`
- `reusable-deploy.yml`

## Injected Skills

- `github-actions` - Workflow patterns and best practices

## Delegates To

- `workflow-builder` agent for workflow generation
