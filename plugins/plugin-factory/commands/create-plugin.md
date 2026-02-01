---
name: create-plugin
description: Create a complete Claude Code plugin with agents, skills, hooks, and MCP integration
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebSearch
argument-validation: optional
---

# Create Plugin Command

Generate a production-ready Claude Code plugin with multi-agent orchestration.

## Usage

```
/plugin-factory:create-plugin <plugin-name> [options]
```

## Arguments

- `$1` - Plugin name (kebab-case, required)
- `$ARGUMENTS` - Full argument string for additional options

## Workflow

This command delegates to the `orchestrator` agent which coordinates:

1. **Discovery Phase** - Requirements gathering via `clarification` agent
2. **Research Phase** - Pattern validation via `researcher` agent
3. **Architecture Phase** - Design planning via `planner` agent
4. **Construction Phase** - Building via specialist agents
5. **Verification Phase** - Validation via `validator` agent
6. **Delivery Phase** - Documentation via `documenter` agent

## Injected Skills

- `plugin-patterns` - Core plugin architecture
- `heuristics-engine` - Quality validation

## Example

```bash
# Create a new plugin
/plugin-factory:create-plugin my-awesome-plugin

# Create with specific features
/plugin-factory:create-plugin api-client --with-mcp --with-hooks
```

## Next Steps

After creation, validate with:
```bash
/plugin-factory:validate-plugin ./my-awesome-plugin
```
