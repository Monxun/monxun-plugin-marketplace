# Composite Actions Reference

Complete guide to creating reusable composite actions in GitHub Actions.

## Basic Structure

### action.yml
```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Sets up a Node.js project with caching and dependencies'
author: 'Your Team'

branding:
  icon: 'package'
  color: 'blue'

inputs:
  node-version:
    description: 'Node.js version to use'
    required: true
    default: '20'
  install-command:
    description: 'Command to install dependencies'
    required: false
    default: 'npm ci'
  working-directory:
    description: 'Directory containing package.json'
    required: false
    default: '.'

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
        cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json

    - name: Install dependencies
      working-directory: ${{ inputs.working-directory }}
      run: ${{ inputs.install-command }}
      shell: bash

    - name: Verify installation
      working-directory: ${{ inputs.working-directory }}
      run: echo "Dependencies installed successfully"
      shell: bash
```

## Using Composite Actions

### Local Action
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup project
        uses: ./.github/actions/setup-project
        with:
          node-version: '20'
          install-command: 'npm ci --production=false'
```

### Remote Action
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: my-org/my-repo/.github/actions/setup-project@v1
        with:
          node-version: '20'
```

## Shell Specification

Every `run` step MUST specify a shell:

```yaml
runs:
  using: 'composite'
  steps:
    - run: echo "Using bash"
      shell: bash

    - run: Write-Host "Using PowerShell"
      shell: pwsh

    - run: python script.py
      shell: python
```

### Available Shells
| Shell | Platforms | Usage |
|-------|-----------|-------|
| `bash` | All | Default for Linux/macOS |
| `pwsh` | All | PowerShell Core |
| `python` | All | Python scripts |
| `sh` | Linux/macOS | POSIX shell |
| `cmd` | Windows | Command Prompt |
| `powershell` | Windows | Windows PowerShell |

## Outputs from Composite Actions

### Setting Output in Step
```yaml
runs:
  using: 'composite'
  steps:
    - name: Generate output
      id: generate
      run: |
        VERSION=$(node -p "require('./package.json').version")
        echo "version=$VERSION" >> $GITHUB_OUTPUT
      shell: bash

outputs:
  version:
    description: 'Package version'
    value: ${{ steps.generate.outputs.version }}
```

### Using in Workflow
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get version
        id: version
        uses: ./.github/actions/get-version

      - run: echo "Version is ${{ steps.version.outputs.version }}"
```

## Conditional Steps

```yaml
runs:
  using: 'composite'
  steps:
    - name: Install production deps
      if: ${{ inputs.production == 'true' }}
      run: npm ci --production
      shell: bash

    - name: Install all deps
      if: ${{ inputs.production != 'true' }}
      run: npm ci
      shell: bash
```

## Using Other Actions

Composite actions can use other actions:

```yaml
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}

    - uses: actions/cache@v4
      with:
        path: ~/.npm
        key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

    - run: npm ci
      shell: bash
```

## Common Patterns

### Docker Build Action
```yaml
# .github/actions/docker-build/action.yml
name: 'Docker Build'
description: 'Build and optionally push Docker image'

inputs:
  image-name:
    required: true
  tag:
    required: false
    default: 'latest'
  push:
    required: false
    default: 'false'
  context:
    required: false
    default: '.'

outputs:
  image:
    value: ${{ steps.build.outputs.image }}

runs:
  using: 'composite'
  steps:
    - uses: docker/setup-buildx-action@v3

    - name: Build image
      id: build
      run: |
        IMAGE="${{ inputs.image-name }}:${{ inputs.tag }}"
        docker build -t $IMAGE ${{ inputs.context }}
        echo "image=$IMAGE" >> $GITHUB_OUTPUT
      shell: bash

    - name: Push image
      if: ${{ inputs.push == 'true' }}
      run: docker push ${{ inputs.image-name }}:${{ inputs.tag }}
      shell: bash
```

### Test Runner Action
```yaml
# .github/actions/run-tests/action.yml
name: 'Run Tests'
description: 'Run tests with coverage'

inputs:
  test-command:
    required: false
    default: 'npm test'
  coverage-threshold:
    required: false
    default: '80'

outputs:
  coverage:
    value: ${{ steps.coverage.outputs.percentage }}

runs:
  using: 'composite'
  steps:
    - name: Run tests
      run: ${{ inputs.test-command }} -- --coverage
      shell: bash

    - name: Check coverage
      id: coverage
      run: |
        COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
        echo "percentage=$COVERAGE" >> $GITHUB_OUTPUT
        if (( $(echo "$COVERAGE < ${{ inputs.coverage-threshold }}" | bc -l) )); then
          echo "Coverage $COVERAGE% is below threshold ${{ inputs.coverage-threshold }}%"
          exit 1
        fi
      shell: bash
```

## Reusable Workflows vs Composite Actions

| Aspect | Reusable Workflow | Composite Action |
|--------|------------------|------------------|
| Scope | Entire workflow | Single step |
| Location | `.github/workflows/` | `.github/actions/` |
| Secrets | Direct access | Passed as inputs |
| Jobs | Multiple jobs | Single logical step |
| Use case | Pipeline templates | Reusable step groups |
