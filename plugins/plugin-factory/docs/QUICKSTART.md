# Plugin Factory Quick Start

Get started with Plugin Factory in 5 minutes.

## Prerequisites

- Claude Code CLI installed
- Terminal access

## Step 1: Load Plugin Factory

```bash
# Navigate to plugin-factory directory
cd /path/to/plugin-factory

# Start Claude with plugin
claude --plugin-dir .
```

## Step 2: Create Your First Plugin

```bash
# In Claude session
/plugin-factory:create-plugin my-first-plugin
```

This triggers the orchestrator agent which:
1. Asks clarifying questions about your plugin
2. Researches relevant patterns
3. Creates the plugin structure
4. Validates the output

## Step 3: Understand the Output

Your plugin will have this structure:

```
my-first-plugin/
├── .claude-plugin/
│   └── plugin.json       # Manifest (ONLY file here)
├── commands/             # Entry point commands
├── agents/               # Specialized agents
├── skills/               # Progressive disclosure skills
├── hooks/                # Event hooks
└── README.md             # Documentation
```

## Step 4: Customize Your Plugin

### Add a Skill

```bash
/plugin-factory:create-skill data-processing ./my-first-plugin
```

### Add an Agent

```bash
/plugin-factory:create-agent code-reviewer ./my-first-plugin
```

### Add Hooks

```bash
/plugin-factory:create-hook PreToolUse ./my-first-plugin
```

## Step 5: Validate

```bash
/plugin-factory:validate-plugin ./my-first-plugin
```

Expected output:
```json
{
  "score": 95,
  "grade": "A",
  "gates": {
    "structure": {"passed": true},
    "schema": {"passed": true},
    "components": {"passed": true},
    "quality": {"passed": true},
    "integration": {"passed": true}
  }
}
```

## Step 6: Test Your Plugin

```bash
# Load your new plugin
claude --plugin-dir ./my-first-plugin

# Check commands
/help

# Check agents
/agents
```

## Common Tasks

### Research Patterns

```bash
# Quick research
/plugin-factory:research-patterns skills

# Deep web search
/plugin-factory:research-patterns hooks --deep
```

### Create MCP Server

```bash
/plugin-factory:create-mcp api-client ./my-first-plugin
```

### Package for Distribution

```bash
/plugin-factory:create-marketplace ./my-first-plugin
```

## Troubleshooting

### Plugin Not Loading

Check structure:
```bash
ls .claude-plugin/
# Should show ONLY: plugin.json
```

### Commands Not Appearing

Verify command frontmatter:
```bash
head -10 commands/my-command.md
# Should start with ---
```

### Validation Failures

Run detailed validation:
```bash
/plugin-factory:validate-plugin ./my-first-plugin --verbose
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for design patterns
- Read [HEURISTICS.md](HEURISTICS.md) for quality standards
- Explore the `templates/` directory for examples
