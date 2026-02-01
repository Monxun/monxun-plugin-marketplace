---
name: validate-template
description: Run quality validation on a Genesis template
allowed-tools: Read, Bash, Grep, Glob
argument-validation: required
---

# Validate Template Command

Run comprehensive quality validation on a Genesis template.

## Usage

```
/genesis:validate-template <template-path> [options]
```

## Arguments

- `$1` - Path to template directory (required)
- `$ARGUMENTS` - Full argument string

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--fix` | Attempt auto-fixes | false |
| `--strict` | Fail on warnings | false |
| `--output <format>` | Output format (json, markdown) | markdown |
| `--gates <list>` | Gates to run | all |

## Quality Gates

### Gate 1: Structure (25%)
- Required directories exist
- genesis.json present
- No misplaced files
- Proper naming conventions

### Gate 2: Syntax (25%)
- JSON files valid
- YAML files valid
- Template syntax correct
- HCL valid (if present)

### Gate 3: Completeness (25%)
- Manifest has required fields
- All variables defined in prompts
- Conditional directories exist
- Post-generation scripts valid

### Gate 4: Security (25%)
- No hardcoded secrets
- No sensitive files
- Dockerfile security
- Workflow secrets

## Examples

```bash
# Basic validation
/genesis:validate-template ./my-template

# Strict mode (fail on warnings)
/genesis:validate-template ./my-template --strict

# Output as JSON
/genesis:validate-template ./my-template --output json

# Run specific gates
/genesis:validate-template ./my-template --gates structure,security
```

## Output

```json
{
  "status": "pass",
  "score": 92,
  "grade": "A",
  "gates": {
    "structure": {"score": 25, "max": 25},
    "syntax": {"score": 25, "max": 25},
    "completeness": {"score": 22, "max": 25},
    "security": {"score": 20, "max": 25}
  },
  "errors": [],
  "warnings": [
    {"gate": "completeness", "message": "Undefined variable: api_timeout"}
  ]
}
```

## Injected Skills

- `heuristics-engine` - Quality validation patterns

## Delegates To

- `genesis-validator` agent for validation

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed (errors) |
| 2 | Validation passed with warnings |
