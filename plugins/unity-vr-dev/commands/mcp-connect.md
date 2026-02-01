---
name: mcp-connect
description: Connect to and verify Unity MCP server for VR development
allowed-tools: Read, Bash, Grep, Glob
argument-validation: optional
---

# Connect Unity MCP

Establish and verify connection to the Unity MCP server.

## Usage

```
/unity-vr-dev:mcp-connect [url]
```

## Arguments

- `url` — MCP server URL (defaults to `http://localhost:8080`)

## Workflow

1. Delegate to **orchestrator** agent
2. Test HTTP connectivity to MCP server
3. Query health endpoint for server status
4. Call `tools/list` to discover available tools
5. Report connection status and tool catalog

## Prerequisites

- Unity Editor running with project open
- Unity-MCP package installed and server enabled
- Port 8080 available (or custom port specified)

## Output

Reports:
- Connection status (connected/failed)
- Unity version detected
- Number of available tools
- Tool catalog with names and descriptions

## Examples

```
/unity-vr-dev:mcp-connect
/unity-vr-dev:mcp-connect http://localhost:9090
```
