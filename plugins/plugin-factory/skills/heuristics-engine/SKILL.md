---
name: heuristics-engine
description: |
  Research-driven quality heuristics for plugin validation.
  Use when: validation, quality gates, heuristics, remediation,
  quality metrics, validation loops, "quality check", "validate plugin".
  Supports: structure validation, schema validation, progressive disclosure.
allowed-tools: Read, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Heuristics Engine Skill

Apply research-driven quality heuristics for Claude Code plugin validation and remediation.

## Quality Gates

### Gate 1: Structure Validation
```bash
# Only plugin.json in .claude-plugin/
ls .claude-plugin/
# Expected: plugin.json only

# No directories in .claude-plugin/
find .claude-plugin -type d -mindepth 1
# Expected: (empty)

# Components at root
ls -d commands/ agents/ skills/ 2>/dev/null
```

### Gate 2: Schema Validation
```bash
# Valid JSON
jq . .claude-plugin/plugin.json

# Name is kebab-case
jq -r '.name' .claude-plugin/plugin.json | grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'

# hooks.json valid (if exists)
[ -f hooks/hooks.json ] && jq . hooks/hooks.json
```

### Gate 3: Description Quality
```bash
# Skill descriptions < 1024 chars
for f in skills/*/SKILL.md; do
  desc=$(sed -n '/^description:/,/^[a-z-]*:/p' "$f" | head -n -1)
  len=$(echo "$desc" | wc -c)
  [ "$len" -gt 1024 ] && echo "WARN: $f description too long"
done
```

### Gate 4: Progressive Disclosure
```bash
# SKILL.md < 500 lines
for f in skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  [ "$lines" -gt 500 ] && echo "WARN: $f has $lines lines (max 500)"
done
```

### Gate 5: Integration Test
```bash
# Plugin loads without errors
claude --plugin-dir . 2>&1 | grep -i error
```

## Validation Checklist

### Structure
- [ ] `.claude-plugin/plugin.json` exists
- [ ] Only plugin.json in `.claude-plugin/`
- [ ] All components at plugin root
- [ ] All referenced paths exist

### Schema
- [ ] plugin.json valid JSON
- [ ] name is kebab-case
- [ ] hooks.json valid JSON (if present)
- [ ] .mcp.json valid JSON (if present)

### Components
- [ ] Commands have valid frontmatter
- [ ] Agents have name and description
- [ ] Skills have SKILL.md
- [ ] Hook scripts are executable

### Quality
- [ ] SKILL.md < 500 lines
- [ ] Descriptions include keywords
- [ ] References for detailed docs
- [ ] Scripts for automation

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

### Max Iterations
- Limit: 5 remediation attempts
- After 5: Report remaining issues

### Fix Categories
| Category | Fix Strategy |
|----------|--------------|
| Structure | Move files to correct location |
| Schema | Correct JSON/YAML syntax |
| Missing | Create required files |
| Quality | Refactor for compliance |

## Anti-Patterns

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| Components in .claude-plugin/ | `ls .claude-plugin/` | Move to root |
| SKILL.md > 500 lines | `wc -l` | Progressive disclosure |
| Vague descriptions | Manual review | Add trigger keywords |
| No validation hooks | Check hooks.json | Add PreToolUse hooks |
| Hardcoded paths | `grep -r "/"` | Use ${CLAUDE_PLUGIN_ROOT} |

## Detailed References

- [Validation Loops](references/validation-loops.md)
- [Remediation Patterns](references/remediation-patterns.md)
- [Quality Metrics](references/quality-metrics.md)
