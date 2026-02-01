---
name: research-patterns
description: Research latest Claude Code patterns from documentation and community
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
argument-validation: optional
---

# Research Patterns Command

Gather latest patterns from official docs and community sources.

## Usage

```
/plugin-factory:research-patterns <topic> [--deep]
```

## Arguments

- `$1` - Research topic (plugins, skills, hooks, agents, mcp)
- `--deep` - Enable comprehensive web search

## Workflow

Delegates to `researcher` agent which:

1. Searches official Claude Code documentation
2. Queries web for community patterns (if --deep)
3. Cross-references with existing plugin patterns
4. Extracts best practices
5. Returns structured findings

## Injected Skills

- `plugin-patterns` - Core patterns reference
- `skill-authoring` - Skill patterns
- `hook-engineering` - Hook patterns
- `agent-design` - Agent patterns
- `mcp-integration` - MCP patterns

## Research Topics

| Topic | Sources |
|-------|---------|
| plugins | Plugin reference, create-plugins guide |
| skills | Agent skills guide, best practices |
| hooks | Hooks reference, event types |
| agents | Subagents guide, orchestration |
| mcp | MCP protocol, server patterns |

## Example

```bash
# Research plugin patterns
/plugin-factory:research-patterns plugins

# Deep research on hooks
/plugin-factory:research-patterns hooks --deep
```

## Output

Returns:
- Official documentation findings
- Community patterns (if --deep)
- Best practices summary
- Anti-patterns to avoid
- Example implementations
