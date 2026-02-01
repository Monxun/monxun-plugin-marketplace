---
name: debug-orchestration
description: |
  Quest debugging and profiling tool orchestration.
  Use when: debugging VR apps, LogCat streaming, GPU profiling,
  ovrgpuprofiler, scrcpy mirroring, MQDH integration, crash analysis,
  "show logs", "debug session", "profile GPU", "screen mirror",
  Immersive Debugger, DebugMember, performance analysis.
  Supports: ADB tools, Meta Quest Developer Hub, wireless debug.
allowed-tools: Read, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Debug Orchestration

Coordinate Quest debugging and profiling tools: LogCat, ovrgpuprofiler, scrcpy, MQDH, and Immersive Debugger.

## Debug Tool Stack

| Tool | Purpose | Requires |
|------|---------|----------|
| ADB LogCat | Real-time log streaming | ADB + device |
| ovrgpuprofiler | GPU performance traces | ADB + device |
| scrcpy | Screen mirroring | ADB + scrcpy installed |
| MQDH | All-in-one device management | MQDH v3.4+ |
| Immersive Debugger | In-headset variable inspection | Meta XR SDK v74+ |

## LogCat Streaming

### Filtered Log Command

```bash
# Unity and VR-specific tags
adb logcat -s Unity,VrApi,XrPerformanceManager,ActivityManager,PackageManager,dalvikvm,DEBUG
```

### Common Filter Patterns

```bash
# Errors only
adb logcat -s Unity:E,VrApi:E

# Unity logs with timestamps
adb logcat -v time -s Unity

# Search for specific message
adb logcat -s Unity | grep -i "exception\|error\|null"

# Clear and restart
adb logcat -c && adb logcat -s Unity
```

### Log Severity Levels

| Level | Flag | Use |
|-------|------|-----|
| Verbose | V | All messages |
| Debug | D | Debug messages |
| Info | I | Informational |
| Warning | W | Warnings |
| Error | E | Errors only |
| Fatal | F | Fatal errors |

See `references/logcat-filtering.md` for advanced filtering patterns.

## GPU Profiling with ovrgpuprofiler

Built into Quest runtime — no installation needed.

### Basic Workflow

```bash
# 1. Enable profiler
adb shell ovrgpuprofiler -e

# 2. Capture 2-second trace
adb shell ovrgpuprofiler --trace=2

# 3. Disable profiler
adb shell ovrgpuprofiler -d
```

### Real-Time Metrics

```bash
# Show real-time GPU metrics (max 30 simultaneous)
adb shell ovrgpuprofiler -m

# List available metrics
adb shell ovrgpuprofiler -l
```

### Key Metrics

| Metric | Target | Meaning |
|--------|--------|---------|
| GPU Time | <11.1ms | Total GPU frame time (90 FPS budget) |
| Vertex Processing | <4ms | Geometry processing |
| Fragment Processing | <7ms | Pixel shading |
| Tiler Utilization | <80% | Tile-based rendering load |

See `references/ovrgpuprofiler-guide.md` for trace analysis.

## scrcpy Screen Mirroring

### Optimized Quest Settings

```bash
# Recommended settings for Quest
scrcpy -b 30M --crop 1440:1540:60:60

# With audio forwarding
scrcpy -b 30M --crop 1440:1540:60:60 --audio-codec=opus

# Record session
scrcpy -b 30M --crop 1440:1540:60:60 --record=session.mp4
```

### Known Issues

**Quest OS v74+ black screen**: Some scrcpy versions have regressions with recent Quest firmware. Verify compatibility with your Quest OS version and scrcpy version.

Workaround: Use MQDH screen capture instead.

## Meta Quest Developer Hub (MQDH)

### Detection

```bash
# Check if MQDH is running
pgrep -f "Meta Quest Developer Hub" || echo "MQDH not running"
```

### Capabilities

- Device management and monitoring
- Log viewing with filtering
- Screenshot and video capture
- APK drag-and-drop installation
- VRC FPS tracking
- GPU trace commands
- Performance overlay

When MQDH is available, prefer it over individual ADB commands for a unified experience.

See `references/mqdh-integration.md` for API integration.

## Immersive Debugger (Meta XR SDK v74+)

### Setup

Enable in Unity: `Meta XR > Immersive Debugger > Enable`

### DebugMember Attribute

```csharp
using Meta.XR.ImmersiveDebugger;

public class PlayerController : MonoBehaviour {
    [DebugMember(Tweakable = true, Category = "Player", Min = 0, Max = 100)]
    public float health = 100f;

    [DebugMember(Category = "Movement")]
    public Vector3 velocity;

    [DebugMember(Tweakable = true, Category = "Settings", Min = 1, Max = 10)]
    public float moveSpeed = 5f;
}
```

### Attribute Parameters

| Parameter | Type | Description |
|-----------|------|------------|
| Tweakable | bool | Enable slider editing in headset |
| Category | string | Group name in debug panel |
| Min | float | Minimum slider value |
| Max | float | Maximum slider value |
| GizmoType | enum | 3D visualization type |

## Wireless ADB Setup

```bash
# With USB connected:
adb tcpip 5555

# Disconnect USB, then:
adb connect <quest-ip>:5555

# Verify
adb devices
```

**Note**: Quest IP changes on network reconnect. Get current IP:
```bash
adb shell ip addr show wlan0 | grep "inet "
```

## Debug Session Checklist

1. Verify ADB connection
2. Clear old logs (`adb logcat -c`)
3. Start LogCat with appropriate filters
4. Enable GPU profiler if performance investigation
5. Start scrcpy or MQDH for visual monitoring
6. Launch application on device
7. Monitor and capture relevant data

## References

- `references/logcat-filtering.md` — Advanced LogCat filter patterns
- `references/ovrgpuprofiler-guide.md` — GPU profiler trace analysis
- `references/mqdh-integration.md` — MQDH setup and API usage
