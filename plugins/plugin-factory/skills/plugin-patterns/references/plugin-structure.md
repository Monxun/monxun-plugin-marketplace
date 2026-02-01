# Plugin Structure Reference

Complete guide to Claude Code plugin directory structure and organization.

## Directory Layout

```
plugin-name/
├── .claude-plugin/                 # Manifest directory
│   └── plugin.json                 # ONLY file allowed here
│
├── commands/                       # Slash commands
│   ├── main-command.md            # Primary entry point
│   ├── secondary-command.md       # Additional commands
│   └── utility-command.md
│
├── agents/                         # Custom subagents
│   ├── specialist-agent.md        # Domain expert
│   ├── validator-agent.md         # Testing specialist
│   └── coordinator-agent.md       # Orchestration
│
├── skills/                         # Auto-triggered capabilities
│   ├── primary-skill/
│   │   ├── SKILL.md               # Main skill file
│   │   ├── references/            # Detailed documentation
│   │   │   ├── guide.md
│   │   │   └── api.md
│   │   └── scripts/               # Utility scripts
│   │       └── helper.py
│   └── secondary-skill/
│       └── SKILL.md
│
├── hooks/                          # Lifecycle automation
│   ├── hooks.json                 # Hook configuration
│   └── scripts/                   # Hook scripts
│       ├── validate.py
│       └── format.sh
│
├── templates/                      # Optional: reusable templates
│   └── component.template
│
├── schemas/                        # Optional: validation schemas
│   └── config.schema.json
│
├── .mcp.json                       # Optional: MCP servers
├── .lsp.json                       # Optional: LSP servers
│
└── docs/                           # Documentation
    ├── README.md
    └── QUICKSTART.md
```

## Component Locations

| Component | Location | File Pattern |
|-----------|----------|--------------|
| Manifest | `.claude-plugin/` | `plugin.json` |
| Commands | `commands/` | `*.md` |
| Agents | `agents/` | `*.md` |
| Skills | `skills/*/` | `SKILL.md` |
| Hooks | `hooks/` | `hooks.json` |
| Hook Scripts | `hooks/scripts/` | `*.sh`, `*.py` |
| MCP Config | Root | `.mcp.json` |
| LSP Config | Root | `.lsp.json` |

## Path References in plugin.json

### String Paths
```json
{
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/"
}
```

### Array Paths (Multiple Locations)
```json
{
  "commands": ["./commands/", "./extra-commands/"],
  "skills": ["./skills/", "./contrib-skills/"]
}
```

### Inline Configuration
```json
{
  "hooks": {
    "PreToolUse": [...]
  }
}
```

## Critical Rules

### Rule 1: .claude-plugin/ Contents
ONLY `plugin.json` may exist in `.claude-plugin/` directory.

❌ **Never do this:**
```
.claude-plugin/
├── plugin.json
├── commands/    # WRONG
└── agents/      # WRONG
```

### Rule 2: Paths Are Relative
All paths in plugin.json are relative to plugin root.

```json
{
  "commands": "./commands/",     // Correct
  "commands": "/abs/path/",      // Avoid
}
```

### Rule 3: Supplementary Behavior
Custom paths supplement default directories, they don't replace them.

## File Discovery

Claude Code discovers components by:
1. Reading plugin.json paths
2. Scanning specified directories
3. Loading all matching files

### Command Discovery
```
commands/*.md → Available as /plugin-name:command-name
```

### Agent Discovery
```
agents/*.md → Available for delegation
```

### Skill Discovery
```
skills/*/SKILL.md → Auto-triggered by description keywords
```

## Nested Skills Structure

Skills support progressive disclosure:

```
skills/
└── my-skill/
    ├── SKILL.md           # Core instructions (< 500 lines)
    ├── references/
    │   ├── guide.md       # Extended documentation
    │   ├── api.md         # API reference
    │   └── examples.md    # Usage examples
    └── scripts/
        └── utility.py     # Helper scripts
```

Reference files from SKILL.md:
```markdown
For complete API documentation, see [API Reference](references/api.md).
```

## Optional Directories

### templates/
Store reusable file templates for generation tasks.

### schemas/
Store JSON schemas for validation.

### docs/
Store user-facing documentation.

## Validation

Check structure is correct:
```bash
# Only plugin.json in .claude-plugin/
ls .claude-plugin/
# Expected output: plugin.json

# No directories in .claude-plugin/
find .claude-plugin -type d -mindepth 1
# Expected output: (empty)

# Components at root
ls -d commands/ agents/ skills/ hooks/ 2>/dev/null
```
