# Plugin Factory Heuristics

Research-driven quality patterns and anti-patterns for Claude Code plugins.

## Core Heuristics

### H1: Structure Isolation

**Rule**: Only `plugin.json` in `.claude-plugin/`

**Why**: Claude Code expects manifest isolation. Components in `.claude-plugin/` may not be discovered.

**Check**:
```bash
ls .claude-plugin/
# Expected: plugin.json (only)
```

**Fix**: Move components to plugin root.

### H2: Progressive Disclosure

**Rule**: SKILL.md < 500 lines

**Why**: Large skill files consume context tokens. Split into references.

**Check**:
```bash
wc -l skills/*/SKILL.md
# All should be < 500
```

**Fix**: Extract detailed sections to `references/`.

### H3: Description Optimization

**Rule**: Include trigger keywords in descriptions

**Why**: Skills are auto-discovered based on description matching.

**Good**:
```yaml
description: |
  Plugin validation and quality metrics.
  Use when: validation, quality gates, "validate plugin".
  Supports: structure validation, schema validation.
```

**Bad**:
```yaml
description: Handles plugin stuff.
```

### H4: Tool Scoping

**Rule**: Minimum necessary tool access

**Why**: Reduces attack surface, prevents accidental changes.

| Purpose | Tools |
|---------|-------|
| Research | Read, Grep, Glob |
| Validation | Read, Bash (no Write) |
| Building | Read, Write, Edit |

### H5: Exit Code Semantics

**Rule**: Use exit 2 to block, exit 0 to continue

**Why**: Claude interprets exit codes differently.

| Exit | Meaning |
|------|---------|
| 0 | Success, parse JSON output |
| 2 | Block operation, show stderr |
| Other | Non-blocking error |

## Quality Metrics

### Structure Score (25 points)

| Check | Points |
|-------|--------|
| plugin.json exists | 5 |
| Only plugin.json in .claude-plugin/ | 5 |
| Components at root | 5 |
| All paths valid | 5 |
| Proper organization | 5 |

### Schema Score (25 points)

| Check | Points |
|-------|--------|
| Valid JSON files | 5 |
| Valid YAML frontmatter | 5 |
| Required fields present | 5 |
| Name kebab-case | 5 |
| Version semver | 5 |

### Component Score (25 points)

| Check | Points |
|-------|--------|
| Command frontmatter valid | 5 |
| Agent frontmatter valid | 5 |
| SKILL.md exists per skill | 5 |
| Hook scripts executable | 5 |
| Descriptions include keywords | 5 |

### Quality Score (25 points)

| Check | Points |
|-------|--------|
| SKILL.md < 500 lines | 10 |
| References for detailed docs | 5 |
| Scripts for deterministic ops | 5 |
| No hardcoded paths | 5 |

## Anti-Patterns

### AP1: Components in .claude-plugin/

**Pattern**:
```
.claude-plugin/
├── plugin.json
├── commands/       ← WRONG
└── skills/         ← WRONG
```

**Issue**: Components may not be discovered.

**Fix**: Move to plugin root.

### AP2: Monolithic Skills

**Pattern**: SKILL.md with 800+ lines

**Issue**: Consumes excessive context tokens.

**Fix**: Extract to `references/` subdirectory.

### AP3: Vague Descriptions

**Pattern**:
```yaml
description: Does things with plugins
```

**Issue**: Won't match natural language triggers.

**Fix**: Add "Use when:" and "Supports:" patterns.

### AP4: Overpermissioned Agents

**Pattern**:
```yaml
allowed-tools: Read, Write, Edit, Bash, Task, WebSearch
```

**Issue**: Unnecessary capabilities, security risk.

**Fix**: Scope to minimum needed tools.

### AP5: Hardcoded Paths

**Pattern**:
```json
"command": "/Users/dev/plugin/scripts/hook.py"
```

**Issue**: Won't work for other users.

**Fix**: Use `${CLAUDE_PLUGIN_ROOT}/scripts/hook.py`

### AP6: Missing Frontmatter

**Pattern**: Markdown files without `---` header

**Issue**: Claude can't parse metadata.

**Fix**: Add YAML frontmatter with required fields.

### AP7: Blocking Without Exit 2

**Pattern**:
```python
if error:
    print("Error!", file=sys.stderr)
    sys.exit(1)  # Wrong!
```

**Issue**: Exit 1 doesn't block, continues with error.

**Fix**: Use `sys.exit(2)` to block operations.

## Validation Workflow

### Pre-Commit Checks

```bash
# Structure
[ -f .claude-plugin/plugin.json ] || echo "Missing manifest"
[ $(ls .claude-plugin/ | wc -l) -eq 1 ] || echo "Extra files"

# Schema
jq . .claude-plugin/plugin.json > /dev/null

# Line counts
for f in skills/*/SKILL.md; do
  [ $(wc -l < "$f") -lt 500 ] || echo "$f too long"
done
```

### Remediation Loop

```
for i in {1..5}; do
  validate_plugin
  if [ $? -eq 0 ]; then
    echo "Pass"
    break
  fi
  fix_errors
done
```

### Quality Report

```json
{
  "score": 95,
  "grade": "A",
  "gates": {
    "structure": {"passed": true, "score": 25},
    "schema": {"passed": true, "score": 25},
    "components": {"passed": true, "score": 25},
    "quality": {"passed": true, "score": 20}
  },
  "recommendations": [
    "Add reference files for large skill"
  ]
}
```

## Research Sources

These heuristics are derived from:

1. Official Claude Code documentation
2. Plugin reference specifications
3. Hooks reference guide
4. Community best practices
5. Testing and validation patterns

## Updates

This document is updated based on:
- New Claude Code releases
- Community feedback
- Validation findings
- Research discoveries
