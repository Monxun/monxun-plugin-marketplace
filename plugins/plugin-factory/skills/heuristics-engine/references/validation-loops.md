# Validation Loops

Implementing iterative validation and remediation.

## Loop Structure

```
┌─────────────┐
│   Validate  │
└──────┬──────┘
       │
       ▼
   ┌───────┐
   │ Pass? │──Yes──→ Done
   └───┬───┘
       │ No
       ▼
   ┌────────┐
   │  Fix   │
   └────┬───┘
       │
       ▼
┌──────────────┐
│ iterations < │──Yes──→ Validate
│     5?       │
└──────┬───────┘
       │ No
       ▼
   Report
   Unresolved
```

## Implementation

### Validation Function
```python
def validate_plugin(path):
    """Run all validation checks."""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }

    # Gate 1: Structure
    check_structure(path, results)

    # Gate 2: Schema
    check_schema(path, results)

    # Gate 3: Components
    check_components(path, results)

    # Gate 4: Integration
    check_integration(path, results)

    return results
```

### Remediation Loop
```python
MAX_ITERATIONS = 5

def validate_and_fix(path):
    """Validate with remediation loop."""
    for iteration in range(MAX_ITERATIONS):
        results = validate_plugin(path)

        if not results["failed"]:
            return {"status": "pass", "iterations": iteration + 1}

        # Attempt fixes
        for error in results["failed"]:
            fix = get_fix_strategy(error)
            if fix:
                apply_fix(fix)

    # Still failing after max iterations
    return {
        "status": "fail",
        "iterations": MAX_ITERATIONS,
        "unresolved": results["failed"]
    }
```

### Fix Strategies
```python
FIX_STRATEGIES = {
    "structure.misplaced_component": move_component_to_root,
    "schema.invalid_json": fix_json_syntax,
    "schema.invalid_name": fix_name_format,
    "component.missing_frontmatter": add_frontmatter,
    "component.skill_too_long": refactor_skill,
}

def get_fix_strategy(error):
    """Get fix strategy for error type."""
    return FIX_STRATEGIES.get(error["type"])
```

## Validation Checks

### Structure Checks
```bash
# Check 1: Only plugin.json in .claude-plugin/
check_structure() {
  contents=$(ls .claude-plugin/)
  if [ "$contents" != "plugin.json" ]; then
    echo "FAIL: Extra files in .claude-plugin/"
    return 1
  fi
  return 0
}
```

### Schema Checks
```bash
# Check 2: Valid JSON
check_json() {
  jq . "$1" > /dev/null 2>&1
  return $?
}

# Check 3: Name format
check_name() {
  name=$(jq -r '.name' .claude-plugin/plugin.json)
  echo "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'
  return $?
}
```

### Component Checks
```bash
# Check 4: Frontmatter exists
check_frontmatter() {
  for f in "$1"/*.md; do
    head -1 "$f" | grep -q '^---' || return 1
  done
  return 0
}

# Check 5: SKILL.md exists
check_skills() {
  for d in skills/*/; do
    [ -f "${d}SKILL.md" ] || return 1
  done
  return 0
}
```

## Error Reporting

### Report Format
```json
{
  "status": "pass|fail",
  "iterations": 3,
  "gates": {
    "structure": {"status": "pass", "checks": 4},
    "schema": {"status": "pass", "checks": 3},
    "components": {"status": "pass", "checks": 5},
    "integration": {"status": "pass", "checks": 2}
  },
  "errors": [],
  "warnings": [
    {"gate": "components", "message": "SKILL.md is 480 lines (approaching limit)"}
  ]
}
```

### Error Categories
```python
ERROR_CATEGORIES = {
    "structure": [
        "misplaced_component",
        "missing_manifest",
        "invalid_directory"
    ],
    "schema": [
        "invalid_json",
        "invalid_name",
        "missing_required_field"
    ],
    "components": [
        "missing_frontmatter",
        "invalid_frontmatter",
        "skill_too_long",
        "missing_description"
    ],
    "integration": [
        "load_error",
        "command_not_found"
    ]
}
```

## Progress Tracking

### Track Iterations
```python
class ValidationProgress:
    def __init__(self):
        self.iteration = 0
        self.history = []

    def record(self, results):
        self.iteration += 1
        self.history.append({
            "iteration": self.iteration,
            "passed": len(results["passed"]),
            "failed": len(results["failed"]),
            "errors": [e["type"] for e in results["failed"]]
        })

    def is_improving(self):
        if len(self.history) < 2:
            return True
        return self.history[-1]["failed"] < self.history[-2]["failed"]
```

### Early Termination
```python
def should_continue(progress):
    """Determine if remediation should continue."""
    # Stop if not improving
    if not progress.is_improving():
        return False

    # Stop if max iterations
    if progress.iteration >= MAX_ITERATIONS:
        return False

    # Stop if all passed
    if progress.history[-1]["failed"] == 0:
        return False

    return True
```

## Best Practices

1. **Validate Early**: Run validation before time-consuming steps
2. **Track Progress**: Log each iteration's results
3. **Prioritize Fixes**: Fix blocking errors first
4. **Limit Iterations**: Don't loop indefinitely
5. **Report Clearly**: Provide actionable error messages
