---
name: deploy-quest
description: Deploy APK to connected Meta Quest device via ADB
allowed-tools: Read, Bash, Grep, Glob
argument-validation: optional
---

# Deploy to Quest

Install and launch an APK on a connected Meta Quest device.

## Usage

```
/unity-vr-dev:deploy-quest [apk-path]
```

## Arguments

- `apk-path` — Path to APK file (defaults to `Builds/QuestApp.apk`)

## Options

- `--wireless` — Use wireless ADB (setup if needed)
- `--uninstall-first` — Remove existing app before install
- `--launch` — Launch app after install (default: yes)

## Workflow

1. Delegate directly to **build-agent**
2. Verify ADB device connection
3. If `--wireless`: setup wireless ADB connection
4. If `--uninstall-first`: remove existing installation
5. Install APK with replacement flag
6. Launch application
7. Report deployment status

## Prerequisites

- ADB installed and in PATH
- Quest device connected (USB or wireless)
- Developer mode enabled on Quest
- APK file exists at specified path

## Examples

```
/unity-vr-dev:deploy-quest
/unity-vr-dev:deploy-quest Builds/MyApp.apk
/unity-vr-dev:deploy-quest --wireless
/unity-vr-dev:deploy-quest --uninstall-first
```
