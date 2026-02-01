---
name: build-quest
description: Build IL2CPP APK for Meta Quest with Gradle caching and optional deployment
allowed-tools: Read, Write, Bash, Glob, Grep, Task
argument-validation: optional
---

# Build for Quest

Build an IL2CPP ARM64 APK for Meta Quest devices.

## Usage

```
/unity-vr-dev:build-quest [options]
```

## Options

- `--deploy` — Auto-deploy to connected Quest device after build
- `--release` — Use release configuration with keystore signing
- `--clean` — Force clean build (ignore Gradle cache)
- `--bundles` — Build asset bundles only (skip APK)

## Workflow

1. Delegate to **orchestrator** agent for pre-flight checks
2. Orchestrator routes to **build-agent** for execution
3. Build agent configures IL2CPP/ARM64 settings
4. Execute build with Gradle caching enabled
5. If `--deploy`: install and launch on connected Quest
6. Report build metrics (size, duration, configuration)

## Prerequisites

- Unity Editor running with project open
- Android SDK and NDK configured
- Meta XR SDK v74+ installed
- For deploy: Quest connected via USB or wireless ADB

## Examples

```
/unity-vr-dev:build-quest
/unity-vr-dev:build-quest --deploy
/unity-vr-dev:build-quest --release --deploy
/unity-vr-dev:build-quest --bundles
```
