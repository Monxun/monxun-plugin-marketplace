---
name: create-skill
description: Create a progressive disclosure skill with SKILL.md and reference files
allowed-tools: Read, Write, Edit, Bash, Glob
argument-validation: optional
---

# Create Skill Command

Generate a skill with progressive disclosure architecture.

## Usage

```
/plugin-factory:create-skill <skill-name> [target-plugin]
```

## Arguments

- `$1` - Skill name (kebab-case, required)
- `$2` - Target plugin directory (optional, defaults to current)

## Workflow

Delegates to `skill-builder` agent which:

1. Creates skill directory structure
2. Generates SKILL.md with proper frontmatter
3. Creates references/ subdirectory
4. Adds reference documentation files
5. Validates line count < 500

## Injected Skills

- `skill-authoring` - Frontmatter, progressive disclosure patterns

## Output Structure

```
skills/<skill-name>/
├── SKILL.md              # Main skill file (< 500 lines)
└── references/
    ├── overview.md       # Detailed overview
    ├── patterns.md       # Usage patterns
    └── examples.md       # Code examples
```

## Example

```bash
# Create a new skill
/plugin-factory:create-skill data-processing

# Create skill in specific plugin
/plugin-factory:create-skill auth-handler ./my-plugin
```

## Progressive Disclosure

- SKILL.md contains essential patterns only
- Complex documentation in references/
- Scripts for deterministic operations
