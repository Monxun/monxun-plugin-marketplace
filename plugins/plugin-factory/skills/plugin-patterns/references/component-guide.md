# Component Creation Guide

Detailed guide for creating each type of plugin component.

## Commands

### Purpose
User-invoked entry points via slash commands (`/plugin-name:command`).

### Pattern: Thin Wrapper
Commands should be lightweight wrappers that delegate to skills or agents.

### Structure
```markdown
---
description: Brief description for /help
argument-hint: [arg1] [arg2]
allowed-tools: Read, Write, Bash
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Command Title

Instructions for Claude when this command is invoked.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | No | Shown in /help |
| `argument-hint` | No | Autocomplete suggestion |
| `allowed-tools` | No | Tool permissions |
| `model` | No | Model override |
| `context` | No | "fork" for isolation |
| `agent` | No | Agent type when forked |
| `hooks` | No | Command-scoped hooks |

### Example: Git Commit Command
```markdown
---
description: Create a well-formatted git commit
argument-hint: [message]
allowed-tools: Bash(git *)
---

# Git Commit

Create a commit with the provided message, following conventional commits format.

Use $ARGUMENTS as the commit message.
```

### Example: Forked Context Command
```markdown
---
description: Analyze code quality
allowed-tools: Read, Grep
context: fork
agent: Explore
---

# Code Analysis

Analyze the current codebase for quality issues.
Run in isolated context to preserve main conversation.
```

## Agents

### Purpose
Specialized subagents for task delegation.

### Structure
```markdown
---
name: agent-name
description: |
  When to delegate to this agent.
  Use when: specific scenarios.

tools: Read, Write, Edit
disallowedTools: WebSearch
model: sonnet
permissionMode: default
skills: skill-one, skill-two
---

# Agent Title

You are a [role]. Your purpose is to [objective].

## Tasks

1. Task one
2. Task two

## Output Format

Expected output structure...

## Constraints

- DO NOT...
- ALWAYS...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | Delegation criteria |
| `tools` | No | Allowed tools (inherit if omitted) |
| `disallowedTools` | No | Explicitly denied tools |
| `model` | No | sonnet/opus/haiku/inherit |
| `permissionMode` | No | default/acceptEdits/dontAsk/bypassPermissions/plan |
| `skills` | No | Skills to inject |
| `hooks` | No | Agent-scoped hooks |

### Example: Validator Agent
```markdown
---
name: validator
description: |
  Validation specialist. Use when: testing, verifying quality.
tools: Read, Bash, Grep
disallowedTools: Write, Edit
model: haiku
---

# Validator

You test and validate without modifying files.

## Validation Steps
1. Check syntax
2. Verify structure
3. Run tests

## Report Format
JSON with status, errors, warnings.
```

## Skills

### Purpose
Auto-triggered capabilities based on natural language matching.

### Structure
```
skill-name/
├── SKILL.md           # Main file (< 500 lines)
└── references/
    ├── guide.md       # Detailed documentation
    └── api.md         # API reference
```

### SKILL.md Template
```markdown
---
name: skill-name
description: |
  Brief description with trigger keywords.
  Use when: keyword1, keyword2, keyword3.
  Supports: capability1, capability2.
allowed-tools: Read, Grep
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Skill Title

## Quick Start
Essential instructions...

## Core Workflow
1. Step one
2. Step two

## Resources
- [Detailed Guide](references/guide.md)
- [API Reference](references/api.md)

## Examples
Concrete examples...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars, lowercase+hyphens |
| `description` | Yes | Max 1024 chars, trigger keywords |
| `allowed-tools` | No | Tool restrictions |
| `model` | No | Model override |
| `context` | No | "fork" for isolation |
| `agent` | No | Agent type when forked |
| `hooks` | No | PreToolUse/PostToolUse/Stop only |
| `user-invocable` | No | false to hide from slash menu |

### Progressive Disclosure Pattern
Keep SKILL.md under 500 lines. Put detailed docs in references/.

## Hooks

### Purpose
Lifecycle automation and validation.

### Structure
```
hooks/
├── hooks.json         # Configuration
└── scripts/
    ├── validate.py    # Validation script
    └── format.sh      # Formatting script
```

### hooks.json Template
```json
{
  "description": "Plugin hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

### Event Types

| Event | Matcher | When Fires |
|-------|---------|------------|
| PreToolUse | Tool name | Before tool execution |
| PostToolUse | Tool name | After successful execution |
| PermissionRequest | Tool name | When permission dialog shown |
| Stop | (none) | When Claude attempts to stop |
| SessionStart | Source | At session start |
| SessionEnd | Reason | At session end |

### Script Template (Python)
```python
#!/usr/bin/env python3
import json
import sys

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Validation logic
    if not valid:
        print("Error message", file=sys.stderr)
        sys.exit(2)  # Block

    sys.exit(0)  # Success

if __name__ == "__main__":
    main()
```

## MCP Servers

### Purpose
External tool integration via Model Context Protocol.

### Structure
```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server.js",
      "args": ["--mode", "plugin"],
      "env": {
        "CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

### Key Points
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin paths
- Use `console.error()` for logging (not console.log)
- Secrets via environment variables

## LSP Servers

### Purpose
Language intelligence integration.

### Structure
```json
{
  "lspServers": {
    "python": {
      "command": "pylsp",
      "extensionToLanguage": {
        ".py": "python"
      }
    }
  }
}
```
