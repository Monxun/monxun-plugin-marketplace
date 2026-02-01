---
name: create-mcp
description: Create MCP server configuration for external tool integration
allowed-tools: Read, Write, Edit, Bash, Glob
argument-validation: optional
---

# Create MCP Command

Generate .mcp.json configuration for Model Context Protocol servers.

## Usage

```
/plugin-factory:create-mcp <server-name> [target-plugin]
```

## Arguments

- `$1` - Server name (required)
- `$2` - Target plugin directory (optional)

## Workflow

Delegates to `mcp-builder` agent which:

1. Determines server type (stdio, SSE, HTTP)
2. Creates .mcp.json configuration
3. Sets up environment variables
4. Creates server scaffold (if needed)
5. Updates plugin.json reference

## Injected Skills

- `mcp-integration` - Transport types, scope management, plugin patterns

## Configuration Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}",
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

## Server Types

| Type | Transport | Use Case |
|------|-----------|----------|
| stdio | stdin/stdout | Local servers |
| SSE | HTTP events | Streaming |
| HTTP | REST | Remote APIs |

## Example

```bash
# Create a database MCP server
/plugin-factory:create-mcp database-server

# Create API client server
/plugin-factory:create-mcp api-client ./my-plugin
```

## Best Practices

- Use `${CLAUDE_PLUGIN_ROOT}` for all paths
- Document required environment variables
- Use stderr for logging (not stdout)
