---
name: validate-plugin
description: Validate plugin structure, schemas, and integration with remediation loop
allowed-tools: Read, Bash, Grep, Glob
argument-validation: optional
---

# Validate Plugin Command

Run comprehensive validation with automated remediation.

## Usage

```
/plugin-factory:validate-plugin [plugin-path]
```

## Arguments

- `$1` - Plugin path (optional, defaults to current directory)

## Workflow

Delegates to `validator` agent which runs:

### Gate 1: Structure Validation
- `.claude-plugin/plugin.json` exists
- Only plugin.json in `.claude-plugin/`
- Components at plugin root

### Gate 2: Schema Validation
- Valid JSON/YAML syntax
- Required fields present
- Kebab-case naming

### Gate 3: Component Validation
- Command frontmatter valid
- Agent frontmatter valid
- Skill structure correct

### Gate 4: Quality Validation
- SKILL.md < 500 lines
- Descriptions include keywords
- Progressive disclosure applied

### Gate 5: Integration Test
- Plugin loads without errors
- Commands appear in /help
- Agents appear in /agents

## Injected Skills

- `heuristics-engine` - Validation loops, remediation patterns

## Remediation Loop

```
Validate → [Pass] → Done
    ↓
  [Fail]
    ↓
  Fix → Validate (max 5x)
    ↓
  [Still Fail]
    ↓
  Report Unresolved
```

## Example

```bash
# Validate current plugin
/plugin-factory:validate-plugin

# Validate specific plugin
/plugin-factory:validate-plugin ./my-plugin
```

## Output

Returns validation report:
- Pass/fail status per gate
- Specific errors found
- Remediation actions taken
- Quality score (A-F grade)
