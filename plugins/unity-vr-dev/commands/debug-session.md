---
name: debug-session
description: Start a Quest VR debug session with LogCat, GPU profiling, and screen mirroring
allowed-tools: Read, Bash, Grep, Glob, Task
argument-validation: optional
---

# Debug Session

Start an interactive debugging session for a Quest VR application.

## Usage

```
/unity-vr-dev:debug-session [mode]
```

## Modes

- `logs` — LogCat streaming with Unity/VR tag filtering (default)
- `gpu` — GPU profiling with ovrgpuprofiler trace capture
- `mirror` — Screen mirroring with scrcpy or MQDH
- `full` — All debug tools: logs + GPU + mirror
- `crash` — Crash investigation mode (DEBUG tag focus)

## Workflow

1. Delegate to **orchestrator** for device verification
2. Orchestrator routes to **debug-agent**
3. Debug agent checks for MQDH availability
4. Starts requested debug tools
5. Streams output and analysis

## Prerequisites

- Quest device connected via USB or wireless ADB
- Application installed on Quest
- For mirror mode: scrcpy installed or MQDH running

## Examples

```
/unity-vr-dev:debug-session
/unity-vr-dev:debug-session gpu
/unity-vr-dev:debug-session full
/unity-vr-dev:debug-session crash
```
