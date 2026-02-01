# Meta Quest Developer Hub (MQDH) Integration

## Overview

MQDH v3.4+ provides an all-in-one device management tool that combines ADB, LogCat, profiling, and deployment features with a GUI.

## Detection

### Check if MQDH is Running

```bash
# macOS
pgrep -f "Meta Quest Developer Hub" && echo "MQDH running" || echo "MQDH not running"

# Windows
tasklist | findstr "MetaQuestDeveloperHub"
```

### Preference Rule

When MQDH is detected and running, prefer it over individual ADB commands for:
- Log viewing (better filtering UI)
- APK installation (drag-and-drop or CLI)
- Performance monitoring (VRC overlay)
- Screenshot/video capture

Fall back to ADB commands when MQDH is not available or for automation scripts.

## Features

### Device Management

- Auto-detect connected Quest devices
- Wireless ADB setup
- Device info (OS version, storage, battery)
- Developer settings management

### Log Viewing

- Real-time log streaming with tag filtering
- Search across log history
- Severity highlighting
- Export to file

### Performance Monitoring

- VRC FPS tracking
- GPU utilization overlay
- Memory usage tracking
- Thermal monitoring

### Deployment

- APK installation via drag-and-drop
- CLI installation: `mqdh install path/to/app.apk`
- App management (uninstall, clear data)
- OBB/asset pack deployment

### Capture

- Screenshots (PNG)
- Video recording (MP4)
- GPU trace capture
- System trace capture

## CLI Commands

MQDH provides CLI commands for automation:

```bash
# Install APK
mqdh install Builds/QuestApp.apk

# Take screenshot
mqdh capture screenshot --output screenshot.png

# Start recording
mqdh capture video --output recording.mp4 --duration 30

# Capture GPU trace
mqdh capture gpu-trace --duration 5 --output trace.json
```

## Integration with Debug Agent

The debug agent should:

1. **Check for MQDH** at session start
2. **Report availability** to the user
3. **Use MQDH commands** when available for richer output
4. **Fall back to ADB** when MQDH is not detected

### Decision Flow

```
Is MQDH running?
├── Yes → Use MQDH for logging, profiling, deployment
│         (richer output, better filtering)
└── No  → Use ADB commands directly
          (always available when ADB works)
```

## Setup

### Installation

Download from: https://developer.oculus.com/meta-quest-developer-hub

### First Run

1. Install MQDH
2. Connect Quest via USB
3. MQDH auto-detects device
4. Authorize on headset if prompted

### Wireless Setup

1. Connect Quest via USB
2. In MQDH: Device > Enable Wireless
3. Disconnect USB
4. MQDH reconnects wirelessly

## Known Limitations

- MQDH must be running before device connection
- Some features require specific Quest OS versions
- CLI commands may vary between MQDH versions
- Cannot run simultaneously with some other ADB-based tools
