# Conditional Blocks Reference

Complete reference for GTL conditional logic.

## Basic Conditionals

### If Block
```handlebars
{{#if condition}}
  Content when true
{{/if}}
```

### If-Else
```handlebars
{{#if condition}}
  Content when true
{{else}}
  Content when false
{{/if}}
```

### If-Else If-Else
```handlebars
{{#if condition1}}
  Content for condition1
{{else if condition2}}
  Content for condition2
{{else}}
  Default content
{{/if}}
```

## Comparison Operators

### Equality
```handlebars
{{#if variable == 'value'}}
{{#if variable != 'value'}}
{{#if variable === 'value'}}  <!-- Strict equality -->
{{#if variable !== 'value'}}  <!-- Strict inequality -->
```

### Numeric Comparisons
```handlebars
{{#if count > 0}}
{{#if count >= 10}}
{{#if count < 100}}
{{#if count <= 50}}
```

### String Comparisons
```handlebars
{{#if name == 'admin'}}
{{#if role != 'guest'}}
```

## Logical Operators

### AND
```handlebars
{{#if use_typescript && use_strict}}
  Strict TypeScript mode
{{/if}}
```

### OR
```handlebars
{{#if database == 'postgresql' || database == 'mysql'}}
  SQL database selected
{{/if}}
```

### NOT
```handlebars
{{#if !skip_tests}}
  Include tests
{{/if}}
```

### Complex Logic
```handlebars
{{#if (use_docker && !is_serverless) || force_container}}
  Include Docker configuration
{{/if}}
```

## Unless Block

Inverse of if - executes when condition is false:

```handlebars
{{#unless skip_docs}}
  Include documentation
{{/unless}}

<!-- Equivalent to -->
{{#if !skip_docs}}
  Include documentation
{{/if}}
```

## Truthiness

### Truthy Values
- Non-empty strings
- Non-zero numbers
- `true`
- Non-empty arrays
- Non-null objects

### Falsy Values
- Empty string `""`
- `0`
- `false`
- `null`
- `undefined`
- Empty array `[]`

## Conditional File Inclusion

### In genesis.json
```json
{
  "conditionals": {
    "docker/": "use_docker",
    "terraform/": "include_infrastructure",
    "tests/": "!skip_tests",
    "alembic/": "database != 'none' && database != 'mongodb'"
  }
}
```

### Directory Conditionals
```handlebars
{{#if use_docker}}
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
{{/if}}
```

## Inline Conditionals

### Ternary Expression
```handlebars
{{ use_typescript ? 'dist/index.js' : 'src/index.js' }}
```

### In JSON
```handlebars
{
  "main": "{{ use_typescript ? 'dist/index.js' : 'src/index.js' }}",
  "replicas": {{ environment == 'prod' ? 3 : 1 }}
}
```

## Complex Examples

### package.json with Conditionals
```handlebars
{
  "name": "{{ project_name }}",
  "scripts": {
    {{#if use_typescript}}
    "build": "tsc",
    "dev": "ts-node src/index.ts",
    {{else}}
    "dev": "node src/index.js",
    {{/if}}
    {{#unless skip_tests}}
    "test": "{{ use_vitest ? 'vitest' : 'jest' }}",
    {{/unless}}
    "start": "node {{ use_typescript ? 'dist' : 'src' }}/index.js"
  },
  "dependencies": {
    {{#if use_express}}
    "express": "^4.18.0"
    {{else if use_fastify}}
    "fastify": "^4.0.0"
    {{/if}}
  },
  "devDependencies": {
    {{#if use_typescript}}
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    {{/if}}
    {{#if use_eslint}}
    "eslint": "^8.0.0"{{#if use_prettier}},{{/if}}
    {{/if}}
    {{#if use_prettier}}
    "prettier": "^3.0.0"
    {{/if}}
  }
}
```

### GitHub Actions with Conditionals
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    {{#if use_services}}
    services:
      {{#if database == 'postgresql'}}
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
      {{else if database == 'mysql'}}
      mysql:
        image: mysql:8
        env:
          MYSQL_ROOT_PASSWORD: test
        ports:
          - 3306:3306
      {{/if}}
    {{/if}}
    steps:
      - uses: actions/checkout@v4
      {{#if use_node}}
      - uses: actions/setup-node@v4
        with:
          node-version: '{{ node_version }}'
      {{else if use_python}}
      - uses: actions/setup-python@v5
        with:
          python-version: '{{ python_version }}'
      {{/if}}
```
