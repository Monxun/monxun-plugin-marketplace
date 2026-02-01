---
name: github-actions
description: |
  GitHub Actions workflow patterns and best practices.
  Use when: generating CI/CD workflows, creating reusable workflows,
  composite actions, matrix builds, security scanning pipelines,
  "create workflow", "github actions", "ci cd pipeline".
  Supports: workflow_call, composite actions, YAML anchors.
allowed-tools: Read, Write, Edit
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# GitHub Actions Skill

Generate production-ready CI/CD workflows using GitHub Actions best practices.

## Workflow Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly
  workflow_dispatch:       # Manual trigger
```

## Reusable Workflow Pattern

### Define Reusable Workflow
```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
      run-e2e:
        required: false
        type: boolean
        default: false
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

### Call Reusable Workflow
```yaml
# .github/workflows/ci.yml
jobs:
  ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '20'
      run-e2e: true
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Composite Action Pattern

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Sets up Node.js project with caching'

inputs:
  node-version:
    description: 'Node.js version'
    required: true
    default: '20'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    - run: npm ci
      shell: bash
```

## Matrix Builds

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## Common Patterns

### Caching
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Artifacts
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: coverage
    path: coverage/
    retention-days: 7
```

### Environment Secrets
```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Job Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
  deploy:
    needs: build
    runs-on: ubuntu-latest
```

### Environments
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
```

## Security Scanning

```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript
      - uses: github/codeql-action/analyze@v3
```

## Path Triggers (Monorepo)

```yaml
on:
  push:
    paths:
      - 'packages/api/**'
      - '.github/workflows/api.yml'
```

## Service Containers

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: test
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

## Limits (2026)

- **Nesting depth**: 10 levels
- **Workflow calls per run**: 50
- **Job execution time**: 6 hours
- **Workflow run time**: 35 days

## Detailed References

- [Reusable Workflows](references/reusable-workflows.md) - Full workflow_call patterns
- [Composite Actions](references/composite-actions.md) - Action packaging
- [Matrix Builds](references/matrix-builds.md) - Multi-dimension testing
- [Security Patterns](references/security-patterns.md) - Security scanning
