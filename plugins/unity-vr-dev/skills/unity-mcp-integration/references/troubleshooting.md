# MCP Integration Troubleshooting

## Connection Issues

### Server Not Responding

**Symptoms**: `curl: (7) Failed to connect to localhost port 8080`

**Checklist**:
1. Unity Editor is running with the project open
2. MCP server package is installed (Window > Package Manager)
3. MCP server is enabled in Unity preferences
4. No other process is using port 8080

```bash
# Check if port is in use
lsof -i :8080

# Check Unity process is running
ps aux | grep Unity
```

### Connection Refused on WSL2

**Symptoms**: Works from Windows, fails from WSL2

**Fix for mirrored mode** (Windows 11 22H2+):
```ini
# %USERPROFILE%/.wslconfig
[wsl2]
networkingMode=mirrored
```

**Fix for NAT mode**:
```bash
# Forward port from Windows to WSL2
netsh interface portproxy add v4tov4 \
  listenport=8080 listenaddress=0.0.0.0 \
  connectport=8080 connectaddress=$(wsl hostname -I)
```

### Tool Not Found

**Symptoms**: `{"error":{"code":-32601,"message":"Method not found"}}`

**Causes**:
- Tool class missing `[McpPluginToolType]` attribute
- Tool method missing `[McpPluginTool]` attribute
- Assembly not compiled (check Console for errors)
- Assembly reload needed after adding new tools

**Fix**: Trigger assembly reload in Unity (Ctrl+R or Assets > Refresh).

## Thread Safety Errors

### InvalidOperationException: Can only be called from the main thread

**Cause**: Unity API called directly from MCP HTTP handler thread.

**Fix**: Wrap all Unity calls:
```csharp
return MainThread.Instance.Run(() => {
    // Unity API calls here
});
```

### Deadlock on MainThread.Instance.Run()

**Cause**: Nested MainThread.Run() calls or calling from main thread.

**Fix**: Check if already on main thread:
```csharp
if (Thread.CurrentThread.ManagedThreadId == 1) {
    // Already on main thread, call directly
    return DoUnityWork();
} else {
    return MainThread.Instance.Run(() => DoUnityWork());
}
```

## Build-Related Issues

### gRPC Linking Errors

**Symptoms**: `undefined symbol: grpcsharp_init` during IL2CPP build

**Cause**: gRPC native library not compatible with IL2CPP ARM64.

**Resolution**: This is a hard constraint. Do NOT use gRPC. Use HTTP or WebSocket alternatives:
- REST API via UnityWebRequest
- WebSocket via NativeWebSocket
- HTTP polling for real-time updates

### IL2CPP Stripping

**Symptoms**: MCP tools missing at runtime, reflection failures

**Cause**: IL2CPP code stripping removes "unused" code including reflection targets.

**Fix**: Add `link.xml` to preserve assemblies:
```xml
<linker>
  <assembly fullname="MCP.Server" preserve="all"/>
  <assembly fullname="YourToolsAssembly" preserve="all"/>
</linker>
```

## Performance Issues

### Slow Tool Response

**Cause**: Main thread dispatcher processes one request per Update() frame.

**Mitigation**:
- Batch operations into single tool calls
- Use async tool variants for long operations
- Avoid querying individual objects; request collections

### Memory Pressure

**Cause**: Large scene serialization or asset operations via MCP.

**Mitigation**:
- Limit scene hierarchy depth in responses
- Use pagination for large asset lists
- Clear undo history after batch operations: `Undo.ClearAll()`

## Quest Device Issues

### ADB Device Not Found

```bash
# List connected devices
adb devices

# Restart ADB server
adb kill-server && adb start-server

# Enable developer mode on Quest
# Settings > System > Developer > USB Connection Dialog: Enabled
```

### Wireless ADB Disconnects

```bash
# Initial setup (USB connected)
adb tcpip 5555
adb connect <device-ip>:5555

# Reconnect after disconnect
adb connect <device-ip>:5555
```

**Note**: Device IP changes on network reconnect. Query current IP:
```bash
adb shell ip addr show wlan0 | grep "inet "
```

## Diagnostic Commands

```bash
# Full diagnostic check
echo "=== MCP Server ===" && \
curl -s http://localhost:8080/health && \
echo "\n=== ADB Devices ===" && \
adb devices && \
echo "\n=== Unity Process ===" && \
ps aux | grep -i unity | grep -v grep
```
