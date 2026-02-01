# MCP Protocol Specification for Unity

## JSON-RPC 2.0 Protocol

The Unity MCP server uses JSON-RPC 2.0 over HTTP transport.

### Base URL

```
http://localhost:8080
```

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "<method-name>",
  "params": { ... },
  "id": <integer>
}
```

### Response Format (Success)

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Operation result message"
      }
    ]
  },
  "id": <integer>
}
```

### Response Format (Error)

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": { "details": "..." }
  },
  "id": <integer>
}
```

## Standard MCP Methods

### tools/list

Discover available tools on the server.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "create-vr-interactable",
        "description": "Create a VR interactable GameObject",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": { "type": "string", "description": "Object name" },
            "position": { "type": "string", "description": "Position x,y,z" }
          },
          "required": ["name"]
        }
      }
    ]
  },
  "id": 1
}
```

### tools/call

Invoke a specific tool.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-vr-interactable",
    "arguments": {
      "name": "GrabbableSphere",
      "position": "0,1.2,0"
    }
  },
  "id": 2
}
```

### resources/list

List available resources (scenes, assets, project info).

```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "id": 3
}
```

### resources/read

Read a specific resource.

```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "unity://scene/active"
  },
  "id": 4
}
```

## Error Codes

| Code | Meaning | Common Cause |
|------|---------|-------------|
| -32700 | Parse error | Malformed JSON |
| -32600 | Invalid request | Missing jsonrpc or method |
| -32601 | Method not found | Tool not registered |
| -32602 | Invalid params | Wrong argument types |
| -32603 | Internal error | Unity API exception |
| -32000 | Server error | MCP server not ready |

## Tool Registration

Tools are registered via the `[McpPluginTool]` attribute in C#. The server auto-discovers all decorated methods at startup and after assembly reload.

### Attribute Parameters

```csharp
[McpPluginTool(
    "tool-name",           // Unique identifier (kebab-case)
    Title = "Display Name", // Human-readable name
    Destructive = false,    // Marks destructive operations
    ReadOnly = true         // Marks read-only operations
)]
```

### Parameter Attributes

```csharp
public string MyTool(
    [Description("Parameter description")] string required,
    [Description("Optional param")] string optional = "default"
)
```

## Communication Flow

```
1. Claude Code sends JSON-RPC request via HTTP POST
2. Unity MCP server receives on background thread
3. Server parses JSON-RPC, validates method and params
4. Tool implementation wraps Unity calls in MainThread.Instance.Run()
5. Main thread executes Unity API operations on next Update()
6. Result marshalled back to background thread
7. JSON-RPC response sent to Claude Code
```

## Health Check

```bash
curl -s http://localhost:8080/health
```

Expected response:

```json
{
  "status": "ok",
  "unity_version": "2022.3.20f1",
  "tools_count": 15,
  "uptime_seconds": 120
}
```

## Rate Limiting

The server processes requests sequentially on Unity's main thread. Rapid-fire requests queue in the dispatcher. For batch operations, prefer single tools that operate on collections rather than individual object calls.
