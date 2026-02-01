# MCP Transport Types

Detailed guide to MCP server transport configurations.

## Overview

| Transport | Use Case | Protocol |
|-----------|----------|----------|
| stdio | Local processes | JSON-RPC over stdin/stdout |
| http | Remote servers | JSON-RPC over HTTP |
| sse | Streaming | Server-Sent Events |

## stdio Transport

### Description
Spawns a local process and communicates via stdin/stdout using JSON-RPC.

### Configuration
```json
{
  "mcpServers": {
    "local-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server.js",
      "args": ["--stdio", "--mode", "production"],
      "env": {
        "NODE_ENV": "production"
      },
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Executable path or command |
| `args` | No | Command-line arguments |
| `env` | No | Environment variables |
| `cwd` | No | Working directory |

### Examples

#### Node.js Server
```json
{
  "mcpServers": {
    "node-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

#### Python Server
```json
{
  "mcpServers": {
    "python-server": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.py"],
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}"
      }
    }
  }
}
```

#### NPX Package
```json
{
  "mcpServers": {
    "npm-server": {
      "command": "npx",
      "args": ["@company/mcp-server", "--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

### Important Notes

1. **stdout is for JSON-RPC only**
   ```javascript
   // WRONG
   console.log("Debug info");

   // CORRECT
   console.error("Debug info");
   ```

2. **Process must stay running**
   - Server should not exit immediately
   - Handle SIGTERM gracefully

3. **Path considerations**
   - Use `${CLAUDE_PLUGIN_ROOT}` for portability
   - Avoid absolute paths

## HTTP Transport

### Description
Connects to a remote HTTP server using JSON-RPC over HTTP.

### Configuration
```json
{
  "mcpServers": {
    "http-server": {
      "url": "http://localhost:3000",
      "transport": "http",
      "env": {
        "AUTH_TOKEN": "${API_TOKEN}"
      }
    }
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | Server URL |
| `transport` | Yes | Must be "http" |
| `env` | No | Environment variables |

### Examples

#### Local API Server
```json
{
  "mcpServers": {
    "local-api": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

#### Remote Server with Auth
```json
{
  "mcpServers": {
    "remote-api": {
      "url": "https://api.example.com/mcp",
      "transport": "http",
      "env": {
        "AUTHORIZATION": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### Security Considerations

- Use HTTPS for production
- Never hardcode tokens
- Validate server certificates

## SSE Transport

### Description
Connects using Server-Sent Events for real-time streaming.

### Configuration
```json
{
  "mcpServers": {
    "sse-server": {
      "url": "http://localhost:3000/sse",
      "transport": "sse"
    }
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | SSE endpoint URL |
| `transport` | Yes | Must be "sse" |
| `env` | No | Environment variables |

### Use Cases

- Real-time data updates
- Long-running operations
- Event streaming

## Choosing a Transport

| Scenario | Recommended |
|----------|-------------|
| Local tool | stdio |
| Remote API | http |
| Real-time streaming | sse |
| Package from npm | stdio (via npx) |
| Self-hosted service | http or sse |

## Multiple Transports

Configure multiple servers:

```json
{
  "mcpServers": {
    "local-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/tools.js"
    },
    "remote-api": {
      "url": "https://api.example.com/mcp",
      "transport": "http"
    },
    "live-data": {
      "url": "https://stream.example.com/sse",
      "transport": "sse"
    }
  }
}
```
