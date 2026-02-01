---
name: mcp-integration
description: |
  Expert guidance for MCP (Model Context Protocol) server integration.
  Use when: MCP servers, external tools, .mcp.json, transport types,
  model context protocol, "create MCP", "add MCP server", MCP config.
  Supports: stdio, http, sse transports, environment variables.
allowed-tools: Read, Write, Edit, Bash
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# MCP Integration Skill

Configure MCP (Model Context Protocol) servers for external tool integration in Claude Code plugins.

## .mcp.json Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server.js",
      "args": ["--option", "value"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Transport Types

### stdio (Default)
Local process communication:

```json
{
  "mcpServers": {
    "local-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server.js",
      "args": ["--stdio"]
    }
  }
}
```

### HTTP
Remote server via HTTP:

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "http://localhost:3000",
      "transport": "http"
    }
  }
}
```

### SSE (Server-Sent Events)
Streaming connection:

```json
{
  "mcpServers": {
    "streaming-server": {
      "url": "http://localhost:3000/sse",
      "transport": "sse"
    }
  }
}
```

## Configuration Options

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes (stdio) | Executable path |
| `url` | Yes (http/sse) | Server URL |
| `transport` | No | Type: stdio/http/sse |
| `args` | No | Command arguments |
| `env` | No | Environment variables |
| `cwd` | No | Working directory |

## Path Variables

Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server.js",
      "env": {
        "CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## NPX Servers

```json
{
  "mcpServers": {
    "npm-server": {
      "command": "npx",
      "args": ["@company/mcp-server"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

## Critical: stdout vs stderr

**ALWAYS use console.error() for logging:**

```javascript
// WRONG - corrupts JSON-RPC
console.log("Debug message");

// CORRECT
console.error("Debug message");
```

## Tool Naming

MCP tools appear as `mcp__<server>__<tool>`:
- `mcp__database__query`
- `mcp__api__fetch`

## Detailed References

- [Transport Types](references/transport-types.md)
- [Scope Management](references/scope-management.md)
- [Plugin MCP Patterns](references/plugin-mcp.md)

## Best Practices

- Always use `${CLAUDE_PLUGIN_ROOT}`
- Never hardcode secrets
- Use stderr for logging
- Document required env vars
