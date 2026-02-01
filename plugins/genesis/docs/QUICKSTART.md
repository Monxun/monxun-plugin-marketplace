# Genesis Quick Start Guide

Get started with Genesis in 5 minutes.

## Installation

Load the Genesis plugin with Claude Code:

```bash
claude --plugin-dir ./plugins/genesis
```

## Basic Usage

### Create a Template from an Exemplar Project

If you have an existing project you want to turn into a reusable template:

```bash
# Analyze and create template from local project
/genesis:create-template --exemplar ./my-awesome-project --name my-template

# Create from a GitHub repository
/genesis:create-template --exemplar https://github.com/user/repo --name my-template
```

### Generate a Project from a Built-in Template

Use one of the included scaffold templates:

```bash
# Create a Node.js API
/genesis:create-template --template nodejs-api --name my-api

# Create a React app with Vite
/genesis:create-template --template react-vite --name my-webapp

# Create a Go microservice
/genesis:create-template --template go-microservice --name my-service
```

### Generate with Custom Variables

Pass variables to customize generation:

```bash
/genesis:create-template --template nodejs-api --name my-api \
  --var port=3000 \
  --var database=postgresql \
  --var use_docker=true
```

## Workflow Generation

Generate CI/CD workflows for your project:

```bash
# Analyze project and generate appropriate workflows
/genesis:generate-workflows --path ./my-project

# Generate specific workflow types
/genesis:generate-workflows --type ci-test,security-scan
```

## Infrastructure Generation

Generate Infrastructure as Code:

```bash
# Generate Terraform for AWS
/genesis:generate-infra --cloud aws --type ecs

# Generate for Kubernetes
/genesis:generate-infra --type kubernetes
```

## Common Workflows

### 1. Create API Template from Example

```bash
# Step 1: Analyze the exemplar
/genesis:analyze-project --path ./reference-api

# Step 2: Research current best practices
/genesis:research-stack --technologies "express,typescript,postgresql"

# Step 3: Create the template
/genesis:create-template --exemplar ./reference-api --name company-api-template

# Step 4: Validate the template
/genesis:validate-template --path ./templates/company-api-template
```

### 2. Bootstrap New Project with CI/CD

```bash
# Step 1: Generate project
/genesis:create-template --template nodejs-api --name my-service

# Step 2: Add CI/CD workflows
/genesis:generate-workflows --path ./my-service

# Step 3: Add infrastructure
/genesis:generate-infra --path ./my-service --cloud aws
```

### 3. Analyze and Improve Existing Project

```bash
# Deep analysis with recommendations
/genesis:analyze-project --path ./my-project --deep

# Generate missing workflows
/genesis:generate-workflows --path ./my-project --fill-gaps

# Validate against best practices
/genesis:validate-template --path ./my-project
```

## Template Variables

When creating templates, Genesis automatically detects and parameterizes:

| Variable Type | Example | Template Syntax |
|--------------|---------|-----------------|
| Project name | `my-api` | `{{ project_name }}` |
| Port numbers | `3000` | `{{ port \| default: 8080 }}` |
| Database | `postgresql` | `{{#if database == 'postgresql'}}` |
| Docker usage | `true/false` | `{{#if use_docker}}` |

## Quality Validation

Run validation before publishing:

```bash
/genesis:validate-template --path ./my-template --strict
```

Quality gates check:
- **Structure** (25%): Correct directory layout
- **Syntax** (25%): Valid JSON/YAML/HCL
- **Completeness** (25%): All required files present
- **Security** (25%): No exposed secrets

Minimum passing score: 80%

## Publishing Templates

Package templates for distribution:

```bash
# Create distributable package
/genesis:publish-template --path ./my-template --output ./dist

# Publish to template registry
/genesis:publish-template --path ./my-template --registry https://templates.example.com
```

## Tips

1. **Start with a clean exemplar**: Remove sensitive data before analysis
2. **Use descriptive variable names**: `database_url` not `db`
3. **Test generated projects**: Run `npm test` or equivalent after generation
4. **Version your templates**: Use semantic versioning in genesis.json
5. **Document variables**: Add descriptions to help users understand options

## Troubleshooting

### Template validation fails

```bash
# Run with verbose output
/genesis:validate-template --path ./my-template --verbose
```

### Variables not interpolating

Ensure GTL syntax is correct:
```
{{ variable }}     ✓ Correct
{{variable}}       ✗ Missing spaces
${ variable }      ✗ Wrong syntax
```

### Missing dependencies

```bash
# Re-analyze to detect all dependencies
/genesis:analyze-project --path ./my-project --include-dev-deps
```

## Next Steps

- Read the [Architecture Guide](./ARCHITECTURE.md) for deep dive
- Explore built-in templates in `templates/project-scaffolds/`
- Check workflow templates in `templates/workflows/`
