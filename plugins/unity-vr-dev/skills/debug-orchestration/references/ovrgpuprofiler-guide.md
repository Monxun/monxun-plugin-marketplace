# ovrgpuprofiler Guide

## Overview

`ovrgpuprofiler` is built into the Quest runtime. No installation needed — works through ADB shell commands.

## Basic Commands

### Enable/Disable

```bash
# Enable profiler
adb shell ovrgpuprofiler -e

# Disable profiler
adb shell ovrgpuprofiler -d
```

### Capture Trace

```bash
# 2-second trace (default)
adb shell ovrgpuprofiler --trace=2

# 5-second trace
adb shell ovrgpuprofiler --trace=5

# 10-second trace (maximum recommended)
adb shell ovrgpuprofiler --trace=10
```

### Real-Time Metrics

```bash
# Show real-time metrics
adb shell ovrgpuprofiler -m

# List available metrics
adb shell ovrgpuprofiler -l
```

## Key Performance Metrics

### Frame Budget (90 FPS)

| Metric | Budget | Alert Threshold |
|--------|--------|----------------|
| Total GPU Time | 11.1ms | >10ms |
| Vertex Processing | ~4ms | >5ms |
| Fragment Processing | ~7ms | >8ms |
| Tiler Utilization | <80% | >85% |

### Identifying Bottlenecks

**GPU-bound**: Total GPU time > 11.1ms
- Check fragment shader complexity
- Reduce overdraw
- Lower texture resolution
- Simplify post-processing

**CPU-bound**: GPU time < 11.1ms but frame drops
- Check `XR.WaitForGPU` profiler marker in Unity Profiler
- Optimize C# code, reduce GC allocations
- Batch draw calls

## Trace Analysis

### Reading Trace Output

```
Frame 0001: GPU=8.2ms  Vert=2.1ms  Frag=5.8ms  Tiler=62%
Frame 0002: GPU=9.1ms  Vert=2.3ms  Frag=6.4ms  Tiler=68%
Frame 0003: GPU=12.5ms Vert=3.8ms  Frag=8.2ms  Tiler=85%  << SPIKE
Frame 0004: GPU=8.4ms  Vert=2.2ms  Frag=5.9ms  Tiler=63%
```

### Spike Detection

Look for frames where:
- GPU time exceeds 11.1ms (frame drop at 90 FPS)
- Tiler utilization exceeds 85% (geometry bottleneck)
- Fragment time dominates (overdraw/shader complexity)
- Vertex time spikes (complex geometry or vertex shaders)

## Optimization Workflows

### Overdraw Investigation

1. Enable profiler: `adb shell ovrgpuprofiler -e`
2. Capture trace during suspect scene: `adb shell ovrgpuprofiler --trace=5`
3. Look for high fragment processing time relative to vertex
4. In Unity: enable Overdraw visualization mode
5. Reduce transparent objects, particle systems, UI layers

### Geometry Optimization

1. Capture trace during camera movement
2. Look for high vertex processing or tiler utilization
3. Check draw call count in Unity Profiler
4. Add LOD groups, reduce polygon counts
5. Enable GPU instancing for repeated objects

### Shader Investigation

1. Capture trace in scene with suspect materials
2. Compare fragment time with simplified shader
3. Profile with Unity's Frame Debugger for draw-by-draw analysis
4. Replace heavy shaders with mobile-optimized variants

## Automation Script

```bash
#!/bin/bash
# Capture GPU profile and save report

echo "Starting GPU profiler..."
adb shell ovrgpuprofiler -e
sleep 1

echo "Capturing 5-second trace..."
TRACE=$(adb shell ovrgpuprofiler --trace=5)

echo "Disabling profiler..."
adb shell ovrgpuprofiler -d

echo "=== GPU Profile Report ==="
echo "$TRACE"
echo "========================="

# Check for frame budget violations
if echo "$TRACE" | grep -qE "GPU=[1-9][0-9]\.[0-9]ms"; then
    echo "WARNING: Frames exceeding 11.1ms budget detected!"
fi
```

## Limitations

- Maximum 30 simultaneous real-time metrics
- Trace capture blocks other profiler operations
- Results are approximate (hardware counter sampling)
- Some metrics not available on all GPU hardware revisions
