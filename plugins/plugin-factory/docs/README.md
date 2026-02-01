# Plugin Factory

A meta-plugin for Claude Code that generates production-ready plugins with research-driven heuristics, multi-agent orchestration, and progressive disclosure patterns.

## Overview

Plugin Factory automates the creation of Claude Code plugins by:

- **Multi-Agent Orchestration**: 10 specialized agents for different tasks
- **Progressive Disclosure**: Skills < 500 lines with reference documentation
- **Research-Driven Heuristics**: Quality validation based on official patterns
- **Automated Validation**: 5-iteration remediation loop with quality gates

## Installation

```bash
# Clone the plugin
git clone <repository-url>
cd plugin-factory

# Use with Claude Code
claude --plugin-dir .
```

## Quick Start

```bash
# Create a new plugin
/plugin-factory:create-plugin my-awesome-plugin

# Validate an existing plugin
/plugin-factory:validate-plugin ./my-plugin

# Research latest patterns
/plugin-factory:research-patterns hooks --deep
```

## Commands

| Command | Description |
|---------|-------------|
| `create-plugin` | Create complete plugin with agents, skills, hooks |
| `create-skill` | Create progressive disclosure skill |
| `create-agent` | Create specialized subagent |
| `create-hook` | Create event hooks with scripts |
| `create-mcp` | Create MCP server configuration |
| `create-marketplace` | Create marketplace distribution package |
| `validate-plugin` | Run comprehensive validation |
| `research-patterns` | Research latest patterns from docs |

## Agents

| Agent | Purpose | Model |
|-------|---------|-------|
| orchestrator | Master workflow coordination | sonnet |
| clarification | Requirements gathering | haiku |
| researcher | Documentation research | sonnet |
| planner | Architecture design | sonnet |
| skill-builder | Skill creation | sonnet |
| hook-builder | Hook creation | sonnet |
| agent-builder | Agent creation | sonnet |
| mcp-builder | MCP configuration | sonnet |
| validator | Testing & validation | haiku |
| documenter | Documentation generation | sonnet |

## Skills

| Skill | Description |
|-------|-------------|
| plugin-patterns | Core plugin architecture patterns |
| skill-authoring | Skill creation with progressive disclosure |
| hook-engineering | Hook system with 12 event types |
| agent-design | Subagent design and orchestration |
| mcp-integration | MCP server integration patterns |
| heuristics-engine | Quality validation and remediation |

## Quality Gates

Plugin Factory validates plugins through 5 quality gates:

1. **Structure**: Correct directory layout
2. **Schema**: Valid JSON/YAML syntax
3. **Components**: Proper frontmatter
4. **Quality**: Progressive disclosure compliance
5. **Integration**: Loads without errors

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute getting started guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Design decisions and workflows
- [HEURISTICS.md](HEURISTICS.md) - Quality patterns and anti-patterns

## License

MIT

## Author

Plugin Factory <contact@plugin-factory.dev>
