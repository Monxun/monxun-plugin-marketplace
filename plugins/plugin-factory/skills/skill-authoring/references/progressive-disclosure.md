# Progressive Disclosure Architecture

Guide to structuring skills for optimal context efficiency.

## Concept

Progressive disclosure loads information in stages:
1. **Metadata**: Always loaded (name, description)
2. **Instructions**: Loaded when triggered (SKILL.md body)
3. **Resources**: Loaded as needed (references, scripts)

## Benefits

| Benefit | Impact |
|---------|--------|
| Faster startup | Metadata is tiny (~100 tokens) |
| Lower context cost | Full skill only when needed |
| Better focus | Core instructions prioritized |
| Unlimited depth | References don't cost until read |

## Architecture

```
skill-name/
├── SKILL.md           # Level 2: Core instructions (< 500 lines)
├── references/        # Level 3: Extended documentation
│   ├── guide.md       # Detailed walkthrough
│   ├── api.md         # API reference
│   ├── examples.md    # Usage examples
│   └── faq.md         # Common questions
└── scripts/           # Level 3: Executable tools
    ├── validate.py    # Validation utility
    └── generate.sh    # Generation utility
```

## Loading Levels

### Level 1: Metadata (Always Loaded)

Only frontmatter YAML loaded at startup:

```yaml
---
name: skill-name
description: |
  Brief description with trigger keywords.
  Use when: keyword1, keyword2.
---
```

**Cost**: ~100 tokens per skill
**Purpose**: Discovery and matching

### Level 2: Instructions (On Trigger)

SKILL.md body loaded when skill activates:

```markdown
# Skill Title

## Quick Start
Essential instructions...

## Core Workflow
Main procedures...

## Resources
Links to references...
```

**Cost**: < 5000 tokens (target)
**Purpose**: Primary guidance

### Level 3: Resources (As Needed)

Additional files loaded only when referenced:

```markdown
For detailed API documentation, see [API Reference](references/api.md).
```

Claude reads the file only if needed for the task.

**Cost**: Variable, on-demand
**Purpose**: Extended documentation

## SKILL.md Guidelines

### What to Include

- Quick start (most common use case)
- Core workflow (main steps)
- Common patterns (frequent scenarios)
- Links to references

### What to Exclude

- Exhaustive API documentation
- Every edge case
- Lengthy examples
- Full code samples

### Line Budget

| Section | Lines |
|---------|-------|
| Frontmatter | 15-30 |
| Quick Start | 30-50 |
| Core Workflow | 100-150 |
| Common Patterns | 50-100 |
| References | 10-20 |
| **Total** | **< 500** |

## Reference File Strategy

### When to Create References

- Content > 50 lines
- Specialized topic
- Not needed for basic usage
- Complete API docs
- Extensive examples

### Reference Types

| Type | Content | When Used |
|------|---------|-----------|
| `guide.md` | Step-by-step tutorial | Learning |
| `api.md` | Complete API reference | Development |
| `examples.md` | Code samples | Implementation |
| `faq.md` | Common questions | Troubleshooting |
| `advanced.md` | Complex scenarios | Power users |

### Linking Pattern

In SKILL.md:
```markdown
## Detailed Resources

- For complete setup, see [Setup Guide](references/guide.md)
- For API details, see [API Reference](references/api.md)
- For examples, see [Examples](references/examples.md)
```

## Script Integration

### When to Use Scripts

- Deterministic operations
- Validation logic
- File generation
- Data processing

### Script Benefits

- No context cost (output only)
- Reliable execution
- Reusable utilities

### Script Reference

In SKILL.md:
```markdown
## Validation

Run the validation script:
```bash
python scripts/validate.py input.json
```
```

## Anti-Patterns

### ❌ Monolithic SKILL.md

```markdown
# Skill (1500 lines)

## Everything
[All documentation in one file]
```

**Problem**: High context cost on every trigger

### ✅ Progressive SKILL.md

```markdown
# Skill (400 lines)

## Essentials
[Core instructions]

## More Info
See [detailed guide](references/guide.md)
```

**Benefit**: Low initial cost, depth available

### ❌ No References

All documentation inline, no progressive loading.

### ✅ Structured References

Clear separation of core vs. extended content.

## Metrics

### Good Skill
- SKILL.md: 300-500 lines
- References: 2-5 files
- Scripts: 1-3 utilities
- Total loaded: 3000-5000 tokens

### Oversized Skill
- SKILL.md: 1000+ lines
- No references
- No scripts
- Total loaded: 10000+ tokens

## Migration Guide

### Converting Large Skills

1. **Identify sections** > 100 lines
2. **Extract to references**:
   - API docs → `api.md`
   - Examples → `examples.md`
   - Advanced → `advanced.md`
3. **Keep essentials** in SKILL.md
4. **Add links** to extracted content
5. **Test** that skill still functions
