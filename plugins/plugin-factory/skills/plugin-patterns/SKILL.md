---
name: plugin-patterns
description: |
  Core plugin architecture and structure patterns for Claude Code.
  Use when: creating plugins, understanding plugin structure, plugin manifest,
  component organization, "create plugin", "plugin structure", "plugin.json".
  Supports: commands, agents, skills, hooks, MCP servers, LSP servers.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Plugin Patterns Skill

Generate production-ready Claude Code plugins with proper structure, manifest configuration, and component organization.

## Critical Rule: Component Location

**NEVER place components inside `.claude-plugin/` directory.**

```
✅ CORRECT:
plugin-name/
├── .claude-plugin/
│   └── plugin.json    # ONLY file here
├── commands/          # At plugin root
├── agents/            # At plugin root
├── skills/            # At plugin root
└── hooks/             # At plugin root

❌ WRONG:
plugin-name/
├── .claude-plugin/
│   ├── plugin.json
│   ├── commands/      # WRONG!
│   └── agents/        # WRONG!
```

## Plugin Manifest (plugin.json)

### Required Fields
```json
{
  "name": "plugin-name"  // kebab-case only
}
```

### Recommended Fields
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  },
  "keywords": ["tag1", "tag2"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}
```

## Component Types

### Commands (Slash Commands)
- Location: `commands/*.md`
- Purpose: User-invoked entry points
- Pattern: Thin wrapper → delegate to skill/agent

### Agents (Custom Subagents)
- Location: `agents/*.md`
- Purpose: Specialized task handlers
- Pattern: Scoped tools + focused prompt

### Skills (Model-Invoked)
- Location: `skills/*/SKILL.md`
- Purpose: Auto-triggered capabilities
- Pattern: Progressive disclosure

### Hooks (Lifecycle Events)
- Location: `hooks/hooks.json` + `hooks/scripts/`
- Purpose: Automated validation/formatting
- Pattern: Exit code control

### MCP Servers
- Location: `.mcp.json`
- Purpose: External tool integration
- Pattern: ${CLAUDE_PLUGIN_ROOT} paths

## Quick Start: Create a Plugin

### 1. Create Directory Structure
```bash
mkdir -p plugin-name/.claude-plugin
mkdir -p plugin-name/{commands,agents,skills,hooks/scripts,docs}
```

### 2. Write plugin.json
```bash
cat > plugin-name/.claude-plugin/plugin.json << 'EOF'
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Your plugin description",
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}
EOF
```

### 3. Create Thin Wrapper Command
```markdown
---
description: Main entry point
argument-hint: [args]
allowed-tools: Read, Write
context: fork
agent: general-purpose
---

# Command Name

Instructions for Claude...
```

### 4. Test Plugin
```bash
claude --plugin-dir ./plugin-name
```

## Detailed References

- [Plugin Structure Guide](references/plugin-structure.md)
- [Manifest Schema Reference](references/manifest-schema.md)
- [Component Creation Guide](references/component-guide.md)

## Validation Checklist

- [ ] Only plugin.json in .claude-plugin/
- [ ] Name is kebab-case
- [ ] All paths exist
- [ ] Commands have frontmatter
- [ ] Agents have name/description
- [ ] Skills < 500 lines
