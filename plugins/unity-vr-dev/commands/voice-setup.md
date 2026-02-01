---
name: voice-setup
description: Configure the in-VR voice interaction pipeline for hands-free development
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
argument-validation: optional
---

# Voice Setup

Configure the voice interaction pipeline for hands-free VR development.

## Usage

```
/unity-vr-dev:voice-setup [component]
```

## Components

- `all` — Full pipeline setup (default)
- `wake-word` — Porcupine wake word only
- `stt` — Deepgram speech-to-text only
- `tts` — Text-to-speech and spatial audio only
- `ptt` — Push-to-talk via controller trigger

## Workflow

1. Delegate to **orchestrator** for environment checks
2. Orchestrator routes to **voice-agent**
3. Voice agent verifies API keys
4. Configures requested components
5. Tests each stage of the pipeline
6. Reports status and latency measurements

## Prerequisites

- Environment variables set: PICOVOICE_KEY, DEEPGRAM_KEY, CLAUDE_API_KEY
- NativeWebSocket package installed in Unity project
- Android permissions: INTERNET, RECORD_AUDIO
- For wake word: Custom "Hey Claude" Porcupine model

## Examples

```
/unity-vr-dev:voice-setup
/unity-vr-dev:voice-setup wake-word
/unity-vr-dev:voice-setup stt
/unity-vr-dev:voice-setup ptt
```
