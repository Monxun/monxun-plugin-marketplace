# Description Optimization Guide

Strategies for writing skill descriptions that trigger reliably.

## How Matching Works

Claude matches user requests against skill descriptions using semantic understanding:

1. User says: "I need to create a new plugin"
2. Claude scans skill descriptions
3. Best matching skill is triggered
4. Skill instructions loaded

## Description Format

```yaml
description: |
  [What it does - one sentence]
  Use when: [trigger keywords, comma-separated]
  Supports: [capabilities, comma-separated]
```

### Example
```yaml
description: |
  Creates production-ready Claude Code plugins with all components.
  Use when: creating a plugin, generating a plugin, building a plugin,
  making a new plugin, plugin factory, scaffold plugin, plugin template,
  "create plugin", "new plugin", "build plugin".
  Supports: commands, agents, skills, hooks, MCP servers, LSP servers.
```

## Keyword Categories

### 1. Action Verbs
```yaml
Use when: create, build, generate, make, implement, set up,
configure, develop, scaffold, initialize
```

### 2. Object Nouns
```yaml
Use when: plugin, skill, agent, hook, command, server,
template, component, manifest
```

### 3. Combined Phrases
```yaml
Use when: "create plugin", "build skill", "generate agent",
"make hook", "set up MCP"
```

### 4. Synonyms
```yaml
# Create = build = generate = make
Use when: create plugin, build plugin, generate plugin, make plugin
```

### 5. Common Misspellings/Variations
```yaml
Use when: plugin, plug-in, plug in
```

## Keyword Density

### Minimum: 5 keywords
```yaml
description: |
  Creates plugins.
  Use when: plugin, create, build, generate, make.
```

### Recommended: 10-15 keywords
```yaml
description: |
  Creates Claude Code plugins.
  Use when: creating a plugin, generating a plugin, building a plugin,
  making a new plugin, plugin factory, scaffold plugin, plugin template,
  "create plugin", "new plugin", "build plugin", "generate plugin".
```

### Maximum: 25-30 keywords
Balance coverage with description length limit (1024 chars).

## Trigger Testing

### Test Phrases to Try

```
"I want to create a plugin"
"Help me build a new plugin"
"Generate a plugin for me"
"Make a plugin that..."
"Set up a plugin"
"I need a plugin for..."
```

### Testing Method

```bash
# Start Claude and test each phrase
claude -p "create a plugin"
# Skill should trigger

claude -p "build a new plugin"
# Skill should trigger
```

## Common Patterns

### Domain Skill
```yaml
description: |
  Expert guidance for [domain].
  Use when: [domain] question, [domain] help, [domain] issue,
  working with [domain], "[domain] problem", "[domain] error".
  Supports: [specific capabilities].
```

### Task Skill
```yaml
description: |
  Performs [task] for [context].
  Use when: [task], [task verb], [task noun],
  "do [task]", "run [task]", "[task] for me".
  Supports: [variations of task].
```

### Integration Skill
```yaml
description: |
  Integrates [system A] with [system B].
  Use when: connect [A] [B], integrate [A] [B],
  [A] to [B], "[A] [B] integration".
  Supports: [specific integrations].
```

## Anti-Patterns

### ❌ Too Vague
```yaml
description: "Helps with stuff"
```
**Problem**: Won't match specific requests

### ❌ Too Specific
```yaml
description: "Creates PostgreSQL 15.2 plugins for Ubuntu 22.04"
```
**Problem**: Won't match general requests

### ❌ No Keywords
```yaml
description: "This skill provides plugin functionality."
```
**Problem**: No trigger words

### ❌ Over 1024 Characters
```yaml
description: |
  [Very long description that exceeds 1024 characters...]
```
**Problem**: Will be truncated

## Optimization Checklist

- [ ] Under 1024 characters
- [ ] Has "Use when:" section
- [ ] 10+ trigger keywords
- [ ] Includes action verbs
- [ ] Includes object nouns
- [ ] Includes common phrases
- [ ] Lists capabilities
- [ ] Tested with sample requests

## Character Count Check

```bash
# Extract description and count characters
sed -n '/^description:/,/^[a-z-]*:/p' SKILL.md | \
  head -n -1 | wc -c

# Should output: <= 1024
```

## A/B Testing Keywords

1. Start with baseline keywords
2. Test trigger phrases
3. Add missing keyword
4. Re-test
5. Iterate until reliable
