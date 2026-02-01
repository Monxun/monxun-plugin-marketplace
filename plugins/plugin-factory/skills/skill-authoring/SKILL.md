---
name: skill-authoring
description: |
  Expert guidance for creating Claude Code skills with progressive disclosure.
  Use when: creating skills, writing SKILL.md, skill frontmatter, skill description,
  progressive disclosure, trigger keywords, "create skill", "skill template".
  Supports: frontmatter schema, description optimization, reference files.
allowed-tools: Read, Write, Edit, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Skill Authoring Skill

Create high-quality Claude Code skills with progressive disclosure architecture and optimized trigger descriptions.

## Skill Structure

```
skill-name/
├── SKILL.md              # Main file (< 500 lines)
└── references/
    ├── guide.md          # Extended documentation
    ├── api.md            # API reference
    └── examples.md       # Usage examples
```

## SKILL.md Template

```yaml
---
name: skill-name
description: |
  Brief description of what this skill does.
  Use when: trigger1, trigger2, trigger3.
  Supports: capability1, capability2.
allowed-tools: Read, Write, Edit
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Skill Title

## Quick Start
Essential instructions (what 80% of users need).

## Core Workflow
1. Step one
2. Step two
3. Step three

## Common Patterns
Frequently used patterns...

## Detailed Resources
- [Full Guide](references/guide.md)
- [API Reference](references/api.md)
- [Examples](references/examples.md)
```

## Frontmatter Schema

### Required Fields

| Field | Max Length | Rules |
|-------|------------|-------|
| `name` | 64 chars | lowercase, hyphens, numbers only |
| `description` | 1024 chars | Include trigger keywords |

### Optional Fields

| Field | Type | Purpose |
|-------|------|---------|
| `allowed-tools` | list | Restrict available tools |
| `model` | string | Override model |
| `context` | string | "fork" for isolation |
| `agent` | string | Agent type when forked |
| `hooks` | object | PreToolUse/PostToolUse/Stop |
| `user-invocable` | boolean | false to hide from slash |

## Description Optimization

### Trigger Keywords Strategy

Include keywords that users naturally say:

**Good Description:**
```yaml
description: |
  Creates production-ready Claude Code plugins.
  Use when: creating a plugin, generating a plugin, building a plugin,
  making a new plugin, plugin factory, scaffold plugin, plugin template,
  "create plugin", "new plugin", "build plugin", "generate plugin".
  Supports: commands, agents, skills, hooks, MCP servers.
```

**Bad Description:**
```yaml
description: "Helps with plugins"  # Too vague
```

### Keyword Categories

1. **Action verbs**: create, build, generate, make, implement
2. **Object nouns**: plugin, skill, agent, hook, command
3. **Synonyms**: build = create = generate = make
4. **Phrases**: "create plugin", "new skill", "add hook"

### Description Format

```yaml
description: |
  [What it does - one sentence]
  Use when: [comma-separated trigger keywords]
  Supports: [comma-separated capabilities]
```

## Progressive Disclosure

### Why < 500 Lines?

- Faster skill loading
- Lower context cost
- Better focus

### What Goes Where

| Content | Location | Purpose |
|---------|----------|---------|
| Core instructions | SKILL.md | Essential guidance |
| Detailed guides | references/ | Extended docs |
| API reference | references/ | Complete reference |
| Examples | references/ | Sample usage |
| Scripts | scripts/ | Automation |

### Linking to References

```markdown
## Detailed Resources

For complete API documentation, see [API Reference](references/api.md).
For usage examples, see [Examples](references/examples.md).
```

## Best Practices

### Do
- Keep SKILL.md focused on essentials
- Include "Use when:" in description
- List 5+ trigger keywords
- Use progressive disclosure
- Test trigger phrases

### Don't
- Exceed 500 lines in SKILL.md
- Use vague descriptions
- Include all documentation inline
- Forget trigger keywords
- Hardcode paths

## Validation

```bash
# Check line count
wc -l skills/*/SKILL.md

# Check description length
grep -A 20 'description:' skills/*/SKILL.md | wc -c

# Test triggers
claude -p "create a skill"  # Should match
```

## Detailed References

- [Frontmatter Schema](references/frontmatter-schema.md)
- [Progressive Disclosure](references/progressive-disclosure.md)
- [Description Optimization](references/description-optimization.md)
