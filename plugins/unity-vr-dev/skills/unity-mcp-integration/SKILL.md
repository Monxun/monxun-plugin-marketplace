---
name: unity-mcp-integration
description: |
  Unity MCP server integration for Claude Code VR development.
  Use when: connecting to Unity Editor, MCP server setup, JSON-RPC tools,
  scene manipulation, VR component creation, "MCP connect", "Unity tools",
  McpPluginTool, main thread dispatcher, tool discovery, tool catalog.
  Supports: HTTP transport, tool registration, thread safety, XR components.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Unity MCP Integration

Configure and manage Model Context Protocol connections between Claude Code and Unity Editor for VR development.

## Architecture

```
Claude Code → MCP Protocol (JSON-RPC 2.0) → Unity MCP Server (HTTP :8080)
  → Main Thread Dispatcher → Unity APIs
```

**Transport**: HTTP on localhost:8080 (no gRPC — IL2CPP ARM64 linking errors)

## MCP Server Setup

### Prerequisites

- Unity 2022.3 LTS or later (through Unity 6)
- Meta XR SDK v74+
- Unity-MCP package installed via Package Manager

### Server Configuration

The MCP server runs inside Unity Editor, exposing tools via JSON-RPC 2.0 over HTTP:

```
Server URL: http://localhost:8080
Protocol: JSON-RPC 2.0
Threading: MainThread.Instance.Run() wrapper required for all Unity API calls
Discovery: Auto-registration via [McpPluginTool] attribute
```

### Connection Verification

```bash
# Test MCP server is responding
curl -s http://localhost:8080/health

# List available tools
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Tool Categories

| Category | Tools | Unity APIs |
|----------|-------|-----------|
| Scene Operations | create-object, add-component, set-transform | EditorSceneManager, GameObject |
| Asset Management | import-asset, create-prefab, build-bundle | AssetDatabase, PrefabUtility |
| Build Pipeline | build-quest-apk, deploy-to-device | BuildPipeline, BuildPlayerOptions |
| VR Components | create-vr-interactable, add-socket, configure-grab | XRGrabInteractable, XRSocketInteractor |
| Test Execution | run-tests, run-performance-test | TestRunnerApi, Measure.Frames |

## Tool Registration Pattern

Custom tools use the `[McpPluginTool]` attribute for auto-discovery:

```csharp
[McpPluginToolType]
public class Tool_SceneControl {
    [McpPluginTool("create-vr-interactable", Title = "Create VR Interactable")]
    public string CreateInteractable(
        [Description("Object name")] string name,
        [Description("Position x,y,z")] string position = "0,0,0"
    ) {
        return MainThread.Instance.Run(() => {
            var go = new GameObject(name);
            go.AddComponent<XRGrabInteractable>();
            go.AddComponent<Rigidbody>();
            // Parse and apply position
            var parts = position.Split(',');
            go.transform.position = new Vector3(
                float.Parse(parts[0]),
                float.Parse(parts[1]),
                float.Parse(parts[2])
            );
            return $"[Success] Created interactable '{go.name}' at ({position})";
        });
    }
}
```

### Critical: Thread Safety

**All Unity API calls MUST go through MainThread.Instance.Run().**

The MCP server handles HTTP requests on background threads. Unity APIs are main-thread-only. The dispatcher queues operations to execute on the next Update() cycle.

## JSON-RPC Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-vr-interactable",
    "arguments": {
      "name": "GrabbableCube",
      "position": "0,1.5,0"
    }
  },
  "id": 1
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[Success] Created interactable 'GrabbableCube' at (0,1.5,0)"
      }
    ]
  },
  "id": 1
}
```

## Common Workflows

### Create VR Scene Element

1. Call `create-object` to instantiate GameObject
2. Call `add-component` to attach XR Interaction Toolkit components
3. Call `set-transform` to position in scene
4. Call `create-prefab` to save as reusable asset

### Build and Deploy

1. Call `build-quest-apk` with IL2CPP/ARM64 settings
2. Monitor build progress via server status endpoint
3. Call `deploy-to-device` to install and launch on Quest

## Troubleshooting

For detailed troubleshooting, see `references/troubleshooting.md`.

Common issues:
- **Server not responding**: Verify Unity Editor is running and MCP package is installed
- **Thread exceptions**: Ensure all Unity API calls use MainThread dispatcher
- **Tool not found**: Check [McpPluginTool] attribute and assembly reload
- **Connection refused**: Check port 8080 availability and firewall settings
- **gRPC errors**: gRPC is not viable on Quest 2 — use HTTP/WebSocket only

## References

- `references/unity-api-reference.md` — Full Unity API patterns for MCP tools
- `references/mcp-protocol-spec.md` — JSON-RPC 2.0 protocol details
- `references/troubleshooting.md` — Connection and runtime troubleshooting
