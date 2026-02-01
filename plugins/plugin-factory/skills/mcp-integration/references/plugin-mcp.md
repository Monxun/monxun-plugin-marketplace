# Plugin MCP Patterns

Common patterns for MCP servers in Claude Code plugins.

## Basic Plugin Server

### Structure
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── servers/
│   └── server.js
└── config/
    └── default.json
```

### .mcp.json
```json
{
  "mcpServers": {
    "my-plugin-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}",
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config/default.json"
      }
    }
  }
}
```

### plugin.json
```json
{
  "name": "my-plugin",
  "mcpServers": "./.mcp.json"
}
```

## Database Integration

### SQLite
```json
{
  "mcpServers": {
    "database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/sqlite-server.js",
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data/app.db",
        "READONLY": "true"
      }
    }
  }
}
```

### Server Implementation
```javascript
// servers/sqlite-server.js
import Database from 'better-sqlite3';

const db = new Database(process.env.DB_PATH, {
  readonly: process.env.READONLY === 'true'
});

// Expose query tool
server.tool('query', async ({ sql }) => {
  return db.prepare(sql).all();
});
```

## API Client

### Configuration
```json
{
  "mcpServers": {
    "api-client": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/api-client.js"],
      "env": {
        "API_BASE_URL": "https://api.example.com",
        "API_KEY": "${EXAMPLE_API_KEY}"
      }
    }
  }
}
```

### Server Implementation
```javascript
// servers/api-client.js
const baseUrl = process.env.API_BASE_URL;
const apiKey = process.env.API_KEY;

if (!apiKey) {
  console.error('Error: EXAMPLE_API_KEY required');
  process.exit(1);
}

server.tool('fetch', async ({ endpoint }) => {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  return response.json();
});
```

## File Processor

### Configuration
```json
{
  "mcpServers": {
    "file-processor": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/processor.py"],
      "env": {
        "WORKSPACE": "${CLAUDE_PLUGIN_ROOT}/workspace",
        "ALLOWED_EXTENSIONS": ".txt,.md,.json"
      }
    }
  }
}
```

## OAuth Integration

### Configuration
```json
{
  "mcpServers": {
    "oauth-service": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/oauth-server.js"],
      "env": {
        "CLIENT_ID": "${OAUTH_CLIENT_ID}",
        "CLIENT_SECRET": "${OAUTH_CLIENT_SECRET}",
        "REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

## Multiple Servers

### Configuration
```json
{
  "mcpServers": {
    "database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db.js"
    },
    "api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api.js"
    },
    "cache": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/cache.js"
    }
  }
}
```

### Tool Naming
- `mcp__database__query`
- `mcp__api__fetch`
- `mcp__cache__get`

## Development Pattern

### Dev vs Prod
```json
{
  "mcpServers": {
    "server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "NODE_ENV": "${NODE_ENV:-development}",
        "LOG_LEVEL": "${LOG_LEVEL:-info}"
      }
    }
  }
}
```

### Debug Mode
```json
{
  "mcpServers": {
    "server": {
      "command": "node",
      "args": ["--inspect", "${CLAUDE_PLUGIN_ROOT}/servers/server.js"]
    }
  }
}
```

## Error Handling

### Startup Validation
```javascript
// Validate required config
const required = ['API_KEY', 'DB_PATH'];
const missing = required.filter(k => !process.env[k]);

if (missing.length) {
  console.error(`Missing env vars: ${missing.join(', ')}`);
  process.exit(1);
}
```

### Graceful Shutdown
```javascript
process.on('SIGTERM', () => {
  console.error('Shutting down...');
  // Cleanup resources
  db.close();
  process.exit(0);
});
```

## Testing

### Manual Testing
```bash
# Start server manually
cd plugin-dir
node servers/server.js

# Test with MCP inspector
npx @anthropic/mcp-inspector
```

### Integration Testing
```bash
# Test with Claude
claude --plugin-dir ./my-plugin -p "use my-plugin-server to query data"
```

## Checklist

- [ ] Use `${CLAUDE_PLUGIN_ROOT}` for all paths
- [ ] Document required environment variables
- [ ] Use stderr for logging (not stdout)
- [ ] Handle missing config gracefully
- [ ] Implement graceful shutdown
- [ ] Test tool functionality
