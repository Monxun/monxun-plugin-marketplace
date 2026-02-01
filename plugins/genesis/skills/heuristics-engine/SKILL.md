---
name: heuristics-engine
description: |
  Quality validation heuristics for Genesis templates.
  Use when: validation, quality gates, heuristics, remediation,
  quality metrics, validation loops, "quality check", "validate template",
  AutoHD discovery, POPPER validation, statistical testing.
  Supports: structure validation, schema validation, security scanning.
allowed-tools: Read, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Heuristics Engine Skill

Apply research-driven quality validation for Genesis templates.

## Quality Gates

### Gate 1: Structure (25%)
```bash
# Check required directories
for dir in templates docs; do
  [ -d "$dir" ] || echo "ERROR: Missing $dir"
done

# Check genesis.json exists
[ -f "genesis.json" ] || echo "ERROR: Missing genesis.json"

# Verify no misplaced files
find templates -name "*.json" -not -name "*.template" | head -5
```

### Gate 2: Syntax (25%)
```bash
# Validate JSON
for f in $(find . -name "*.json"); do
  jq . "$f" > /dev/null 2>&1 || echo "ERROR: Invalid JSON: $f"
done

# Validate YAML
for f in $(find . -name "*.yml" -o -name "*.yaml"); do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "ERROR: Invalid YAML: $f"
done
```

### Gate 3: Completeness (25%)
```bash
# Check manifest fields
jq -e '.name' genesis.json > /dev/null || echo "ERROR: Missing name"
jq -e '.prompts' genesis.json > /dev/null || echo "ERROR: Missing prompts"

# Check variables defined
grep -oE '\{\{\s*[a-z_]+' templates/**/*.template | while read var; do
  var=$(echo "$var" | sed 's/{{[ ]*//')
  jq -e ".prompts[] | select(.name == \"$var\")" genesis.json > /dev/null || \
    echo "WARNING: Undefined variable: $var"
done
```

### Gate 4: Security (25%)
```bash
# Check for hardcoded secrets
grep -rn "password.*=" . --include="*.template" | grep -v "{{ " && \
  echo "WARNING: Potential hardcoded password"

# Check Dockerfile security
grep -q "USER root" Dockerfile* && echo "WARNING: Running as root"
grep -q "USER" Dockerfile* || echo "WARNING: No non-root user"
```

## Quality Score Calculation

```
Total Score = Structure(25) + Syntax(25) + Completeness(25) + Security(25)

Grade:
  A: 90-100
  B: 80-89
  C: 70-79
  D: 60-69
  F: <60
```

## Validation Report Format

```json
{
  "status": "pass|fail|warning",
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
    {"gate": "completeness", "file": "...", "message": "..."}
  ]
}
```

## Remediation Loop

```
Validate → [Pass] → Complete
    ↓
  [Fail]
    ↓
  Report Issues with Fixes
    ↓
  Request Fix from Builder
    ↓
  Re-validate (max 5x)
    ↓
  [Still Fail] → Report Unresolved
```

## AutoHD Pattern Discovery

1. **Generate Candidates**: Extract recurring patterns
2. **Evaluate**: Score against examples
3. **Evolve**: Combine best patterns
4. **Validate**: POPPER falsification testing

## POPPER Validation

1. Decompose into testable hypotheses
2. Design falsification experiments
3. Execute tests, calculate e-values
4. Accumulate evidence, reject or accept

## Quick Validation

```bash
# Full validation script
echo "=== Structure ===" && ls -la
echo "=== Syntax ===" && jq . genesis.json
echo "=== Variables ===" && grep -oE '\{\{[^}]+\}\}' templates/**/* | sort -u
echo "=== Security ===" && grep -rn "secret\|password\|key" . --include="*.template"
```

## Detailed References

- [AutoHD Discovery](references/autohd-discovery.md) - Heuristic generation
- [POPPER Validation](references/popper-validation.md) - Statistical validation
- [Quality Gates](references/quality-gates.md) - Gate definitions
