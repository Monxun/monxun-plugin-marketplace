# Matrix Builds Reference

Complete guide to matrix strategy in GitHub Actions.

## Basic Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

This creates 6 jobs (3 Node versions × 2 OS).

## Matrix Options

### fail-fast
```yaml
strategy:
  fail-fast: false  # Continue other jobs if one fails
  matrix:
    node: [18, 20, 22]
```

### max-parallel
```yaml
strategy:
  max-parallel: 2  # Run at most 2 jobs concurrently
  matrix:
    node: [18, 20, 22]
```

## Include / Exclude

### Exclude Combinations
```yaml
strategy:
  matrix:
    node: [18, 20, 22]
    os: [ubuntu-latest, macos-latest, windows-latest]
    exclude:
      - os: windows-latest
        node: 18
      - os: macos-latest
        node: 22
```

### Include Additional Combinations
```yaml
strategy:
  matrix:
    node: [18, 20]
    include:
      - node: 22
        os: ubuntu-latest
        experimental: true
      - node: 20
        os: ubuntu-latest
        coverage: true
```

### Include New Variables
```yaml
strategy:
  matrix:
    node: [18, 20, 22]
    include:
      - node: 18
        npm: 9
      - node: 20
        npm: 10
      - node: 22
        npm: 10
```

## Dynamic Matrix

### From JSON Output
```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          MATRIX='{"node": [18, 20, 22], "os": ["ubuntu-latest", "macos-latest"]}'
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  test:
    needs: setup
    strategy:
      matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

### From File
```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set-matrix
        run: |
          MATRIX=$(cat .github/matrix.json)
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  test:
    needs: setup
    strategy:
      matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
```

## Complex Matrix Patterns

### Multi-Language Testing
```yaml
strategy:
  matrix:
    language: [node, python, go]
    include:
      - language: node
        version: '20'
        setup: actions/setup-node@v4
        install: npm ci
        test: npm test
      - language: python
        version: '3.12'
        setup: actions/setup-python@v5
        install: pip install -r requirements.txt
        test: pytest
      - language: go
        version: '1.22'
        setup: actions/setup-go@v5
        install: go mod download
        test: go test ./...
```

### Database Testing
```yaml
strategy:
  matrix:
    database: [postgresql, mysql, sqlite]
    include:
      - database: postgresql
        db_url: postgres://postgres:postgres@localhost:5432/test
        service_image: postgres:16
      - database: mysql
        db_url: mysql://root:root@localhost:3306/test
        service_image: mysql:8
      - database: sqlite
        db_url: sqlite:///test.db
        service_image: ''
```

### Environment-Based Matrix
```yaml
strategy:
  matrix:
    environment: [dev, staging, prod]
    include:
      - environment: dev
        aws_region: us-east-1
        replicas: 1
      - environment: staging
        aws_region: us-east-1
        replicas: 2
      - environment: prod
        aws_region: us-west-2
        replicas: 3
```

## Using Matrix Values

### In Steps
```yaml
steps:
  - name: Show matrix values
    run: |
      echo "Node: ${{ matrix.node }}"
      echo "OS: ${{ matrix.os }}"

  - name: Conditional step
    if: ${{ matrix.node == 20 }}
    run: echo "Running on Node 20"
```

### In Job Name
```yaml
jobs:
  test:
    name: Test Node ${{ matrix.node }} on ${{ matrix.os }}
    strategy:
      matrix:
        node: [18, 20]
        os: [ubuntu-latest, macos-latest]
```

### In Artifacts
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: results-${{ matrix.node }}-${{ matrix.os }}
    path: results/
```

## Best Practices

### 1. Keep Matrix Small
```yaml
# Good - focused matrix
strategy:
  matrix:
    node: [20, 22]  # Current LTS + latest

# Avoid - too many combinations
strategy:
  matrix:
    node: [16, 18, 19, 20, 21, 22]
    os: [ubuntu-latest, macos-latest, windows-latest]
```

### 2. Use Include for Edge Cases
```yaml
strategy:
  matrix:
    node: [20]  # Standard testing
    include:
      - node: 18
        os: ubuntu-latest
        legacy: true
      - node: 22
        os: ubuntu-latest
        experimental: true
```

### 3. Fail-Fast for PR Checks
```yaml
strategy:
  fail-fast: true  # Fail quickly on PRs
  matrix:
    node: [20, 22]
```

### 4. Full Matrix for Releases
```yaml
strategy:
  fail-fast: false  # Run all combinations
  matrix:
    node: [18, 20, 22]
    os: [ubuntu-latest, macos-latest, windows-latest]
```
