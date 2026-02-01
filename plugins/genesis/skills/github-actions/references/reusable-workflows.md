# Reusable Workflows Reference

Complete guide to GitHub Actions reusable workflows with `workflow_call`.

## Basic Structure

### Defining a Reusable Workflow
```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI Workflow

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version to use'
        required: true
        type: string
      run-e2e:
        description: 'Whether to run E2E tests'
        required: false
        type: boolean
        default: false
      environment:
        description: 'Deployment environment'
        required: false
        type: string
        default: 'development'
    secrets:
      NPM_TOKEN:
        description: 'NPM authentication token'
        required: false
      DATABASE_URL:
        description: 'Database connection string'
        required: true
    outputs:
      artifact-url:
        description: 'URL of uploaded artifact'
        value: ${{ jobs.build.outputs.artifact-url }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact-url: ${{ steps.upload.outputs.artifact-url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
      - run: npm ci
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      - run: npm test
      - if: ${{ inputs.run-e2e }}
        run: npm run test:e2e
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Calling a Reusable Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  call-reusable:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '20'
      run-e2e: true
      environment: production
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Input Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text value | `'20'`, `'production'` |
| `boolean` | True/false | `true`, `false` |
| `number` | Numeric value | `3000`, `60` |

## Secrets Handling

### Inherit All Secrets
```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    secrets: inherit
```

### Explicit Secrets
```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    secrets:
      MY_SECRET: ${{ secrets.MY_SECRET }}
```

## Outputs

### Define Output in Reusable Workflow
```yaml
on:
  workflow_call:
    outputs:
      image-tag:
        description: 'Docker image tag'
        value: ${{ jobs.build.outputs.tag }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.build.outputs.tag }}
    steps:
      - id: build
        run: echo "tag=${{ github.sha }}" >> $GITHUB_OUTPUT
```

### Use Output in Caller
```yaml
jobs:
  build:
    uses: ./.github/workflows/build.yml

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build.outputs.image-tag }}"
```

## Cross-Repository Calls

### Public Repository
```yaml
jobs:
  call-workflow:
    uses: org/repo/.github/workflows/workflow.yml@main
    with:
      input1: 'value'
```

### Private Repository (Same Org)
```yaml
jobs:
  call-workflow:
    uses: my-org/private-repo/.github/workflows/workflow.yml@v1
    secrets: inherit
```

## Nesting Workflows

### Limits (2026)
- Maximum nesting depth: 10 levels
- Maximum workflow calls per run: 50
- Cannot call itself (no recursion)

### Example Nested Structure
```
main.yml
  └── calls ci.yml
        ├── calls test.yml
        └── calls build.yml
              └── calls docker.yml
```

## Best Practices

### 1. Version Pinning
```yaml
# Good - pinned to specific ref
uses: org/repo/.github/workflows/ci.yml@v1.2.0

# Acceptable - pinned to branch
uses: org/repo/.github/workflows/ci.yml@main

# Avoid - no pinning
uses: org/repo/.github/workflows/ci.yml
```

### 2. Input Validation
```yaml
on:
  workflow_call:
    inputs:
      environment:
        type: string
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate environment
        run: |
          if [[ ! "${{ inputs.environment }}" =~ ^(dev|staging|prod)$ ]]; then
            echo "Invalid environment: ${{ inputs.environment }}"
            exit 1
          fi
```

### 3. Conditional Execution
```yaml
jobs:
  test:
    if: ${{ inputs.run-tests }}
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: test
    if: ${{ always() && (needs.test.result == 'success' || needs.test.result == 'skipped') }}
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
```

## Complete Example

### reusable-deploy.yml
```yaml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
      AWS_SECRET_ACCESS_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ inputs.environment }}-cluster \
            --service api-service \
            --force-new-deployment
```
