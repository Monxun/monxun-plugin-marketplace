# MCP Scope Management

Managing MCP server configuration across different scopes.

## Configuration Scopes

| Scope | Location | Priority | Visibility |
|-------|----------|----------|------------|
| User | `~/.claude/settings.json` | 3 | All projects |
| Project | `.claude/settings.json` | 2 | Current project |
| Plugin | `.mcp.json` in plugin | 1 | Where plugin enabled |

## Plugin MCP Configuration

### Location
Place `.mcp.json` at plugin root:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json          # MCP configuration
└── servers/
    └── server.js
```

### Path Resolution
Use `${CLAUDE_PLUGIN_ROOT}`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server.js"
    }
  }
}
```

### Plugin Manifest Reference

In `plugin.json`:
```json
{
  "name": "my-plugin",
  "mcpServers": "./.mcp.json"
}
```

Or inline:
```json
{
  "name": "my-plugin",
  "mcpServers": {
    "mcpServers": {
      "my-server": {
        "command": "${CLAUDE_PLUGIN_ROOT}/server.js"
      }
    }
  }
}
```

## Environment Variables

### Plugin Variables
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory path

### User Variables
Reference system env vars:
```json
{
  "mcpServers": {
    "api-server": {
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "SECRET": "${MY_SECRET}"
      }
    }
  }
}
```

### Required Variables
Document in README:
```markdown
## Required Environment Variables

| Variable | Description |
|----------|-------------|
| `MY_API_KEY` | API key for service |
| `MY_SECRET` | Secret token |
```

## Server Isolation

### Per-Plugin Servers
Each plugin can have its own MCP servers:

```
plugin-a/
└── .mcp.json  → server-a

plugin-b/
└── .mcp.json  → server-b
```

### Tool Namespacing
Tools are namespaced by server:
- `mcp__server-a__tool1`
- `mcp__server-b__tool1`

No conflicts even with same tool names.

## Scope Precedence

When same server name in multiple scopes:

1. **User scope** - Lowest priority
2. **Project scope** - Medium priority
3. **Plugin scope** - Highest priority

Plugin config overrides user/project config.

## Enabling/Disabling

### Disable in Settings
```json
{
  "mcpServers": {
    "server-name": {
      "disabled": true
    }
  }
}
```

### Per-Project Override
In `.claude/settings.json`:
```json
{
  "mcpServers": {
    "plugin-server": {
      "disabled": true
    }
  }
}
```

## Best Practices

### 1. Use Plugin Scope
Keep MCP config in plugin for portability.

### 2. Document Dependencies
List required env vars and setup steps.

### 3. Provide Defaults
Use sensible defaults, allow overrides:
```json
{
  "mcpServers": {
    "api": {
      "env": {
        "TIMEOUT": "${MCP_TIMEOUT:-30000}"
      }
    }
  }
}
```

### 4. Validate Configuration
Check required vars on startup:
```javascript
if (!process.env.API_KEY) {
  console.error("Error: API_KEY required");
  process.exit(1);
}
```

### 5. Graceful Degradation
Handle missing servers gracefully in plugin logic.
