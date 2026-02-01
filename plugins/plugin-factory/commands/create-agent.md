---
name: create-agent
description: Create a specialized subagent with scoped tools and permissions
allowed-tools: Read, Write, Edit, Glob
argument-validation: optional
---

# Create Agent Command

Generate a custom subagent with proper tool scoping and frontmatter.

## Usage

```
/plugin-factory:create-agent <agent-name> [target-plugin]
```

## Arguments

- `$1` - Agent name (kebab-case, required)
- `$2` - Target plugin directory (optional, defaults to current)

## Workflow

Delegates to `agent-builder` agent which:

1. Gathers agent purpose and capabilities
2. Determines appropriate tool scoping
3. Selects optimal model (haiku/sonnet/opus)
4. Generates agent markdown with frontmatter
5. Validates against schema

## Injected Skills

- `agent-design` - Frontmatter schema, tool scoping, orchestration patterns

## Frontmatter Options

```yaml
---
name: agent-name
description: Agent purpose and trigger keywords
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit, Bash
permissionMode: default
skills: skill-name-to-inject
context: fork
---
```

## Example

```bash
# Create a research agent
/plugin-factory:create-agent code-reviewer

# Create agent with specific model
/plugin-factory:create-agent quick-validator --model haiku
```

## Best Practices

- Use `haiku` for fast, simple tasks
- Scope tools to minimum needed
- Include trigger keywords in description
