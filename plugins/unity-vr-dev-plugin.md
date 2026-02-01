# Unity VR Dev Plugin - Complete File Guide

## Table of Contents

- unity-vr-dev/.claude-plugin/plugin.json
- unity-vr-dev/.mcp.json
- unity-vr-dev/agents/orchestrator.md
- unity-vr-dev/agents/build-agent.md
- unity-vr-dev/agents/debug-agent.md
- unity-vr-dev/agents/voice-agent.md
- unity-vr-dev/agents/test-agent.md
- unity-vr-dev/agents/knowledge-agent.md
- unity-vr-dev/commands/build-quest.md
- unity-vr-dev/commands/deploy-quest.md
- unity-vr-dev/commands/mcp-connect.md
- unity-vr-dev/commands/debug-session.md
- unity-vr-dev/commands/voice-setup.md
- unity-vr-dev/commands/test-suite.md
- unity-vr-dev/commands/adr-create.md
- unity-vr-dev/skills/unity-mcp-integration/SKILL.md
- unity-vr-dev/skills/unity-mcp-integration/references/unity-api-reference.md
- unity-vr-dev/skills/unity-mcp-integration/references/mcp-protocol-spec.md
- unity-vr-dev/skills/unity-mcp-integration/references/troubleshooting.md
- unity-vr-dev/skills/quest-build-automation/SKILL.md
- unity-vr-dev/skills/quest-build-automation/references/il2cpp-optimization.md
- unity-vr-dev/skills/quest-build-automation/references/gradle-caching.md
- unity-vr-dev/skills/quest-build-automation/references/keystore-management.md
- unity-vr-dev/skills/debug-orchestration/SKILL.md
- unity-vr-dev/skills/debug-orchestration/references/logcat-filtering.md
- unity-vr-dev/skills/debug-orchestration/references/ovrgpuprofiler-guide.md
- unity-vr-dev/skills/debug-orchestration/references/mqdh-integration.md
- unity-vr-dev/skills/voice-pipeline/SKILL.md
- unity-vr-dev/skills/voice-pipeline/references/porcupine-setup.md
- unity-vr-dev/skills/voice-pipeline/references/deepgram-integration.md
- unity-vr-dev/skills/voice-pipeline/references/spatial-audio.md
- unity-vr-dev/skills/adr-management/SKILL.md
- unity-vr-dev/skills/adr-management/references/adr-template.md
- unity-vr-dev/skills/adr-management/references/decision-catalog.md
- unity-vr-dev/skills/wsl2-networking/SKILL.md
- unity-vr-dev/skills/wsl2-networking/references/mirrored-mode.md
- unity-vr-dev/skills/wsl2-networking/references/port-forwarding.md
- unity-vr-dev/hooks/hooks.json
- unity-vr-dev/hooks/scripts/check-adb-connection.py
- unity-vr-dev/hooks/scripts/validate-build-config.py
- unity-vr-dev/hooks/scripts/post-build-report.sh
- unity-vr-dev/schemas/build-config.schema.json
- unity-vr-dev/schemas/mcp-response.schema.json
- unity-vr-dev/templates/adr-template.md
- unity-vr-dev/templates/build-config.json

---

## File: unity-vr-dev/.claude-plugin/plugin.json

**Extension:** json
**Language:** json
**Size:** 719 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "name": "unity-vr-dev",
  "version": "1.0.0",
  "description": "AI-powered Unity VR development for Meta Quest. Build automation, debug orchestration, voice integration, and testing through Claude Code MCP.",
  "author": {
    "name": "monxun"
  },
  "keywords": [
    "unity",
    "vr",
    "quest",
    "meta-xr",
    "build-automation",
    "debugging",
    "voice",
    "mcp",
    "il2cpp"
  ],
  "license": "MIT",
  "commands": "./commands/",
  "agents": [
    "./agents/orchestrator.md",
    "./agents/build-agent.md",
    "./agents/debug-agent.md",
    "./agents/voice-agent.md",
    "./agents/test-agent.md",
    "./agents/knowledge-agent.md"
  ],
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}
```

---

## File: unity-vr-dev/.mcp.json

**Extension:** json
**Language:** json
**Size:** 281 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "mcpServers": {
    "unity-mcp": {
      "type": "http",
      "url": "http://localhost:8080",
      "description": "Unity MCP server exposing Editor tools via JSON-RPC 2.0. Provides scene manipulation, build pipeline, asset management, and VR component creation."
    }
  }
}
```

---

## File: unity-vr-dev/agents/orchestrator.md

**Extension:** md
**Language:** markdown
**Size:** 2569 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: orchestrator
description: |
  Master coordinator for Unity VR development workflows.
  Use when: orchestrating multi-step VR tasks, routing to specialist agents,
  managing build-debug-test cycles, coordinating MCP tool invocations.
  Automatically invoked by build-quest, debug-session, voice-setup, mcp-connect commands.

tools: Task, Read, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: unity-mcp-integration, quest-build-automation
---

# Orchestrator Agent

You are the master coordination agent for the Unity VR Dev plugin. You route tasks to specialist agents based on context analysis.

## Routing Rules

Analyze the user's request and delegate to the appropriate specialist:

| Pattern | Agent | Reason |
|---------|-------|--------|
| "build", "compile", "APK", "deploy", "Quest" | build-agent | IL2CPP build and deployment |
| "debug", "logs", "LogCat", "profile", "GPU", "crash" | debug-agent | Debug and profiling tools |
| "voice", "microphone", "wake word", "speech", "TTS" | voice-agent | Voice pipeline configuration |
| "test", "coverage", "benchmark", "CI", "GameCI" | test-agent | Testing and CI/CD |
| "ADR", "decision", "architecture record" | knowledge-agent | ADR creation and search |
| "MCP", "connect", "tools", "server" | self | MCP connection management |

## Workflow Coordination

For multi-phase tasks, orchestrate sequential agent invocations:

1. **Build & Deploy**: build-agent → (optional) test-agent → build-agent (deploy)
2. **Debug Session**: Verify MCP connection → debug-agent → (optional) build-agent (rebuild)
3. **Full Iteration**: build-agent (build) → debug-agent (verify) → test-agent (validate)

## MCP Connection Management

When handling MCP connection directly:

1. Verify Unity Editor is running with MCP server active
2. Test connectivity to `localhost:8080`
3. Query tool discovery endpoint to list available MCP tools
4. Report connection status and available capabilities

## Error Handling

- If an agent reports failure, analyze the error and either retry with adjusted parameters or escalate to the user
- For build failures, check common causes: missing SDK, wrong Unity version, keystore issues
- For device failures, verify ADB connection before retrying
- Always capture error context for ADR knowledge if the issue is novel

## Context Awareness

- Track the current project state (last build result, connected devices, active debug sessions)
- Use previous command outputs to inform routing decisions
- Prefer incremental operations over full rebuilds when possible
```

---

## File: unity-vr-dev/agents/build-agent.md

**Extension:** md
**Language:** markdown
**Size:** 2816 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: build-agent
description: |
  IL2CPP build specialist for Meta Quest VR applications.
  Use when: building Quest APK, IL2CPP compilation, Gradle caching,
  ADB deployment, asset bundle builds, keystore configuration,
  "build for Quest", "deploy APK", "install on device".

tools: Read, Write, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: quest-build-automation, wsl2-networking
---

# Build Agent

You are the IL2CPP build specialist for Meta Quest VR applications. You handle the complete build-deploy lifecycle.

## Responsibilities

1. **Quest APK builds** — Configure and execute IL2CPP ARM64 builds
2. **Gradle cache optimization** — Maximize incremental build speed
3. **ADB deployment** — Install and launch APKs on Quest devices
4. **Asset bundle builds** — Hot-reload content without full rebuild
5. **Keystore management** — Configure signing for debug and release

## Build Workflow

### Standard Build

1. Verify build prerequisites (Unity version, SDK, NDK)
2. Check and apply required Player Settings (IL2CPP, ARM64, Linear, GLES3)
3. Resolve build scenes from EditorBuildSettings
4. Execute build via Unity CLI or MCP `build-quest-apk` tool
5. Report build result (success/failure, APK size, duration)

### Deploy Workflow

1. Verify ADB device connection (`adb devices`)
2. Check device storage availability
3. Install APK with replacement (`adb install -r`)
4. Launch application (`adb shell am start`)
5. Confirm application running

## Pre-Build Checks

Before every build, verify:

` ` `bash
# ADB available
adb version

# Device connected (for deploy)
adb devices | grep -v "List"

# Unity project has Android platform
# Check via MCP or project settings
` ` `

## Key Constraints

- **IL2CPP is mandatory** — Quest requires ahead-of-time compilation
- **ARM64 only** — No ARMv7 support on Quest
- **No gRPC** — Use HTTP/WebSocket for communication
- **No C# hot-reload on device** — Use asset bundles for content iteration

## Error Handling

| Error | Cause | Resolution |
|-------|-------|-----------|
| `NDK not found` | Android NDK not configured | Set NDK path in Preferences > External Tools |
| `Keystore not found` | Missing or wrong keystore path | Check KEYSTORE_PATH environment variable |
| `IL2CPP build failure` | C++ compilation error | Check build log for specific error |
| `ADB: no devices` | Quest not connected or not authorized | Enable developer mode, approve USB dialog |
| `INSTALL_FAILED_UPDATE_INCOMPATIBLE` | Signature mismatch | Uninstall existing app first |

## Output Format

Always report build results in this format:

` ` `
Build Result: SUCCESS/FAILURE
APK Path: Builds/QuestApp.apk
APK Size: XX.X MB
Build Duration: X min Y sec
Scenes: [list of included scenes]
Configuration: IL2CPP / ARM64 / Development|Release
` ` `
```

---

## File: unity-vr-dev/agents/debug-agent.md

**Extension:** md
**Language:** markdown
**Size:** 2352 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: debug-agent
description: |
  Debug tools orchestrator for Meta Quest VR applications.
  Use when: streaming logs, GPU profiling, scrcpy mirroring, MQDH usage,
  crash analysis, Immersive Debugger configuration, "show logs",
  "debug", "profile", "why is", "screen mirror".

tools: Read, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: debug-orchestration, unity-mcp-integration
---

# Debug Agent

You are the debugging specialist for Meta Quest VR applications. You orchestrate LogCat, GPU profiling, screen mirroring, and in-headset debugging tools.

## Responsibilities

1. **LogCat streaming** — Filter and analyze Unity/VR logs from Quest
2. **GPU profiling** — Capture and interpret ovrgpuprofiler traces
3. **Screen mirroring** — Setup scrcpy or MQDH mirroring
4. **Crash analysis** — Investigate native crashes and ANRs
5. **Immersive Debugger** — Configure [DebugMember] attributes for in-headset inspection

## Debug Session Startup

When starting a debug session:

1. Verify ADB connection: `adb devices`
2. Check for MQDH: `pgrep -f "Meta Quest Developer Hub"`
3. Clear old logs: `adb logcat -c`
4. Start appropriate monitoring based on the issue type

## Issue Routing

| Symptom | Approach |
|---------|----------|
| App crashes on launch | LogCat with DEBUG tag, check native crash |
| Low FPS / stuttering | ovrgpuprofiler trace, check frame budget |
| Visual artifacts | scrcpy mirroring + LogCat for shader errors |
| Specific variable wrong | Immersive Debugger with [DebugMember] |
| General debugging | LogCat streaming with Unity tag |
| Memory issues | LogCat GC warnings + Unity Profiler |

## Performance Targets

- **Frame budget**: 11.1ms (90 FPS)
- GPU time > 11.1ms = GPU-bound
- GPU time < 11.1ms with frame drops = CPU-bound
- Check `XR.WaitForGPU` profiler marker

## Output Format

Always report debug findings with:

```
Debug Session: [type]
Device: [Quest model and OS version]
Duration: [session length]
Findings:
- [categorized findings with severity]
Recommendations:
- [actionable next steps]
```

## Error Handling

- If ADB disconnects during session, attempt wireless reconnect
- If LogCat produces too much output, narrow tag filters
- If ovrgpuprofiler fails, verify Quest app is running
- If scrcpy shows black screen, try MQDH capture instead (Quest OS v74+ regression)
```

---

## File: unity-vr-dev/agents/voice-agent.md

**Extension:** md
**Language:** markdown
**Size:** 2887 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: voice-agent
description: |
  Voice pipeline specialist for in-VR voice interaction.
  Use when: configuring wake word, speech-to-text, TTS output,
  Porcupine setup, Deepgram configuration, NativeWebSocket,
  Claude API voice integration, spatial audio, microphone setup.

tools: Read, Write, Edit, Bash
model: sonnet
permissionMode: default
skills: voice-pipeline, unity-mcp-integration
---

# Voice Agent

You are the voice pipeline specialist for in-VR hands-free development. You configure and troubleshoot the full voice interaction chain.

## Responsibilities

1. **Wake word setup** — Configure Picovoice Porcupine for "Hey Claude"
2. **Push-to-talk** — Setup OVRInput trigger-based activation
3. **STT configuration** — Deepgram WebSocket streaming via NativeWebSocket
4. **Claude API integration** — SSE streaming with Claude-Unity
5. **TTS output** — Spatial audio positioning for AI responses

## Setup Workflow

### Initial Configuration

1. Verify API keys are set (PICOVOICE_KEY, DEEPGRAM_KEY, CLAUDE_API_KEY)
2. Check Android permissions (INTERNET, RECORD_AUDIO)
3. Install NativeWebSocket package
4. Configure Porcupine with custom "Hey Claude" model
5. Setup Deepgram WebSocket connection
6. Configure Claude-Unity for SSE streaming
7. Setup spatial audio source for TTS output

### API Key Verification

```bash
# Check environment variables are set (not the values)
test -n "$PICOVOICE_KEY" && echo "PICOVOICE_KEY: set" || echo "PICOVOICE_KEY: MISSING"
test -n "$DEEPGRAM_KEY" && echo "DEEPGRAM_KEY: set" || echo "DEEPGRAM_KEY: MISSING"
test -n "$CLAUDE_API_KEY" && echo "CLAUDE_API_KEY: set" || echo "CLAUDE_API_KEY: MISSING"
```

## Protocol Constraints

- **No gRPC** — IL2CPP ARM64 linking errors are a hard constraint
- **NativeWebSocket** — Required for Quest WebSocket communication
- **HTTP/REST** — For Claude API and TTS API calls
- **DispatchMessageQueue()** — Must call in Update() for NativeWebSocket on Quest

## Latency Targets

| Stage | Target | Acceptable |
|-------|--------|-----------|
| Wake word | <200ms | <300ms |
| STT | <500ms | <800ms |
| Claude processing | <1s | <2s |
| TTS | <200ms | <300ms |
| **Total pipeline** | **<2s** | **<3s** |

## Error Handling

| Issue | Resolution |
|-------|-----------|
| No microphone permission | Guide user to request RECORD_AUDIO |
| Porcupine init failure | Verify access key, fall back to push-to-talk |
| WebSocket connect failure | Check internet, retry with backoff |
| High STT latency | Reduce audio chunk size, check network |
| TTS decode failure | Verify audio format, try alternate TTS provider |

## Output Format

Report voice pipeline status as:

```
Voice Pipeline Status:
  Wake Word: [active/inactive/error]
  STT: [connected/disconnected/error]
  Claude API: [ready/processing/error]
  TTS: [ready/playing/error]
  Latency: [last measured end-to-end]
```
```

---

## File: unity-vr-dev/agents/test-agent.md

**Extension:** md
**Language:** markdown
**Size:** 3504 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: test-agent
description: |
  Testing automation specialist for Unity VR applications.
  Use when: running tests, performance benchmarks, CI/CD pipelines,
  GameCI configuration, code coverage, device testing, Unity Test Framework,
  "run tests", "benchmark", "coverage report", "check performance".

tools: Read, Write, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: unity-mcp-integration
---

# Test Agent

You are the testing automation specialist for Unity VR applications. You manage unit tests, performance benchmarks, CI/CD pipelines, and device testing.

## Responsibilities

1. **Unity Test Framework** — Run EditMode and PlayMode tests
2. **VR input simulation** — InputTestFixture for XRController inputs
3. **Performance benchmarks** — 11.1ms frame budget (90 FPS) assertions
4. **GameCI integration** — GitHub Actions with unity-test-runner@v4
5. **Device testing** — Meta Scriptable Testing for Quest device farm

## Test Types

| Type | Framework | Purpose |
|------|-----------|---------|
| EditMode | Unity Test Framework | Logic tests without Play Mode |
| PlayMode | Unity Test Framework | Runtime behavior tests |
| Performance | Unity Performance Testing | Frame budget validation |
| Integration | Custom + MCP | End-to-end MCP tool verification |
| Device | Meta Scriptable Testing | On-device automation |

## VR Input Simulation

```csharp
using UnityEngine.InputSystem;
using UnityEngine.TestTools;

[TestFixture]
public class VRInteractionTests : InputTestFixture {
    [Test]
    public void GrabInteraction_WithTrigger_GrabsObject() {
        var device = InputSystem.AddDevice<UnityEngine.XR.Interaction.Toolkit.Inputs.Simulation.XRSimulatedController>();
        Press(device.gripButton);
        // Assert grab behavior
        Release(device.gripButton);
    }
}
```

**Note**: Direct XR input subsystem calls don't work in Play Mode tests. Use Input System simulation via InputTestFixture.

## Performance Benchmarks

```csharp
[Test, Performance]
public void FrameBudget_MeetsTarget() {
    Measure.Frames()
        .WarmupCount(30)
        .MeasurementCount(120)
        .ProfilerMarkers("XR.WaitForGPU")
        .Run();
    // Assert frame time < 11.1ms for 90 FPS
}
```

**Key marker**: `XR.WaitForGPU` — indicates GPU-bound (>11.1ms) vs CPU-bound.

## GameCI Configuration

```yaml
# .github/workflows/test.yml
- uses: game-ci/unity-test-runner@v4
  with:
    testMode: all
    coverageOptions: generateBadgeReport;assemblyFilters:+MyGame.*
```

## Running Tests

### Via MCP

```bash
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"run-tests","arguments":{"mode":"playmode","category":"VR"}},"id":1}'
```

### Via Unity CLI

```bash
Unity -runTests -batchmode -projectPath /path/to/project \
  -testPlatform PlayMode \
  -testResults results.xml
```

## Output Format

```
Test Results:
  Total: XX | Passed: XX | Failed: XX | Skipped: XX
  Duration: X.Xs
  Coverage: XX.X%

Failed Tests:
  - [TestName]: [failure reason]

Performance:
  Avg Frame Time: X.Xms (budget: 11.1ms)
  P95 Frame Time: X.Xms
  GPU-bound frames: X%
```

## Error Handling

- If tests fail to start: verify Unity Test Framework package is installed
- If XR input tests fail: check InputTestFixture setup and XR Simulator
- If performance tests are noisy: increase warmup and measurement counts
- If GameCI fails: check Unity license activation in CI environment
```

---

## File: unity-vr-dev/agents/knowledge-agent.md

**Extension:** md
**Language:** markdown
**Size:** 2017 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: knowledge-agent
description: |
  Architecture Decision Record management for VR development.
  Use when: creating ADRs, searching decisions, updating decision status,
  "create ADR", "architecture decision", "why did we", decision history.

tools: Read, Write, Edit, Grep, Glob
model: haiku
permissionMode: default
skills: adr-management
---

# Knowledge Agent

You are the ADR management specialist. You create, search, and maintain Architecture Decision Records for VR development projects.

## Responsibilities

1. **Create ADRs** — Generate new ADRs from decision context
2. **Search ADRs** — Find relevant past decisions by topic
3. **Update status** — Transition ADR status (Proposed → Accepted → Deprecated/Superseded)
4. **Link related** — Connect related ADRs via references

## Creating an ADR

1. Determine the next sequential number
2. Generate kebab-case filename from title
3. Fill in the ADR template with context, decision, and consequences
4. Save to `docs/adr/` directory
5. Report the created ADR

### Naming Convention

```
docs/adr/ADR-NNNN-kebab-case-title.md
```

### Next Number Logic

```bash
# Find highest existing number
ls docs/adr/ADR-*.md 2>/dev/null | \
  sed 's/.*ADR-\([0-9]*\).*/\1/' | \
  sort -n | tail -1
```

If no ADRs exist, start at `ADR-0001`.

## Searching ADRs

When asked "why did we..." or "what was decided about...":

1. Search by keyword in ADR files
2. Check status (only Accepted ADRs are active)
3. Report the relevant decision with context

## Quality Standards

- Title should be a clear statement of the decision
- Context must explain the forces at play
- Decision must state what was chosen AND why
- Consequences must include both positive and negative impacts
- Always link to related ADRs

## Output Format

When creating:
```
Created: ADR-NNNN: [Title]
Status: Proposed
File: docs/adr/ADR-NNNN-kebab-case-title.md
```

When searching:
```
Found X relevant ADRs:
- ADR-NNNN: [Title] (Status: [status])
  Decision: [brief summary]
```
```

---

## File: unity-vr-dev/commands/build-quest.md

**Extension:** md
**Language:** markdown
**Size:** 1252 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/commands/deploy-quest.md

**Extension:** md
**Language:** markdown
**Size:** 1180 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/commands/mcp-connect.md

**Extension:** md
**Language:** markdown
**Size:** 1014 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/commands/debug-session.md

**Extension:** md
**Language:** markdown
**Size:** 1153 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/commands/voice-setup.md

**Extension:** md
**Language:** markdown
**Size:** 1231 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/commands/test-suite.md

**Extension:** md
**Language:** markdown
**Size:** 1363 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: test-suite
description: Run Unity VR test suite with coverage and performance benchmarks
allowed-tools: Read, Write, Bash, Grep, Glob, Task
argument-validation: optional
---

# Test Suite

Run the Unity VR test suite with optional coverage reporting and performance benchmarks.

## Usage

```
/unity-vr-dev:test-suite [mode]
```

## Modes

- `all` — Run all tests (default)
- `editmode` — EditMode tests only
- `playmode` — PlayMode tests only
- `performance` — Performance benchmarks only
- `coverage` — All tests with coverage report

## Options

- `--category <name>` — Filter by test category (e.g., "VR", "Build")
- `--ci` — Generate CI-compatible output (XML results)

## Workflow

1. Delegate to **orchestrator** for environment validation
2. Orchestrator routes to **test-agent**
3. Test agent runs requested test mode via MCP or Unity CLI
4. Collects results, coverage, and performance data
5. Reports summary with pass/fail, coverage %, and frame budget compliance

## Prerequisites

- Unity Editor running with project open
- Unity Test Framework package installed
- For performance tests: Unity Performance Testing package
- For coverage: Code Coverage package

## Examples

```
/unity-vr-dev:test-suite
/unity-vr-dev:test-suite playmode
/unity-vr-dev:test-suite performance
/unity-vr-dev:test-suite coverage --category VR
```
```

---

## File: unity-vr-dev/commands/adr-create.md

**Extension:** md
**Language:** markdown
**Size:** 1079 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: adr-create
description: Create a new Architecture Decision Record for VR development knowledge capture
allowed-tools: Read, Write, Edit, Grep, Glob, Task
argument-validation: optional
---

# Create ADR

Create a new Architecture Decision Record to capture a technical decision.

## Usage

```
/unity-vr-dev:adr-create [title]
```

## Arguments

- `title` — Short descriptive title for the decision (e.g., "Use HTTP for MCP transport")

## Workflow

1. Delegate directly to **knowledge-agent**
2. Knowledge agent determines next ADR number
3. Creates ADR file from template with provided title
4. Prompts for context, decision, and consequences if not provided
5. Saves to `docs/adr/` directory

## Output

Creates file at `docs/adr/ADR-NNNN-kebab-case-title.md` with:
- Sequential number
- Provided title
- Template sections ready for content
- Status: Proposed

## Examples

```
/unity-vr-dev:adr-create Use HTTP for MCP transport
/unity-vr-dev:adr-create Adopt Porcupine for wake word detection
/unity-vr-dev:adr-create Select GameCI for Unity testing pipeline
```
```

---

## File: unity-vr-dev/skills/unity-mcp-integration/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 5096 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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
```

---

## File: unity-vr-dev/skills/unity-mcp-integration/references/unity-api-reference.md

**Extension:** md
**Language:** markdown
**Size:** 4602 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Unity API Reference for MCP Tools

## Scene Operations

### EditorSceneManager

```csharp
// Get active scene
Scene scene = EditorSceneManager.GetActiveScene();

// Save scene
EditorSceneManager.SaveScene(scene);

// Create new scene
Scene newScene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects);
```

### GameObject Creation

```csharp
// Create empty
var go = new GameObject("MyObject");

// Create primitive
var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);

// Instantiate prefab
var instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
```

### Component Management

```csharp
// Add component
var rb = go.AddComponent<Rigidbody>();

// Get component
var collider = go.GetComponent<Collider>();

// Configure XR Grab Interactable
var grab = go.AddComponent<XRGrabInteractable>();
grab.movementType = XRBaseInteractable.MovementType.VelocityTracking;
grab.throwOnDetach = true;
```

## XR Interaction Toolkit Components

### XRGrabInteractable

```csharp
var grab = go.AddComponent<XRGrabInteractable>();
grab.movementType = XRBaseInteractable.MovementType.VelocityTracking;
grab.throwOnDetach = true;
grab.smoothPosition = true;
grab.smoothRotation = true;
grab.tightenPosition = 0.5f;
grab.tightenRotation = 0.5f;
```

### XRSocketInteractor

```csharp
var socket = go.AddComponent<XRSocketInteractor>();
socket.showInteractableHoverMeshes = true;
socket.recycleDelayTime = 1f;
```

### XRRayInteractor

```csharp
var ray = go.AddComponent<XRRayInteractor>();
ray.maxRaycastDistance = 10f;
ray.enableUIInteraction = true;
```

## Asset Management

### AssetDatabase

```csharp
// Import asset
AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);

// Create material
var mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
AssetDatabase.CreateAsset(mat, "Assets/Materials/NewMaterial.mat");

// Refresh database
AssetDatabase.Refresh();
```

### PrefabUtility

```csharp
// Save as prefab
PrefabUtility.SaveAsPrefabAsset(go, "Assets/Prefabs/MyPrefab.prefab");

// Unpack prefab
PrefabUtility.UnpackPrefabInstance(go, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
```

### AssetBundle Building

```csharp
AssetBundleBuild[] builds = new AssetBundleBuild[1];
builds[0].assetBundleName = "scene-bundle";
builds[0].assetNames = new string[] { "Assets/Scenes/MyScene.unity" };

BuildPipeline.BuildAssetBundles(
    "Assets/StreamingAssets/Bundles",
    builds,
    BuildAssetBundleOptions.ChunkBasedCompression,
    BuildTarget.Android
);
```

## Build Pipeline

### BuildPlayerOptions

```csharp
BuildPlayerOptions options = new BuildPlayerOptions {
    scenes = EditorBuildSettings.scenes
        .Where(s => s.enabled)
        .Select(s => s.path).ToArray(),
    locationPathName = "Builds/QuestApp.apk",
    target = BuildTarget.Android,
    targetGroup = BuildTargetGroup.Android,
    options = BuildOptions.None
};
```

### Quest-Specific Settings

```csharp
// Required for Quest
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;

// Graphics
PlayerSettings.colorSpace = ColorSpace.Linear;
PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new[] { GraphicsDeviceType.OpenGLES3 });

// XR
PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel29;
PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;
```

## Test APIs

### TestRunnerApi

```csharp
var testRunnerApi = ScriptableObject.CreateInstance<TestRunnerApi>();
testRunnerApi.Execute(new ExecutionSettings {
    filter = new Filter {
        testMode = TestMode.PlayMode,
        categoryNames = new[] { "VR" }
    }
});
```

### Performance Testing

```csharp
[Test, Performance]
public void FrameBudget_MeetsTarget()
{
    Measure.Frames()
        .WarmupCount(30)
        .MeasurementCount(120)
        .ProfilerMarkers("XR.WaitForGPU")
        .Run();
}
```

## Thread Safety Pattern

```csharp
// All MCP tool implementations must wrap Unity calls:
public string MyTool(string param) {
    return MainThread.Instance.Run(() => {
        // Safe to call Unity APIs here
        var go = new GameObject(param);
        return $"Created {go.name}";
    });
}

// Async variant for long operations:
public async Task<string> MyAsyncTool(string param) {
    return await MainThread.Instance.RunAsync(() => {
        // Long-running Unity operation
        AssetDatabase.Refresh();
        return "Done";
    });
}
```
```


## File: unity-vr-dev/skills/unity-mcp-integration/references/mcp-protocol-spec.md

**Extension:** md
**Language:** markdown
**Size:** 3826 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# MCP Protocol Specification for Unity

## JSON-RPC 2.0 Protocol

The Unity MCP server uses JSON-RPC 2.0 over HTTP transport.

### Base URL

```
http://localhost:8080
```

### Request Format

```json
{
  "jsonrpc": "2.0",
  "method": "<method-name>",
  "params": { ... },
  "id": <integer>
}
```

### Response Format (Success)

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Operation result message"
      }
    ]
  },
  "id": <integer>
}
```

### Response Format (Error)

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": { "details": "..." }
  },
  "id": <integer>
}
```

## Standard MCP Methods

### tools/list

Discover available tools on the server.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "create-vr-interactable",
        "description": "Create a VR interactable GameObject",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": { "type": "string", "description": "Object name" },
            "position": { "type": "string", "description": "Position x,y,z" }
          },
          "required": ["name"]
        }
      }
    ]
  },
  "id": 1
}
```

### tools/call

Invoke a specific tool.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-vr-interactable",
    "arguments": {
      "name": "GrabbableSphere",
      "position": "0,1.2,0"
    }
  },
  "id": 2
}
```

### resources/list

List available resources (scenes, assets, project info).

```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "id": 3
}
```

### resources/read

Read a specific resource.

```json
{
  "jsonrpc": "2.0",
  "method": "resources/read",
  "params": {
    "uri": "unity://scene/active"
  },
  "id": 4
}
```

## Error Codes

| Code | Meaning | Common Cause |
|------|---------|-------------|
| -32700 | Parse error | Malformed JSON |
| -32600 | Invalid request | Missing jsonrpc or method |
| -32601 | Method not found | Tool not registered |
| -32602 | Invalid params | Wrong argument types |
| -32603 | Internal error | Unity API exception |
| -32000 | Server error | MCP server not ready |

## Tool Registration

Tools are registered via the `[McpPluginTool]` attribute in C#. The server auto-discovers all decorated methods at startup and after assembly reload.

### Attribute Parameters

```csharp
[McpPluginTool(
    "tool-name",           // Unique identifier (kebab-case)
    Title = "Display Name", // Human-readable name
    Destructive = false,    // Marks destructive operations
    ReadOnly = true         // Marks read-only operations
)]
```

### Parameter Attributes

```csharp
public string MyTool(
    [Description("Parameter description")] string required,
    [Description("Optional param")] string optional = "default"
)
```

## Communication Flow

```
1. Claude Code sends JSON-RPC request via HTTP POST
2. Unity MCP server receives on background thread
3. Server parses JSON-RPC, validates method and params
4. Tool implementation wraps Unity calls in MainThread.Instance.Run()
5. Main thread executes Unity API operations on next Update()
6. Result marshalled back to background thread
7. JSON-RPC response sent to Claude Code
```

## Health Check

```bash
curl -s http://localhost:8080/health
```

Expected response:

```json
{
  "status": "ok",
  "unity_version": "2022.3.20f1",
  "tools_count": 15,
  "uptime_seconds": 120
}
```

## Rate Limiting

The server processes requests sequentially on Unity's main thread. Rapid-fire requests queue in the dispatcher. For batch operations, prefer single tools that operate on collections rather than individual object calls.

```

---

## File: unity-vr-dev/skills/unity-mcp-integration/references/troubleshooting.md

**Extension:** md
**Language:** markdown
**Size:** 3994 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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

```

---

## File: unity-vr-dev/skills/quest-build-automation/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 5787 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: quest-build-automation
description: |
  Quest 2/3/Pro build automation with IL2CPP and Gradle optimization.
  Use when: building APK, IL2CPP compilation, ARM64 builds, Gradle caching,
  deploy to Quest, ADB install, keystore management, asset bundles,
  "build for Quest", "deploy APK", incremental builds, hot-reload.
  Supports: Unity 2022.3-Unity 6, Meta XR SDK v74+, signed APKs.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Quest Build Automation

Automate IL2CPP ARM64 builds for Meta Quest with Gradle caching, keystore management, and ADB deployment.

## Hard Constraints

| Constraint | Value | Impact |
|-----------|-------|--------|
| Scripting Backend | IL2CPP | No C# hot-reload on device |
| Architecture | ARM64 | ARMv7/Mono not supported |
| Graphics API | OpenGL ES 3.0 | Vulkan also supported |
| Color Space | Linear | Requires GLES 3.0 or Vulkan |
| Min SDK | Android API 29 | Quest 2 minimum |

## Build Configuration

### Required Player Settings

```csharp
// Scripting
PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;

// Graphics
PlayerSettings.colorSpace = ColorSpace.Linear;
PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new[] { GraphicsDeviceType.OpenGLES3 });

// Android
PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel29;
PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;

// Build system
EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;
```

### Build Command

```csharp
BuildPlayerOptions options = new BuildPlayerOptions {
    scenes = EditorBuildSettings.scenes
        .Where(s => s.enabled)
        .Select(s => s.path).ToArray(),
    locationPathName = "Builds/QuestApp.apk",
    target = BuildTarget.Android,
    targetGroup = BuildTargetGroup.Android,
    options = BuildOptions.None
};
BuildPipeline.BuildPlayer(options);
```

### Unity CLI Build

```bash
# Headless build from command line
Unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -executeMethod BuildScript.BuildQuest \
  -logFile build.log
```

## Gradle Caching

Gradle caching reduces incremental build times by 30-50%.

### Enable Caching

In `Preferences > External Tools`:
- Check "Export Project" for manual Gradle builds
- Or use embedded Gradle with cache enabled

### Gradle Properties

```properties
# gradle.properties (in exported project)
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
android.enableBuildCache=true
```

### Cache Location

```bash
# Default cache directory
~/.gradle/caches/

# Clear cache if builds are inconsistent
rm -rf ~/.gradle/caches/build-cache-*
```

See `references/gradle-caching.md` for advanced cache optimization.

## ADB Deployment

### Install and Launch

```bash
# Install APK (replace existing)
adb install -r Builds/QuestApp.apk

# Launch application
adb shell am start -n com.company.app/com.unity3d.player.UnityPlayerActivity

# Combined install and launch
adb install -r Builds/QuestApp.apk && \
adb shell am start -n com.company.app/com.unity3d.player.UnityPlayerActivity
```

### Wireless ADB

```bash
# Setup (with USB connected)
adb tcpip 5555
adb connect <quest-ip>:5555

# Verify
adb devices
```

### Uninstall

```bash
adb uninstall com.company.app
```

## Keystore Management

### Create Keystore

```bash
keytool -genkey -v \
  -keystore quest-release.keystore \
  -alias quest-key \
  -keyalg RSA -keysize 2048 \
  -validity 10000
```

### Configure in Unity

```csharp
PlayerSettings.Android.useCustomKeystore = true;
PlayerSettings.Android.keystoreName = "path/to/quest-release.keystore";
PlayerSettings.Android.keystorePass = Environment.GetEnvironmentVariable("KEYSTORE_PASS");
PlayerSettings.Android.keyaliasName = "quest-key";
PlayerSettings.Android.keyaliasPass = Environment.GetEnvironmentVariable("KEY_PASS");
```

**Security**: Store passwords in environment variables or credential manager. Never commit to source control.

See `references/keystore-management.md` for CI/CD keystore handling.

## Hot-Reload Strategy

IL2CPP eliminates C# hot-reload on device. Use layered iteration:

| Layer | Strategy | Speed |
|-------|----------|-------|
| Editor | Hot Reload plugins (Mono in Editor) | Milliseconds |
| Content | Asset bundle streaming | Seconds |
| Device | Gradle-cached incremental build | 30-50% faster |
| Full | Clean IL2CPP build | Minutes |

### Asset Bundle Hot-Reload

```csharp
// Build bundles for Android
BuildPipeline.BuildAssetBundles(
    "Assets/StreamingAssets/Bundles",
    BuildAssetBundleOptions.ChunkBasedCompression,
    BuildTarget.Android
);
```

```bash
# Push updated bundle to device
adb push Assets/StreamingAssets/Bundles/scene-bundle \
  /sdcard/Android/data/com.company.app/files/Bundles/

# Trigger reload via MCP tool
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"reload-bundles"},"id":1}'
```

## Build Variants

### Development Build

```csharp
options.options = BuildOptions.Development |
                  BuildOptions.AllowDebugging |
                  BuildOptions.ConnectWithProfiler;
```

### Release Build

```csharp
options.options = BuildOptions.None;
// Ensure keystore is configured
// Enable code stripping for smaller APK
PlayerSettings.stripEngineCode = true;
```

## References

- `references/il2cpp-optimization.md` — IL2CPP build size and speed optimization
- `references/gradle-caching.md` — Advanced Gradle cache configuration
- `references/keystore-management.md` — Keystore creation, backup, CI/CD usage

```

---

## File: unity-vr-dev/skills/quest-build-automation/references/il2cpp-optimization.md

**Extension:** md
**Language:** markdown
**Size:** 3507 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# IL2CPP Optimization Guide

## Build Size Reduction

### Managed Code Stripping

```csharp
// In Player Settings
PlayerSettings.stripEngineCode = true;
```

Stripping levels (Project Settings > Player > Other Settings):
- **Minimal**: Remove unreachable managed code
- **Low**: Remove most unreachable code
- **Medium**: Remove more aggressively (recommended for Quest)
- **High**: Maximum stripping (test thoroughly)

### link.xml Preservation

When stripping removes code needed at runtime (especially reflection-based):

```xml
<linker>
  <!-- Preserve entire assembly -->
  <assembly fullname="MyGameplay" preserve="all"/>

  <!-- Preserve specific type -->
  <assembly fullname="MyPlugins">
    <type fullname="MyPlugins.McpTools" preserve="all"/>
  </assembly>

  <!-- Preserve by namespace -->
  <assembly fullname="ThirdParty">
    <namespace fullname="ThirdParty.MCP" preserve="all"/>
  </assembly>
</linker>
```

Place `link.xml` in `Assets/` directory.

### Assembly Definitions

Use Assembly Definitions (.asmdef) to:
- Reduce recompilation scope during development
- Enable selective stripping per assembly
- Improve incremental build times

```json
{
  "name": "VR.Interactions",
  "references": [
    "Unity.XR.Interaction.Toolkit",
    "Unity.InputSystem"
  ],
  "includePlatforms": ["Android"],
  "allowUnsafeCode": false
}
```

## Build Speed Optimization

### Incremental IL2CPP

Unity caches IL2CPP output between builds. To benefit:
- Don't clean the `Library/` folder between builds
- Use the same build output directory
- Keep `Library/Il2cppBuildCache/` intact

### Build Cache Location

```
Library/Il2cppBuildCache/     # C++ compilation cache
Library/Bee/                   # Build system cache
Temp/gradleOut/               # Gradle build cache
```

### Parallel Compilation

```
# Unity Editor preferences
Preferences > External Tools > IL2CPP C++ Compiler Configuration
  - Debug: Fastest builds, no optimization
  - Release: Balanced speed and optimization
  - Master: Full optimization, slowest builds
```

For development, use **Debug** or **Release** configuration.

## APK Size Analysis

### Build Report

```csharp
// After build, check the report
var report = BuildReport.GetLatestReport();
Debug.Log($"Total size: {report.summary.totalSize}");
foreach (var step in report.steps) {
    Debug.Log($"{step.name}: {step.duration}");
}
```

### Common Size Offenders

| Asset Type | Typical Size | Optimization |
|-----------|-------------|-------------|
| Textures | 40-60% | Compress with ASTC, reduce resolution |
| Audio | 10-20% | Vorbis compression, mono for SFX |
| Meshes | 10-15% | Mesh compression, LODs |
| Scripts (IL2CPP) | 5-15% | Code stripping, assembly defs |
| Shaders | 5-10% | Strip unused variants |

### Texture Compression

Quest 2 supports ASTC natively:

```
Texture Import Settings:
  Override for Android: Yes
  Format: ASTC 6x6 (good quality/size balance)
  Compressor Quality: Best
```

## Runtime Performance

### Ahead-of-Time Compilation

IL2CPP converts all C# to C++ and compiles ahead of time. This means:
- No JIT compilation overhead at runtime
- Predictable performance without JIT warmup
- Generic types fully expanded at compile time
- Virtual method dispatch optimized

### Generic Sharing

IL2CPP shares generic implementations where possible. For best results:
- Prefer reference type generics (shared implementation)
- Value type generics create separate implementations (larger binary)
- Avoid excessive generic type variations

```

---

## File: unity-vr-dev/skills/quest-build-automation/references/gradle-caching.md

**Extension:** md
**Language:** markdown
**Size:** 3354 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Gradle Caching for Quest Builds

## Cache Configuration

### Enable Build Cache

In the exported Gradle project's `gradle.properties`:

```properties
# Build caching
org.gradle.caching=true
android.enableBuildCache=true

# Parallel execution
org.gradle.parallel=true

# Daemon (keeps Gradle JVM running between builds)
org.gradle.daemon=true

# Memory allocation
org.gradle.jvmargs=-Xmx4096m -XX:+HeapDumpOnOutOfMemoryError

# R8 (code shrinking) cache
android.enableR8.fullMode=true
```

### Local Cache Directory

```properties
# Custom cache location (gradle.properties)
org.gradle.caching=true

# Or in init.gradle
buildCache {
    local {
        directory = new File(rootDir, '.gradle-cache')
        removeUnusedEntriesAfterDays = 30
    }
}
```

### Cache Location

Default: `~/.gradle/caches/`

```bash
# Check cache size
du -sh ~/.gradle/caches/

# Clear stale caches
rm -rf ~/.gradle/caches/build-cache-*
rm -rf ~/.gradle/caches/transforms-*
```

## Incremental Build Strategy

### What Gets Cached

| Component | Cached? | Notes |
|-----------|---------|-------|
| IL2CPP C++ output | Yes | `Library/Il2cppBuildCache/` |
| Gradle compilation | Yes | `.gradle/` in project |
| DEX conversion | Yes | Gradle build cache |
| APK packaging | Partial | Resources may re-pack |
| Asset processing | Yes | `Library/` folder |

### Typical Speed Improvements

| Build Type | Clean Build | Cached Build | Improvement |
|-----------|-------------|-------------|-------------|
| Code-only change | 5-10 min | 2-5 min | 30-50% |
| Asset change | 5-10 min | 3-6 min | 20-40% |
| Config change | 5-10 min | 4-8 min | 10-30% |
| Full clean | 8-15 min | N/A | Baseline |

### Maximizing Cache Hits

1. **Don't clean between builds** — Let IL2CPP and Gradle reuse cached outputs
2. **Use consistent build settings** — Changing options invalidates caches
3. **Keep Library/ intact** — Contains IL2CPP build cache
4. **Same output path** — Changing APK output path may invalidate packaging cache

## CI/CD Cache Strategy

### GitHub Actions Cache

```yaml
- name: Cache Gradle
  uses: actions/cache@v3
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ hashFiles('**/*.gradle*') }}
    restore-keys: gradle-

- name: Cache IL2CPP
  uses: actions/cache@v3
  with:
    path: Library/Il2cppBuildCache
    key: il2cpp-${{ hashFiles('Assets/**/*.cs') }}
    restore-keys: il2cpp-
```

### Cache Invalidation

Caches should be invalidated when:
- Unity version changes
- Android SDK/NDK version changes
- Gradle plugin version changes
- Significant dependency changes

```bash
# Force clean build
rm -rf Library/Il2cppBuildCache/
rm -rf Temp/gradleOut/
```

## Troubleshooting

### Build Fails After Cache

**Symptom**: Build errors that don't occur on clean build

**Fix**: Incremental delete of specific caches:
```bash
# Try in order, rebuilding after each:
rm -rf Temp/gradleOut/
rm -rf Library/Il2cppBuildCache/
rm -rf Library/Bee/
```

### Gradle Daemon Memory Issues

**Symptom**: `OutOfMemoryError` during build

**Fix**: Increase daemon memory:
```properties
org.gradle.jvmargs=-Xmx6144m -XX:MaxMetaspaceSize=512m
```

### Cache Size Growing

**Symptom**: Disk usage steadily increasing

**Fix**: Configure cache eviction:
```groovy
buildCache {
    local {
        removeUnusedEntriesAfterDays = 14
    }
}
```

```

---

## File: unity-vr-dev/skills/quest-build-automation/references/keystore-management.md

**Extension:** md
**Language:** markdown
**Size:** 3297 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Keystore Management for Quest Builds

## Creating a Keystore

### Command Line

```bash
keytool -genkey -v \
  -keystore quest-release.keystore \
  -alias quest-key \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "$KEYSTORE_PASS" \
  -keypass "$KEY_PASS" \
  -dname "CN=Developer,OU=VR,O=Company,L=City,ST=State,C=US"
```

### Unity GUI

1. Player Settings > Publishing Settings
2. Check "Custom Keystore"
3. Click "Create New Keystore..."
4. Set password and alias

## Security Best Practices

### Never Commit Keystores

```gitignore
# .gitignore
*.keystore
*.jks
keystore.properties
```

### Environment Variables

```bash
# Set in shell profile or CI secrets
export KEYSTORE_PATH="/secure/path/quest-release.keystore"
export KEYSTORE_PASS="secure-password"
export KEY_ALIAS="quest-key"
export KEY_PASS="secure-key-password"
```

### Unity Configuration via Script

```csharp
public static void ConfigureKeystore() {
    PlayerSettings.Android.useCustomKeystore = true;
    PlayerSettings.Android.keystoreName = Environment.GetEnvironmentVariable("KEYSTORE_PATH");
    PlayerSettings.Android.keystorePass = Environment.GetEnvironmentVariable("KEYSTORE_PASS");
    PlayerSettings.Android.keyaliasName = Environment.GetEnvironmentVariable("KEY_ALIAS");
    PlayerSettings.Android.keyaliasPass = Environment.GetEnvironmentVariable("KEY_PASS");
}
```

## CI/CD Integration

### GitHub Actions Secrets

```yaml
# In repository settings, add secrets:
# KEYSTORE_BASE64 - base64-encoded keystore file
# KEYSTORE_PASS
# KEY_ALIAS
# KEY_PASS

- name: Decode keystore
  run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > quest-release.keystore

- name: Build with keystore
  env:
    KEYSTORE_PATH: quest-release.keystore
    KEYSTORE_PASS: ${{ secrets.KEYSTORE_PASS }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASS: ${{ secrets.KEY_PASS }}
  run: unity-build-command
```

### Encode Keystore for CI

```bash
# Encode keystore as base64 for storage in CI secrets
base64 -i quest-release.keystore -o keystore-base64.txt
# Copy contents of keystore-base64.txt to CI secret
```

## Backup and Recovery

### Backup Strategy

1. Store keystore in secure location (password manager, hardware security module)
2. Keep encrypted backup separate from source code
3. Document the alias name and creation date
4. Test restoration periodically

### If Keystore is Lost

- Cannot update existing app on Meta Store
- Must submit as new application with new package name
- All existing installs become orphaned

**Prevention**: Always maintain at least 2 secure copies of production keystores.

## Debug vs Release Signing

### Debug Keystore

Unity auto-generates a debug keystore for development:
```
Location: ~/.android/debug.keystore
Alias: androiddebugkey
Password: android
```

Use debug keystore for:
- Local development builds
- Testing on personal devices
- CI development builds

### Release Keystore

Use custom keystore for:
- Meta App Lab submissions
- Meta Store releases
- Distribution builds

## Keystore Verification

```bash
# List keystore contents
keytool -list -v -keystore quest-release.keystore

# Verify APK signing
jarsigner -verify -verbose -certs Builds/QuestApp.apk

# Check APK signature (Android SDK)
apksigner verify --verbose Builds/QuestApp.apk
```

```

---

## File: unity-vr-dev/skills/debug-orchestration/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 5329 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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

```

---

## File: unity-vr-dev/skills/debug-orchestration/references/logcat-filtering.md

**Extension:** md
**Language:** markdown
**Size:** 2872 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# LogCat Filtering Guide

## Tag-Based Filtering

### Unity-Specific Tags

```bash
# Core Unity tags
adb logcat -s Unity         # Unity engine logs
adb logcat -s UnityMain     # Main thread logs

# VR-specific tags
adb logcat -s VrApi                  # Meta VR runtime
adb logcat -s XrPerformanceManager   # XR performance metrics
adb logcat -s OVRPlugin              # OVR plugin events

# Android system tags
adb logcat -s ActivityManager   # Activity lifecycle
adb logcat -s PackageManager    # Package install/update
adb logcat -s dalvikvm          # VM events
adb logcat -s DEBUG             # Native crashes
```

### Combined Tag Filter

```bash
# Full VR debug filter
adb logcat -s Unity,VrApi,XrPerformanceManager,ActivityManager,PackageManager,dalvikvm,DEBUG

# Performance focus
adb logcat -s VrApi,XrPerformanceManager,OVRPlugin

# Crash investigation
adb logcat -s DEBUG,Unity:E,dalvikvm:E
```

## Severity Filtering

```bash
# Only errors and fatals from all tags
adb logcat *:E

# Warnings and above from Unity, errors from VrApi
adb logcat -s Unity:W VrApi:E

# Verbose output for specific tag
adb logcat -s Unity:V
```

## Regex Filtering

```bash
# Filter by message content
adb logcat -s Unity | grep -i "exception"
adb logcat -s Unity | grep -i "error\|warning\|null"
adb logcat -s Unity | grep -E "FPS|frame|render"

# Exclude noise
adb logcat -s Unity | grep -v "GarbageCollector\|Shader\|Loading"

# Performance metrics extraction
adb logcat -s VrApi | grep -E "FPS=[0-9]+"
```

## Output Formatting

```bash
# With timestamps
adb logcat -v time -s Unity

# With thread info
adb logcat -v threadtime -s Unity

# With process info
adb logcat -v process -s Unity

# Brief format (tag and message only)
adb logcat -v brief -s Unity
```

## Log Capture to File

```bash
# Capture to file
adb logcat -s Unity > unity_logs.txt

# Capture with timeout (30 seconds)
timeout 30 adb logcat -s Unity > unity_logs.txt

# Append to existing file
adb logcat -s Unity >> unity_logs.txt
```

## Common Log Patterns

### Null Reference

```
E Unity   : NullReferenceException: Object reference not set to an instance of an object
```

Filter: `adb logcat -s Unity:E | grep "NullReference"`

### Memory Warnings

```
W Unity   : [GarbageCollector] GC.Alloc exceeded threshold
```

Filter: `adb logcat -s Unity:W | grep "GarbageCollector\|memory\|alloc"`

### XR Performance Drops

```
W VrApi   : FPS=72 Prd=0 Tear=0 Early=0 Stale=18
```

Filter: `adb logcat -s VrApi | grep "Stale=[1-9]"`

### Native Crashes

```
F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR)
```

Filter: `adb logcat -s DEBUG | grep "signal\|backtrace\|SEGV"`

## Session Management

```bash
# Clear all logs before starting
adb logcat -c

# Get log buffer size
adb logcat -g

# Dump current log and exit
adb logcat -d -s Unity

# Ring buffer (last N lines)
adb logcat -t 100 -s Unity
```

```

---

## File: unity-vr-dev/skills/debug-orchestration/references/ovrgpuprofiler-guide.md

**Extension:** md
**Language:** markdown
**Size:** 3443 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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

```

---

## File: unity-vr-dev/skills/debug-orchestration/references/mqdh-integration.md

**Extension:** md
**Language:** markdown
**Size:** 2825 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
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

```

---

## File: unity-vr-dev/skills/voice-pipeline/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 6246 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: voice-pipeline
description: |
  In-VR voice interaction pipeline for hands-free development.
  Use when: voice commands, wake word detection, speech-to-text,
  Porcupine setup, Deepgram STT, NativeWebSocket, spatial audio,
  "Hey Claude", microphone, TTS, voice setup, Claude API voice.
  Supports: push-to-talk, wake word, streaming STT, SSE responses.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Voice Pipeline

Configure the in-VR voice interaction pipeline: Wake Word → STT → Claude API → TTS with spatial audio.

## Pipeline Architecture

```
User speaks → Porcupine Wake Word (on-device, 50-200ms)
  → Deepgram STT (WebSocket streaming, 100-500ms)
    → Claude API (SSE streaming, 350ms-1s+)
      → TTS (speculative processing, 75-200ms)
        → Spatial Audio Output (3D positioned)
```

**Total latency**: 600ms-2s (acceptable for VR assistance)

## Components

| Stage | Technology | Latency | Location |
|-------|-----------|---------|----------|
| Wake Word | Picovoice Porcupine | 50-200ms | On-device |
| Push-to-Talk | OVRInput trigger | Immediate | On-device |
| Speech-to-Text | Deepgram WebSocket | 100-500ms | Cloud |
| LLM Processing | Claude API (SSE) | 350ms-1s+ | Cloud |
| Text-to-Speech | Deepgram TTS | 75-200ms | Cloud |
| Audio Output | Unity Spatial Audio | <10ms | On-device |

## Wake Word Detection

### Picovoice Porcupine

On-device processing — no cloud dependency, low latency, power-efficient.

```csharp
using Pv.Unity;

PorcupineManager porcupine;

void Start() {
    porcupine = PorcupineManager.FromKeywordPaths(
        accessKey: Environment.GetEnvironmentVariable("PICOVOICE_KEY"),
        keywordPaths: new string[] { "hey-claude_en_android.ppn" },
        wakeWordCallback: OnWakeWord
    );
    porcupine.Start();
}

void OnWakeWord(int keywordIndex) {
    Debug.Log("Wake word detected!");
    StartListening();
}

void OnDestroy() {
    porcupine?.Stop();
    porcupine?.Delete();
}
```

**Quest compatibility**: Porcupine supports Android (Quest's base OS). Not explicitly Quest-certified — verify with Picovoice.

### Push-to-Talk Alternative

```csharp
void Update() {
    // Right trigger for push-to-talk
    if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch)) {
        StartListening();
    }
    if (OVRInput.GetUp(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch)) {
        StopListening();
    }
}
```

## Speech-to-Text (Deepgram)

### WebSocket Streaming via NativeWebSocket

```csharp
using NativeWebSocket;

WebSocket ws;

async void StartListening() {
    ws = new WebSocket(
        "wss://api.deepgram.com/v1/listen?" +
        "encoding=linear16&sample_rate=16000&channels=1",
        new Dictionary<string, string> {
            { "Authorization", $"Token {Environment.GetEnvironmentVariable("DEEPGRAM_KEY")}" }
        }
    );

    ws.OnMessage += (bytes) => {
        string json = System.Text.Encoding.UTF8.GetString(bytes);
        ProcessTranscription(json);
    };

    await ws.Connect();
    StartMicrophoneCapture();
}

void Update() {
    // Required for NativeWebSocket on Quest
    ws?.DispatchMessageQueue();
}
```

### Audio Streaming

```csharp
void StreamAudioChunk(float[] samples) {
    // Convert float PCM to 16-bit PCM bytes
    byte[] pcmBytes = new byte[samples.Length * 2];
    for (int i = 0; i < samples.Length; i++) {
        short val = (short)(samples[i] * short.MaxValue);
        pcmBytes[i * 2] = (byte)(val & 0xFF);
        pcmBytes[i * 2 + 1] = (byte)((val >> 8) & 0xFF);
    }
    ws.Send(pcmBytes);  // Stream 100-200ms chunks
}
```

**Note**: NativeWebSocket has reported connectivity issues on some Quest devices. Test thoroughly.

## Claude API Integration

### SSE Streaming via Claude-Unity

```csharp
using ClaudeUnity;

async void ProcessVoiceCommand(string transcription) {
    var client = new ClaudeClient(
        apiKey: Environment.GetEnvironmentVariable("CLAUDE_API_KEY")
    );

    // Stream responses for lower perceived latency
    await client.StreamMessageAsync(
        model: "claude-sonnet-4-20250514",
        messages: new[] {
            new Message("user", transcription)
        },
        onPartialResponse: (partial) => {
            // Begin TTS on partial response (speculative processing)
            QueueTTSChunk(partial);
        },
        onComplete: (response) => {
            Debug.Log($"Full response: {response}");
        }
    );
}
```

**IL2CPP compatible**: Claude-Unity verified working with both IL2CPP and Mono backends.

## Text-to-Speech

### Spatial Audio Output

```csharp
void PlaySpatialTTS(AudioClip clip, Vector3 sourcePosition) {
    var audioSource = GetComponent<AudioSource>();
    audioSource.spatialBlend = 1.0f;  // Full 3D
    audioSource.transform.position = sourcePosition;
    audioSource.clip = clip;
    audioSource.Play();
}
```

### Speculative Processing

Start TTS before Claude finishes generating the full response:

1. Receive partial SSE response from Claude
2. Send sentence-boundary text to TTS API
3. Queue audio clips for sequential playback
4. Continue receiving and processing in parallel

This reduces perceived latency by 200-500ms.

## API Keys

All API keys must be stored securely:

```bash
# Environment variables (never commit to source)
export PICOVOICE_KEY="your-picovoice-access-key"
export DEEPGRAM_KEY="your-deepgram-api-key"
export CLAUDE_API_KEY="your-claude-api-key"
```

**Unity Android Manifest** — Requires internet permission:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

## Protocol Constraints

- **No gRPC** — IL2CPP ARM64 linking errors (`undefined symbol: grpcsharp_init`)
- **Use NativeWebSocket** — Open-source, no external DLLs, Quest compatible
- **HTTP/WebSocket only** — All cloud APIs accessed via REST or WebSocket

## References

- `references/porcupine-setup.md` — Wake word model setup and configuration
- `references/deepgram-integration.md` — Deepgram API streaming details
- `references/spatial-audio.md` — Unity spatial audio for TTS output

```

---

## File: unity-vr-dev/skills/voice-pipeline/references/porcupine-setup.md

**Extension:** md
**Language:** markdown
**Size:** 4029 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Porcupine Wake Word Setup

## Overview

Picovoice Porcupine provides on-device wake word detection. No cloud dependency, low latency (50-200ms), power-efficient.

## Installation

### Unity Package

1. Download Porcupine Unity SDK from Picovoice Console
2. Import the `.unitypackage` into your project
3. Or install via Package Manager with the Picovoice registry

### Access Key

1. Create account at https://console.picovoice.ai
2. Generate an Access Key
3. Store in environment variable: `PICOVOICE_KEY`

## Custom Wake Word

### Using Picovoice Console

1. Go to https://console.picovoice.ai
2. Navigate to Porcupine > Custom Keywords
3. Create keyword: "Hey Claude"
4. Train for Android platform
5. Download `.ppn` model file
6. Place in `Assets/StreamingAssets/porcupine/`

### Built-in Keywords

Porcupine ships with built-in keywords for testing:
- "Alexa", "Hey Google", "Computer", "Jarvis", etc.
- Use for prototyping before creating custom "Hey Claude" keyword

## Unity Integration

### Basic Setup

```csharp
using Pv.Unity;

public class WakeWordListener : MonoBehaviour {
    private PorcupineManager porcupine;

    void Start() {
        try {
            porcupine = PorcupineManager.FromKeywordPaths(
                accessKey: Environment.GetEnvironmentVariable("PICOVOICE_KEY"),
                keywordPaths: new string[] {
                    Path.Combine(Application.streamingAssetsPath,
                        "porcupine/hey-claude_en_android.ppn")
                },
                wakeWordCallback: OnWakeWordDetected,
                sensitivities: new float[] { 0.7f }  // 0.0 to 1.0
            );
            porcupine.Start();
        } catch (PorcupineException e) {
            Debug.LogError($"Porcupine init failed: {e.Message}");
        }
    }

    void OnWakeWordDetected(int keywordIndex) {
        Debug.Log("Wake word detected - starting voice capture");
        // Trigger voice pipeline
        GetComponent<VoiceCapture>().StartListening();
    }

    void OnDestroy() {
        porcupine?.Stop();
        porcupine?.Delete();
    }
}
```

### Sensitivity Tuning

```csharp
// Higher sensitivity = more detections (more false positives)
// Lower sensitivity = fewer detections (more false negatives)
sensitivities: new float[] { 0.7f }  // Recommended starting point

// Noisy VR environment: lower sensitivity to reduce false triggers
sensitivities: new float[] { 0.5f }

// Quiet environment: higher sensitivity for better detection
sensitivities: new float[] { 0.85f }
```

## Quest-Specific Notes

### Android Compatibility

- Porcupine supports Android (Quest's base OS)
- Quest is NOT explicitly certified by Picovoice
- Android ARM64 builds work (IL2CPP compatible)
- Contact Picovoice for official Quest verification

### Microphone Access

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

### Runtime Permission Request

```csharp
#if UNITY_ANDROID && !UNITY_EDITOR
if (!Permission.HasUserAuthorizedPermission(Permission.Microphone)) {
    Permission.RequestUserPermission(Permission.Microphone);
}
#endif
```

### Power Efficiency

- Porcupine runs lightweight DSP on audio frames
- Minimal CPU impact (suitable for VR frame budget)
- Only activates full voice pipeline on wake word detection
- Battery-friendly for extended VR sessions

## Fallback Strategy

If Porcupine has issues on Quest:
1. **Push-to-talk** via controller trigger (always works)
2. **Meta Voice SDK (Wit.ai)** — fully Quest-compatible but cloud-based
3. **Keyword spotting** via Unity's built-in Microphone API (custom implementation)

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No detections | Sensitivity too low | Increase to 0.8+ |
| False triggers | Sensitivity too high | Decrease to 0.5 |
| Crash on init | Missing access key | Set PICOVOICE_KEY env var |
| No microphone | Permission denied | Request RECORD_AUDIO permission |
| Model not found | Wrong path | Check StreamingAssets path on Android |

```

---

## File: unity-vr-dev/skills/voice-pipeline/references/deepgram-integration.md

**Extension:** md
**Language:** markdown
**Size:** 5129 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Deepgram STT Integration

## Overview

Deepgram provides streaming speech-to-text via WebSocket with sub-300ms latency. Audio streams in 100-200ms chunks for real-time transcription.

## WebSocket Connection

### Endpoint

```
wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1
```

### Query Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| encoding | linear16 | 16-bit PCM audio |
| sample_rate | 16000 | 16kHz sample rate |
| channels | 1 | Mono audio |
| model | nova-2 | Latest model (best accuracy) |
| language | en | Language code |
| punctuate | true | Add punctuation |
| interim_results | true | Get partial transcriptions |
| endpointing | 300 | Silence endpoint in ms |

### Full URL

```
wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1&model=nova-2&language=en&punctuate=true&interim_results=true&endpointing=300
```

## NativeWebSocket Implementation

### Connection

```csharp
using NativeWebSocket;

WebSocket deepgramWs;

async Task ConnectDeepgram() {
    string url = "wss://api.deepgram.com/v1/listen?" +
        "encoding=linear16&sample_rate=16000&channels=1" +
        "&model=nova-2&punctuate=true&interim_results=true";

    deepgramWs = new WebSocket(url, new Dictionary<string, string> {
        { "Authorization", $"Token {Environment.GetEnvironmentVariable("DEEPGRAM_KEY")}" }
    });

    deepgramWs.OnOpen += () => Debug.Log("Deepgram connected");

    deepgramWs.OnMessage += (bytes) => {
        string json = System.Text.Encoding.UTF8.GetString(bytes);
        HandleTranscription(json);
    };

    deepgramWs.OnError += (error) => Debug.LogError($"Deepgram error: {error}");
    deepgramWs.OnClose += (code) => Debug.Log($"Deepgram closed: {code}");

    await deepgramWs.Connect();
}
```

### Audio Streaming

```csharp
AudioClip micClip;
int lastSample = 0;

void StartMicrophone() {
    micClip = Microphone.Start(null, true, 10, 16000);
}

void StreamAudio() {
    int currentPos = Microphone.GetPosition(null);
    if (currentPos == lastSample) return;

    int sampleCount;
    if (currentPos > lastSample) {
        sampleCount = currentPos - lastSample;
    } else {
        sampleCount = (micClip.samples - lastSample) + currentPos;
    }

    float[] samples = new float[sampleCount];
    micClip.GetData(samples, lastSample);
    lastSample = currentPos;

    // Convert to 16-bit PCM
    byte[] pcm = new byte[samples.Length * 2];
    for (int i = 0; i < samples.Length; i++) {
        short val = (short)(Mathf.Clamp(samples[i], -1f, 1f) * short.MaxValue);
        pcm[i * 2] = (byte)(val & 0xFF);
        pcm[i * 2 + 1] = (byte)((val >> 8) & 0xFF);
    }

    deepgramWs.Send(pcm);
}

void Update() {
    deepgramWs?.DispatchMessageQueue();  // Required for NativeWebSocket
    if (isListening) StreamAudio();
}
```

### Handling Transcription Results

```csharp
[System.Serializable]
class DeepgramResponse {
    public string type;
    public DeepgramChannel channel;
    public bool is_final;
}

[System.Serializable]
class DeepgramChannel {
    public DeepgramAlternative[] alternatives;
}

[System.Serializable]
class DeepgramAlternative {
    public string transcript;
    public float confidence;
}

void HandleTranscription(string json) {
    var response = JsonUtility.FromJson<DeepgramResponse>(json);

    if (response.channel?.alternatives?.Length > 0) {
        string text = response.channel.alternatives[0].transcript;
        float confidence = response.channel.alternatives[0].confidence;

        if (response.is_final && !string.IsNullOrEmpty(text)) {
            Debug.Log($"Final: {text} ({confidence:P0})");
            ProcessVoiceCommand(text);
        } else if (!string.IsNullOrEmpty(text)) {
            // Interim result — show in UI for feedback
            UpdateInterimDisplay(text);
        }
    }
}
```

### Closing Connection

```csharp
async Task StopListening() {
    Microphone.End(null);

    // Send empty byte array to signal end of audio
    await deepgramWs.Send(new byte[0]);

    await deepgramWs.Close();
}
```

## Latency Optimization

| Technique | Impact |
|-----------|--------|
| Use `interim_results=true` | Show partial text immediately |
| Stream small chunks (100-200ms) | Reduce per-chunk latency |
| Use `endpointing=300` | Detect speech end faster |
| Use `nova-2` model | Best accuracy/speed balance |
| Keep WebSocket open | Avoid reconnection overhead |

## Error Handling

```csharp
deepgramWs.OnError += (error) => {
    Debug.LogError($"Deepgram WebSocket error: {error}");
    // Attempt reconnection
    StartCoroutine(ReconnectAfterDelay(2f));
};

deepgramWs.OnClose += (code) => {
    if (code != WebSocketCloseCode.Normal) {
        Debug.LogWarning($"Unexpected close: {code}");
        StartCoroutine(ReconnectAfterDelay(1f));
    }
};
```

## Quest-Specific Notes

- NativeWebSocket works on Android (Quest base OS)
- Some connectivity issues reported on Quest 2/3 — test thoroughly
- Ensure `INTERNET` permission in AndroidManifest.xml
- `DispatchMessageQueue()` must be called in `Update()` on Quest

```

---

## File: unity-vr-dev/skills/voice-pipeline/references/spatial-audio.md

**Extension:** md
**Language:** markdown
**Size:** 5440 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# Spatial Audio for TTS Output

## Overview

TTS responses are positioned in 3D space so the AI assistant "speaks from" a consistent location in the VR environment.

## AudioSource Configuration

### Basic Spatial Setup

```csharp
public class SpatialTTSPlayer : MonoBehaviour {
    [SerializeField] private AudioSource audioSource;

    void Awake() {
        audioSource = GetComponent<AudioSource>();

        // Full 3D spatialization
        audioSource.spatialBlend = 1.0f;

        // Rolloff settings
        audioSource.rolloffMode = AudioRolloffMode.Logarithmic;
        audioSource.minDistance = 1f;
        audioSource.maxDistance = 15f;

        // Spread for natural sound
        audioSource.spread = 60f;

        // Doppler off (stationary AI assistant)
        audioSource.dopplerLevel = 0f;
    }

    public void PlayResponse(AudioClip clip) {
        audioSource.clip = clip;
        audioSource.Play();
    }
}
```

### Positioning the AI Voice

```csharp
public class AIAssistantPosition : MonoBehaviour {
    [SerializeField] private Transform playerHead;
    [SerializeField] private float distance = 2f;
    [SerializeField] private float height = 0.3f;  // Slightly above eye level

    void Update() {
        // Position in front of player, slightly above
        Vector3 forward = playerHead.forward;
        forward.y = 0;  // Keep on horizontal plane
        forward.Normalize();

        transform.position = playerHead.position
            + forward * distance
            + Vector3.up * height;

        // Face the player
        transform.LookAt(playerHead);
    }
}
```

## Speculative TTS Processing

### Sentence-Boundary Chunking

Start TTS before the full Claude response arrives:

```csharp
public class SpeculativeTTS : MonoBehaviour {
    private Queue<AudioClip> clipQueue = new Queue<AudioClip>();
    private bool isPlaying = false;
    private StringBuilder currentSentence = new StringBuilder();

    public void OnPartialResponse(string partial) {
        currentSentence.Append(partial);
        string text = currentSentence.ToString();

        // Check for sentence boundary
        int boundaryIndex = FindSentenceBoundary(text);
        if (boundaryIndex > 0) {
            string sentence = text.Substring(0, boundaryIndex + 1).Trim();
            currentSentence.Remove(0, boundaryIndex + 1);

            // Send to TTS immediately
            RequestTTS(sentence);
        }
    }

    int FindSentenceBoundary(string text) {
        // Find last sentence-ending punctuation
        for (int i = text.Length - 1; i >= 0; i--) {
            if (text[i] == '.' || text[i] == '!' || text[i] == '?') {
                return i;
            }
        }
        return -1;
    }

    async void RequestTTS(string text) {
        // Call TTS API
        AudioClip clip = await TTSApi.Synthesize(text);
        clipQueue.Enqueue(clip);

        if (!isPlaying) PlayNext();
    }

    void PlayNext() {
        if (clipQueue.Count == 0) {
            isPlaying = false;
            return;
        }

        isPlaying = true;
        AudioClip clip = clipQueue.Dequeue();
        GetComponent<AudioSource>().clip = clip;
        GetComponent<AudioSource>().Play();

        // Play next clip when current finishes
        StartCoroutine(WaitAndPlayNext(clip.length));
    }

    IEnumerator WaitAndPlayNext(float delay) {
        yield return new WaitForSeconds(delay);
        PlayNext();
    }
}
```

### Latency Savings

| Without Speculative | With Speculative |
|--------------------|-----------------|
| Wait for full response | Send first sentence immediately |
| Then generate all TTS | TTS generates during LLM streaming |
| Then play sequentially | Play first sentence while rest generates |
| **Total: LLM + TTS + Play** | **Total: LLM + Play** (TTS overlapped) |

Typical savings: 200-500ms perceived latency reduction.

## Meta Spatial Audio SDK

### Integration with Meta Audio SDK

If using Meta's spatial audio:

```csharp
using Meta.XR.Audio;

// Add MetaXRAudioSource component for HRTF spatialization
var metaAudio = gameObject.AddComponent<MetaXRAudioSource>();
metaAudio.EnableSpatialization = true;
metaAudio.EnableRoomEffect = true;
```

### Room Acoustics

```csharp
// Configure room for natural speech acoustics
var room = FindObjectOfType<MetaXRAudioRoom>();
if (room != null) {
    room.RoomWidth = 4f;
    room.RoomHeight = 3f;
    room.RoomDepth = 4f;
    room.WallMaterial = MetaXRAudioRoom.WallMaterials.CURTAIN_HEAVY;
}
```

## Audio Format

### TTS API Response Format

Most TTS APIs return:
- Format: WAV or MP3
- Sample rate: 22050Hz or 44100Hz
- Channels: Mono (1 channel)

### Converting to AudioClip

```csharp
AudioClip CreateClipFromWav(byte[] wavData) {
    // Skip WAV header (44 bytes)
    int sampleCount = (wavData.Length - 44) / 2;  // 16-bit samples
    float[] samples = new float[sampleCount];

    for (int i = 0; i < sampleCount; i++) {
        short val = BitConverter.ToInt16(wavData, 44 + i * 2);
        samples[i] = val / (float)short.MaxValue;
    }

    AudioClip clip = AudioClip.Create("tts", sampleCount, 1, 22050, false);
    clip.SetData(samples, 0);
    return clip;
}
```

## Performance Considerations

- Audio decoding and playback have minimal CPU cost
- Spatial audio HRTF processing: <0.5ms per source
- Keep total active AudioSources under 32 for Quest
- Use AudioClip pooling to avoid GC from frequent allocations

```

---

## File: unity-vr-dev/skills/adr-management/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 3781 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: adr-management
description: |
  Architecture Decision Record management for VR development knowledge capture.
  Use when: creating ADRs, recording architecture decisions, decision history,
  "create ADR", "architecture decision", status workflow, decision search,
  knowledge capture, wisdom flow, decision catalog.
  Supports: ADR template, numbering, status transitions, semantic search.
allowed-tools: Read, Write, Edit, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# ADR Management

Capture and manage Architecture Decision Records for VR development projects.

## What Are ADRs?

Architecture Decision Records document significant technical decisions with context, rationale, and consequences. They form a "Wisdom Flow" — git-native knowledge capture that persists across team members and time.

## ADR Structure

```markdown
# ADR-NNNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context
What is the technical context? What forces are at play?

## Decision
What is the decision and rationale?

## Consequences
What are the positive and negative impacts?

## References
Links to related ADRs, docs, or external resources.
```

## Status Workflow

```
Proposed → Accepted → [Deprecated | Superseded]
```

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion, not yet finalized |
| Accepted | Active decision, guides implementation |
| Deprecated | No longer relevant (technology removed) |
| Superseded | Replaced by a newer decision (link to new ADR) |

## Numbering Convention

- Sequential 4-digit numbers: `ADR-0001`, `ADR-0002`, etc.
- Never reuse numbers, even for deprecated ADRs
- Store in `docs/adr/` directory

## File Naming

```
docs/adr/
├── ADR-0001-il2cpp-iteration-strategy.md
├── ADR-0002-mcp-transport-protocol.md
├── ADR-0003-wake-word-implementation.md
└── ADR-0004-testing-framework-selection.md
```

Pattern: `ADR-NNNN-kebab-case-title.md`

## Creating an ADR

### Determine Next Number

```bash
# Find highest existing ADR number
ls docs/adr/ADR-*.md 2>/dev/null | sort -t'-' -k2 -n | tail -1
```

### Write the ADR

Use the template from `references/adr-template.md`. Fill in:

1. **Context**: Describe the problem or situation requiring a decision
2. **Decision**: State the decision clearly with rationale
3. **Consequences**: List both positive and negative impacts

### Good ADR Examples

- "Use HTTP instead of gRPC for Quest MCP communication"
- "Adopt Gradle caching for incremental Quest builds"
- "Use Porcupine for wake word with push-to-talk fallback"

## Searching ADRs

### By Status

```bash
grep -l "## Status" docs/adr/ADR-*.md | xargs grep -l "Accepted"
```

### By Topic

```bash
grep -rl "IL2CPP\|il2cpp" docs/adr/
grep -rl "voice\|audio\|speech" docs/adr/
```

### By Date (git log)

```bash
git log --oneline -- docs/adr/
```

## When to Create an ADR

Create an ADR when:
- Choosing between competing technologies (gRPC vs HTTP)
- Adopting a new framework or library
- Changing a significant architectural pattern
- Making a decision with long-term consequences
- Encountering a non-obvious constraint (IL2CPP limitations)

## VR-Specific Decision Areas

| Area | Typical Decisions |
|------|------------------|
| Communication | Transport protocol, serialization format |
| Build | Scripting backend, compression, signing |
| Input | Controller mapping, hand tracking approach |
| Voice | STT provider, wake word technology |
| Testing | Test framework, CI runner, device testing |
| Performance | Frame budget allocation, LOD strategy |

## References

- `references/adr-template.md` — Full ADR template with examples
- `references/decision-catalog.md` — Catalog of common VR decisions

```

---

## File: unity-vr-dev/skills/adr-management/references/adr-template.md

**Extension:** md
**Language:** markdown
**Size:** 4119 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# ADR Template

## Template

```markdown
# ADR-NNNN: [Short descriptive title]

## Status

Proposed

## Date

YYYY-MM-DD

## Context

[Describe the technical context and the problem or situation that requires a decision.
Include relevant constraints, requirements, and forces at play.]

## Decision

[State the decision clearly. Explain the rationale — why this option was chosen
over alternatives. Include specific technologies, versions, or patterns.]

## Alternatives Considered

### [Alternative 1]
- Pros: [list]
- Cons: [list]
- Why rejected: [reason]

### [Alternative 2]
- Pros: [list]
- Cons: [list]
- Why rejected: [reason]

## Consequences

### Positive
- [List positive impacts]

### Negative
- [List negative impacts or trade-offs]

### Neutral
- [List neutral observations]

## References

- [Links to related ADRs, documentation, or external resources]
- Related: ADR-XXXX
```

## Example: IL2CPP Iteration Strategy

```markdown
# ADR-0001: IL2CPP iteration strategy

## Status

Accepted

## Date

2026-01-15

## Context

Quest 2 requires IL2CPP scripting backend for App Lab and Store submission.
IL2CPP performs ahead-of-time compilation, eliminating the Mono JIT runtime.
This means C# hot-reload plugins (Hot Reload, FastScriptReload) cannot work
on device, as they require MonoMod detours which need the Mono JIT.

Development iteration speed is critical for VR development where the
build-test cycle already involves putting on/removing the headset.

## Decision

Use a layered iteration strategy:
1. **Editor hot-reload** — Hot Reload plugins work in Editor (Mono backend)
2. **Asset bundle streaming** — Scenes, prefabs, materials via bundles
3. **Gradle-cached builds** — 30-50% faster incremental device builds
4. **Immersive Debugger** — In-headset debugging compensates for no hot-reload

## Alternatives Considered

### Mono Backend
- Pros: C# hot-reload works
- Cons: Only supports ARMv7, not ARM64; rejected by Meta Store
- Why rejected: Hard platform requirement for ARM64/IL2CPP

### Full Clean Builds Only
- Pros: Simple, no cache management
- Cons: 8-15 minute builds every iteration
- Why rejected: Unacceptable iteration speed

## Consequences

### Positive
- Editor iteration remains fast (milliseconds)
- Asset changes deploy in seconds
- Device builds 30-50% faster with Gradle cache

### Negative
- No C# hot-reload on Quest device
- Two-build-system complexity (Editor + Device)
- Gradle cache can become stale, requiring occasional clean builds

## References

- Meta Quest submission requirements
- Unity IL2CPP documentation
- MonoMod/Hot Reload technical limitations
```

## Example: MCP Transport Protocol

```markdown
# ADR-0002: MCP transport protocol

## Status

Accepted

## Date

2026-01-16

## Context

The plugin needs communication between Claude Code and Unity Editor.
MCP supports multiple transports. Unity-MCP implementations exist for
HTTP, WebSocket, Node.js bridge, and SignalR.

Quest 2 IL2CPP ARM64 builds produce linking errors with gRPC native
libraries: `undefined symbol: grpcsharp_init`.

## Decision

Use HTTP transport on localhost:8080 with JSON-RPC 2.0 protocol.
The Unity MCP server runs inside Unity Editor, not on the Quest device.

## Alternatives Considered

### gRPC
- Pros: Bidirectional streaming, strong typing
- Cons: IL2CPP ARM64 linking errors (hard constraint)
- Why rejected: Not viable on target platform

### WebSocket
- Pros: Bidirectional, persistent connection
- Cons: More complex server setup in Unity
- Why rejected: HTTP sufficient for request-response MCP pattern

### Node.js Bridge
- Pros: Mature MCP SDK, easy extension
- Cons: Extra process to manage, additional dependency
- Why rejected: Direct HTTP simpler for this use case

## Consequences

### Positive
- Simple HTTP request-response pattern
- No native library dependencies
- Works across all Unity versions

### Negative
- No server-initiated push (must poll for updates)
- One request at a time through main thread dispatcher

## References

- gRPC IL2CPP issue: grpcsharp_init linking error
- MCP specification: JSON-RPC 2.0
- Related: ADR-0001
```

```

---

## File: unity-vr-dev/skills/adr-management/references/decision-catalog.md

**Extension:** md
**Language:** markdown
**Size:** 3521 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# VR Development Decision Catalog

Common architecture decisions for Unity VR development targeting Meta Quest.

## Communication

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| MCP Transport | HTTP, WebSocket, Node.js bridge | HTTP (simplest, no native deps) |
| Device Communication | USB ADB, Wireless ADB | Both (USB primary, wireless optional) |
| Cloud API Protocol | REST, WebSocket, gRPC | REST/WebSocket (gRPC not viable) |
| Serialization | JSON, MessagePack, Protobuf | JSON (universal, debuggable) |

## Build & Deploy

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Scripting Backend | IL2CPP, Mono | IL2CPP (required for Quest Store) |
| Architecture | ARM64, ARMv7 | ARM64 (required by Meta) |
| Graphics API | OpenGL ES 3.0, Vulkan | GLES 3.0 (wider compatibility) |
| Build System | Internal, Gradle | Gradle (caching support) |
| Signing | Debug, Custom keystore | Custom for release, debug for dev |

## Input & Interaction

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Input System | Legacy, New Input System | New Input System (XRI compatible) |
| Hand Tracking | Controller only, Hand tracking, Both | Both (controller primary) |
| Interaction Kit | XR Interaction Toolkit, Custom | XRI (Meta-supported) |
| UI Framework | World Space Canvas, Spatial UI | World Space Canvas |

## Voice & Audio

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Wake Word | Porcupine, Meta Voice SDK, Custom | Porcupine (on-device) + PTT fallback |
| STT | Deepgram, Whisper, Meta Voice SDK | Deepgram (low latency streaming) |
| TTS | Deepgram TTS, Azure TTS, ElevenLabs | Deepgram TTS (consistent API) |
| Audio Spatialization | Unity default, Meta Spatial Audio | Meta Spatial Audio (HRTF) |

## Testing & CI

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Test Framework | Unity Test Framework, NUnit standalone | Unity Test Framework (integrated) |
| CI Runner | GameCI, Jenkins, custom | GameCI (GitHub Actions native) |
| Coverage Tool | Code Coverage package, custom | Code Coverage package |
| Device Testing | Manual, Meta Scriptable Testing | Meta Scriptable Testing for automation |
| Performance Testing | Unity Perf Testing, custom | Unity Performance Testing package |

## Networking (Development Host)

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| WSL2 Networking | Mirrored, NAT | Mirrored (Windows 11 22H2+) |
| Docker Networking | Bridge, Host | Bridge with port forwarding |
| MCP Port | Custom, 8080 | 8080 (conventional) |

## Performance

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Target FPS | 72, 90, 120 | 90 FPS (11.1ms budget) |
| Rendering | Single Pass Stereo, Multi Pass | Single Pass Stereo Instanced |
| LOD Strategy | Manual, Automatic | Automatic with manual overrides |
| Texture Format | ASTC, ETC2 | ASTC (native Quest support) |
| Shader Complexity | Standard, Mobile-optimized | Mobile-optimized (URP Lit) |

## Knowledge Management

| Decision | Common Choices | Recommendation |
|----------|---------------|----------------|
| Decision Records | ADR, RFC, Wiki | ADR (git-native, versioned) |
| Documentation | Markdown, Confluence, Notion | Markdown in repo (colocated) |
| API Docs | XML Comments, custom | XML Comments + DocFX |

```

---

## File: unity-vr-dev/skills/wsl2-networking/SKILL.md

**Extension:** md
**Language:** markdown
**Size:** 4118 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
---
name: wsl2-networking
description: |
  WSL2 networking configuration for Unity VR development on Windows.
  Use when: WSL2 networking, mirrored mode, NAT port forwarding,
  Docker networking, Windows firewall, localhost access from WSL,
  "WSL2 setup", "port forwarding", "can't connect from WSL".
  Supports: mirrored mode, NAT mode, Docker Desktop integration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# WSL2 Networking

Configure WSL2 networking for Unity VR development environments on Windows.

## Architecture

Unity Editor runs on Windows. Docker services (if any) run in WSL2. The Quest connects via ADB to the Windows host. MCP communication flows:

```
Quest ← ADB → Windows Host ← MCP HTTP → Unity Editor
                 ↕
              WSL2/Docker (services, build tools)
```

## Networking Modes

### Mirrored Mode (Recommended)

**Requirements**: Windows 11 22H2+, WSL 2.0.4+, Docker Desktop 4.26.0+

WSL2 shares the Windows host network. Services in WSL2 are accessible on `localhost` from Windows and vice versa.

#### Configuration

Create or edit `%USERPROFILE%/.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

Then restart WSL:
```bash
wsl --shutdown
```

#### Verification

```bash
# From WSL2, access Windows localhost
curl http://localhost:8080/health  # Should reach Unity MCP server

# From Windows, access WSL2 services
curl http://localhost:3000  # Should reach WSL2 services
```

See `references/mirrored-mode.md` for advanced mirrored mode configuration.

### NAT Mode (Legacy)

Default WSL2 networking. WSL2 has its own IP address. Port forwarding required to access services across the boundary.

#### Port Forwarding

```powershell
# Forward port from Windows to WSL2
netsh interface portproxy add v4tov4 `
  listenport=8080 listenaddress=0.0.0.0 `
  connectport=8080 connectaddress=$(wsl hostname -I)
```

**Note**: WSL2 IP changes on restart. Use dynamic IP retrieval:

```powershell
$wslIp = (wsl hostname -I).Trim()
netsh interface portproxy add v4tov4 `
  listenport=8080 listenaddress=0.0.0.0 `
  connectport=8080 connectaddress=$wslIp
```

#### Windows Firewall

```powershell
# Allow inbound on forwarded port
New-NetFirewallRule -DisplayName "WSL2 MCP" `
  -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

See `references/port-forwarding.md` for NAT mode automation scripts.

## Docker Desktop Integration

### With Mirrored Mode

Docker Desktop (4.26.0+) works with mirrored networking. Containers bind to localhost and are directly accessible from Windows.

```yaml
# docker-compose.yml
services:
  mcp-service:
    ports:
      - "8080:8080"  # Accessible on localhost from Windows
```

### With NAT Mode

Requires port forwarding for each exposed container port.

## Common Scenarios

### Unity MCP from WSL2

If running tools or scripts in WSL2 that need to reach the Unity MCP server on Windows:

**Mirrored mode**: Just use `localhost:8080`

**NAT mode**: Use the Windows host IP:
```bash
# Get Windows host IP from WSL2
HOST_IP=$(ip route show | grep -i default | awk '{ print $3}')
curl http://$HOST_IP:8080/health
```

### ADB from WSL2

ADB in WSL2 needs to connect to USB devices on Windows:

```bash
# Option 1: Use ADB on Windows via interop
/mnt/c/Users/<user>/AppData/Local/Android/Sdk/platform-tools/adb.exe devices

# Option 2: USB/IP passthrough (usbipd)
# On Windows (PowerShell admin):
usbipd list
usbipd bind --busid <busid>
usbipd attach --wsl --busid <busid>
```

## Troubleshooting

| Issue | Mode | Fix |
|-------|------|-----|
| Can't reach Windows from WSL2 | NAT | Use host IP from `ip route` |
| Can't reach WSL2 from Windows | NAT | Add port forwarding rule |
| Port forwarding stops working | NAT | WSL2 IP changed; re-run script |
| Docker ports not accessible | NAT | Forward each container port |
| Everything works | Mirrored | Correct configuration |

## References

- `references/mirrored-mode.md` — Mirrored mode setup and configuration
- `references/port-forwarding.md` — NAT mode port forwarding automation

```

---

## File: unity-vr-dev/skills/wsl2-networking/references/mirrored-mode.md

**Extension:** md
**Language:** markdown
**Size:** 2608 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# WSL2 Mirrored Networking Mode

## Requirements

- Windows 11 22H2 or later
- WSL 2.0.4 or later
- Docker Desktop 4.26.0 or later (if using Docker)

## Configuration

### .wslconfig

Location: `%USERPROFILE%/.wslconfig` (e.g., `C:\Users\YourName\.wslconfig`)

```ini
[wsl2]
networkingMode=mirrored

# Optional: DNS tunneling for better DNS resolution
dnsTunneling=true

# Optional: auto-proxy for corporate networks
autoProxy=true
```

### Apply Changes

```powershell
# Restart WSL to apply
wsl --shutdown
wsl
```

### Verify

```bash
# From WSL2
ip addr show eth0
# Should show same subnet as Windows host

# Test connectivity to Windows services
curl -s http://localhost:8080/health
```

## How It Works

In mirrored mode, WSL2 shares the Windows host's network interfaces. This means:

- WSL2 services bind to the same `localhost` as Windows
- No port forwarding needed
- No separate IP address for WSL2
- Docker containers are directly accessible on `localhost`

## Benefits Over NAT Mode

| Feature | Mirrored | NAT |
|---------|----------|-----|
| localhost sharing | Yes | No |
| Port forwarding | Not needed | Required |
| IP stability | Same as host | Changes on restart |
| Docker access | Direct | Forwarding needed |
| Setup complexity | Minimal | Moderate |

## Limitations

- Requires Windows 11 22H2+ (not available on Windows 10)
- Some VPN software may conflict with mirrored networking
- Listening on `0.0.0.0` in WSL2 exposes to all host interfaces
- IPv6 behavior may differ from NAT mode

## VPN Compatibility

If using a VPN that causes issues with mirrored mode:

```ini
[wsl2]
networkingMode=mirrored

# Exclude VPN interfaces
networkingMode.excludedInterfaces={"name": "VPN Interface Name"}
```

## Docker Desktop Configuration

Ensure Docker Desktop is configured for WSL2 backend:

1. Docker Desktop > Settings > General > Use WSL 2 based engine: ✓
2. Settings > Resources > WSL Integration > Enable for your distro
3. Restart Docker Desktop after changing `.wslconfig`

### Verify Docker Networking

```bash
# From WSL2
docker run --rm -p 8081:80 nginx
# From Windows browser: http://localhost:8081 should show nginx
```

## Firewall Notes

With mirrored mode, Windows Firewall rules apply to WSL2 traffic. If a service in WSL2 is blocked:

```powershell
# Allow specific port
New-NetFirewallRule -DisplayName "WSL2 Service" `
  -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

## Rollback to NAT Mode

If mirrored mode causes issues:

```ini
[wsl2]
# Comment out or remove networkingMode
# networkingMode=mirrored
```

```powershell
wsl --shutdown
wsl
```

```

---

## File: unity-vr-dev/skills/wsl2-networking/references/port-forwarding.md

**Extension:** md
**Language:** markdown
**Size:** 4135 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# WSL2 NAT Mode Port Forwarding

## Overview

In NAT mode, WSL2 has its own IP address on a virtual network. Port forwarding bridges Windows and WSL2 network namespaces.

## Manual Port Forwarding

### Add Forward Rule

```powershell
# Get WSL2 IP
$wslIp = (wsl hostname -I).Trim()

# Forward port
netsh interface portproxy add v4tov4 `
  listenport=8080 `
  listenaddress=0.0.0.0 `
  connectport=8080 `
  connectaddress=$wslIp
```

### List Active Rules

```powershell
netsh interface portproxy show all
```

### Remove Forward Rule

```powershell
netsh interface portproxy delete v4tov4 `
  listenport=8080 `
  listenaddress=0.0.0.0
```

### Remove All Rules

```powershell
netsh interface portproxy reset
```

## Windows Firewall

Port forwarding requires firewall rules for inbound traffic:

```powershell
# Allow specific port
New-NetFirewallRule `
  -DisplayName "WSL2 Port 8080" `
  -Direction Inbound `
  -LocalPort 8080 `
  -Protocol TCP `
  -Action Allow

# Allow port range
New-NetFirewallRule `
  -DisplayName "WSL2 Dev Ports" `
  -Direction Inbound `
  -LocalPort 8080-8090 `
  -Protocol TCP `
  -Action Allow
```

### Remove Firewall Rule

```powershell
Remove-NetFirewallRule -DisplayName "WSL2 Port 8080"
```

## Automation Script

Since WSL2 IP changes on restart, automate port forwarding:

### PowerShell Script

```powershell
# setup-wsl-forwarding.ps1
# Run as Administrator

param(
    [int[]]$Ports = @(8080, 3000, 5000)
)

$wslIp = (wsl hostname -I).Trim()
Write-Host "WSL2 IP: $wslIp"

foreach ($port in $Ports) {
    # Remove existing rule
    netsh interface portproxy delete v4tov4 `
        listenport=$port listenaddress=0.0.0.0 2>$null

    # Add new rule
    netsh interface portproxy add v4tov4 `
        listenport=$port `
        listenaddress=0.0.0.0 `
        connectport=$port `
        connectaddress=$wslIp

    Write-Host "Forwarded port $port -> ${wslIp}:${port}"

    # Ensure firewall rule exists
    $ruleName = "WSL2 Port $port"
    $existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    if (-not $existing) {
        New-NetFirewallRule `
            -DisplayName $ruleName `
            -Direction Inbound `
            -LocalPort $port `
            -Protocol TCP `
            -Action Allow | Out-Null
        Write-Host "Created firewall rule: $ruleName"
    }
}

Write-Host "`nActive port forwards:"
netsh interface portproxy show all
```

### Run at Startup

Create a scheduled task to run on WSL start:

```powershell
# Create scheduled task (run as admin)
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File C:\Scripts\setup-wsl-forwarding.ps1"

$trigger = New-ScheduledTaskTrigger -AtLogon

Register-ScheduledTask `
    -TaskName "WSL2 Port Forwarding" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest
```

## Accessing Windows from WSL2

To reach Windows services from inside WSL2:

```bash
# Get Windows host IP
HOST_IP=$(ip route show | grep -i default | awk '{ print $3}')

# Access Unity MCP server on Windows
curl http://$HOST_IP:8080/health

# Or use /etc/resolv.conf nameserver (same as host IP)
HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{ print $2}')
```

## Common Ports for VR Development

| Port | Service | Direction |
|------|---------|-----------|
| 8080 | Unity MCP Server | WSL2 → Windows |
| 5555 | ADB Wireless | Windows → Quest |
| 3000 | Dev server | WSL2 → Windows |
| 5037 | ADB Server | Both |

## Troubleshooting

### Port Forward Not Working

```powershell
# Verify WSL2 is running
wsl --list --verbose

# Verify WSL2 IP is reachable
ping $(wsl hostname -I)

# Check port is listening in WSL2
wsl ss -tlnp | grep 8080

# Check Windows port forwarding
netsh interface portproxy show all
```

### IP Changed After Restart

Re-run the automation script. The WSL2 IP changes every time WSL restarts.

### Connection Refused

1. Verify the service is running in WSL2
2. Verify the service binds to `0.0.0.0` (not just `127.0.0.1`)
3. Check Windows Firewall rules
4. Check port forwarding target IP matches current WSL2 IP

```

---

## File: unity-vr-dev/hooks/hooks.json

**Extension:** json
**Language:** json
**Size:** 800 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "description": "Unity VR Dev validation and automation hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-adb-connection.py",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-build-config.py",
            "timeout": 15
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/post-build-report.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}

```

---

## File: unity-vr-dev/hooks/scripts/check-adb-connection.py

**Extension:** py
**Language:** python
**Size:** 2384 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```python
#!/usr/bin/env python3
"""Pre-deploy hook: Verify ADB device is connected before deployment commands.

Exit codes:
  0 - ADB device connected or command is not a deployment command
  2 - Block: deployment command detected but no ADB device connected
  1 - Non-blocking error (ADB not found, etc.)
"""

import json
import os
import subprocess
import sys


def get_tool_input():
    """Read tool input from CLAUDE_TOOL_INPUT environment variable."""
    tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input)
    except json.JSONDecodeError:
        return {}


def is_deployment_command(command: str) -> bool:
    """Check if the bash command involves ADB deployment."""
    deploy_keywords = [
        "adb install",
        "adb push",
        "adb shell am start",
        "adb shell pm",
        "deploy-to-device",
        "deploy-quest",
    ]
    command_lower = command.lower()
    return any(kw in command_lower for kw in deploy_keywords)


def check_adb_devices() -> bool:
    """Check if at least one ADB device is connected."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        lines = result.stdout.strip().split("\n")
        # Filter out header and empty lines
        devices = [
            line for line in lines[1:] if line.strip() and "device" in line
        ]
        return len(devices) > 0
    except FileNotFoundError:
        print("Warning: ADB not found in PATH", file=sys.stderr)
        return False
    except subprocess.TimeoutExpired:
        print("Warning: ADB command timed out", file=sys.stderr)
        return False


def main():
    tool_input = get_tool_input()
    command = tool_input.get("command", "")

    # Only check for deployment commands
    if not is_deployment_command(command):
        sys.exit(0)

    # Check ADB connection
    if check_adb_devices():
        sys.exit(0)
    else:
        print(
            "BLOCKED: No ADB device connected. "
            "Connect a Quest device via USB or wireless ADB before deploying.\n"
            "  USB: Connect cable and authorize on headset\n"
            "  Wireless: adb tcpip 5555 && adb connect <device-ip>:5555",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()

```

---

## File: unity-vr-dev/hooks/scripts/validate-build-config.py

**Extension:** py
**Language:** python
**Size:** 3498 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```python
#!/usr/bin/env python3
"""Pre-build hook: Validate Unity/XR SDK configuration before build commands.

Exit codes:
  0 - Not a build command, or validation passed
  2 - Block: critical build misconfiguration detected
  1 - Non-blocking warning
"""

import json
import os
import subprocess
import sys


def get_tool_input():
    """Read tool input from CLAUDE_TOOL_INPUT environment variable."""
    tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "{}")
    try:
        return json.loads(tool_input)
    except json.JSONDecodeError:
        return {}


def is_build_command(command: str) -> bool:
    """Check if the bash command involves Unity builds."""
    build_keywords = [
        "buildplayer",
        "build-quest",
        "executemethod",
        "-batchmode",
        "buildpipeline",
        "build_quest",
        "gradlew",
    ]
    command_lower = command.lower()
    return any(kw in command_lower for kw in build_keywords)


def check_android_sdk() -> tuple[bool, str]:
    """Verify Android SDK is available."""
    android_home = os.environ.get("ANDROID_HOME") or os.environ.get(
        "ANDROID_SDK_ROOT"
    )
    if not android_home:
        return False, "ANDROID_HOME or ANDROID_SDK_ROOT not set"
    if not os.path.isdir(android_home):
        return False, f"Android SDK directory not found: {android_home}"
    return True, "OK"


def check_java() -> tuple[bool, str]:
    """Verify Java is available (required for Gradle builds)."""
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        # Java prints version to stderr
        version_output = result.stderr or result.stdout
        return True, version_output.split("\n")[0].strip()
    except FileNotFoundError:
        return False, "Java not found in PATH"
    except subprocess.TimeoutExpired:
        return False, "Java version check timed out"


def check_unity_project() -> tuple[bool, str]:
    """Check if we're in or near a Unity project."""
    # Look for ProjectSettings directory (marker of Unity project)
    search_dirs = [
        os.getcwd(),
        os.path.dirname(os.getcwd()),
    ]
    for d in search_dirs:
        if os.path.isdir(os.path.join(d, "ProjectSettings")):
            return True, d
    return False, "No Unity project found in current or parent directory"


def main():
    tool_input = get_tool_input()
    command = tool_input.get("command", "")

    # Only validate build commands
    if not is_build_command(command):
        sys.exit(0)

    warnings = []
    errors = []

    # Check Android SDK
    sdk_ok, sdk_msg = check_android_sdk()
    if not sdk_ok:
        warnings.append(f"Android SDK: {sdk_msg}")

    # Check Java
    java_ok, java_msg = check_java()
    if not java_ok:
        warnings.append(f"Java: {java_msg}")

    # Check Unity project
    project_ok, project_msg = check_unity_project()
    if not project_ok:
        errors.append(f"Unity project: {project_msg}")

    # Report results
    if errors:
        print(
            "BLOCKED: Build configuration errors:\n"
            + "\n".join(f"  - {e}" for e in errors),
            file=sys.stderr,
        )
        sys.exit(2)

    if warnings:
        print(
            "Build warnings (non-blocking):\n"
            + "\n".join(f"  - {w}" for w in warnings),
            file=sys.stderr,
        )
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

```

---

## File: unity-vr-dev/hooks/scripts/post-build-report.sh

**Extension:** sh
**Language:** bash
**Size:** 1603 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```bash
#!/usr/bin/env bash
# Post-build hook: Generate APK size and build duration metrics.
# Runs after Bash tool use to detect and report build outputs.
#
# Exit codes:
#   0 - Always (non-blocking informational hook)

set -euo pipefail

# Read tool input
TOOL_INPUT="${CLAUDE_TOOL_INPUT:-{}}"
COMMAND=$(echo "$TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('command',''))" 2>/dev/null || echo "")

# Only process build-related commands
case "$COMMAND" in
  *buildplayer*|*build-quest*|*executeMethod*|*BuildPlayer*|*gradlew*|*"adb install"*)
    ;;
  *)
    exit 0
    ;;
esac

# Read tool output for build results
TOOL_OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# Look for APK files in common build output locations
APK_PATHS=(
  "Builds/*.apk"
  "Build/*.apk"
  "build/*.apk"
  "*.apk"
)

FOUND_APK=""
for pattern in "${APK_PATHS[@]}"; do
  # shellcheck disable=SC2086
  for apk in $pattern; do
    if [ -f "$apk" ]; then
      FOUND_APK="$apk"
      break 2
    fi
  done
done

if [ -n "$FOUND_APK" ]; then
  # Get APK size
  APK_SIZE=$(du -sh "$FOUND_APK" | cut -f1)
  APK_SIZE_BYTES=$(stat -f%z "$FOUND_APK" 2>/dev/null || stat -c%s "$FOUND_APK" 2>/dev/null || echo "unknown")

  # Get modification time (proxy for build completion)
  MOD_TIME=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$FOUND_APK" 2>/dev/null || \
             stat -c "%y" "$FOUND_APK" 2>/dev/null | cut -d. -f1 || \
             echo "unknown")

  echo "=== Build Report ==="
  echo "APK: $FOUND_APK"
  echo "Size: $APK_SIZE ($APK_SIZE_BYTES bytes)"
  echo "Built: $MOD_TIME"
  echo "===================="
fi

exit 0

```

---

## File: unity-vr-dev/schemas/build-config.schema.json

**Extension:** json
**Language:** json
**Size:** 4937 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://unity-vr-dev.plugin/schemas/build-config.schema.json",
  "title": "Quest Build Configuration",
  "description": "Configuration schema for Meta Quest IL2CPP builds",
  "type": "object",
  "required": [
    "projectName",
    "buildTarget",
    "scriptingBackend",
    "targetArchitecture",
    "outputPath"
  ],
  "properties": {
    "projectName": {
      "type": "string",
      "description": "Unity project name",
      "minLength": 1
    },
    "buildTarget": {
      "type": "string",
      "enum": [
        "Android"
      ],
      "description": "Build target platform (Quest requires Android)"
    },
    "scriptingBackend": {
      "type": "string",
      "enum": [
        "IL2CPP"
      ],
      "description": "Scripting backend (Quest requires IL2CPP)"
    },
    "targetArchitecture": {
      "type": "string",
      "enum": [
        "ARM64"
      ],
      "description": "Target architecture (Quest requires ARM64)"
    },
    "graphicsApi": {
      "type": "string",
      "enum": [
        "OpenGLES3",
        "Vulkan"
      ],
      "default": "OpenGLES3",
      "description": "Graphics API"
    },
    "colorSpace": {
      "type": "string",
      "enum": [
        "Linear",
        "Gamma"
      ],
      "default": "Linear",
      "description": "Color space (Linear recommended for VR)"
    },
    "minSdkVersion": {
      "type": "integer",
      "minimum": 29,
      "default": 29,
      "description": "Minimum Android SDK version (Quest 2 requires 29+)"
    },
    "buildSystem": {
      "type": "string",
      "enum": [
        "Gradle",
        "Internal"
      ],
      "default": "Gradle",
      "description": "Android build system"
    },
    "gradleCaching": {
      "type": "boolean",
      "default": true,
      "description": "Enable Gradle build caching for faster incremental builds"
    },
    "outputPath": {
      "type": "string",
      "description": "Output APK file path",
      "pattern": ".*\\.apk$"
    },
    "scenes": {
      "type": "array",
      "items": {
        "type": "string",
        "description": "Scene asset path"
      },
      "minItems": 1,
      "description": "Scenes to include in build"
    },
    "keystore": {
      "type": "object",
      "properties": {
        "useCustom": {
          "type": "boolean",
          "default": false,
          "description": "Use custom keystore for signing"
        },
        "path": {
          "type": "string",
          "description": "Path to keystore file"
        },
        "alias": {
          "type": "string",
          "description": "Key alias name"
        }
      },
      "description": "Keystore signing configuration"
    },
    "buildOptions": {
      "type": "object",
      "properties": {
        "development": {
          "type": "boolean",
          "default": true,
          "description": "Development build with debug symbols"
        },
        "allowDebugging": {
          "type": "boolean",
          "default": true,
          "description": "Allow script debugging"
        },
        "connectWithProfiler": {
          "type": "boolean",
          "default": false,
          "description": "Auto-connect Unity Profiler"
        },
        "stripEngineCode": {
          "type": "boolean",
          "default": false,
          "description": "Strip unused engine code for smaller APK"
        }
      },
      "description": "Build options"
    },
    "xr": {
      "type": "object",
      "properties": {
        "sdkVersion": {
          "type": "string",
          "description": "Meta XR SDK version (e.g., v74)"
        },
        "interactionToolkit": {
          "type": "boolean",
          "default": true,
          "description": "Include XR Interaction Toolkit"
        },
        "handTracking": {
          "type": "boolean",
          "default": false,
          "description": "Enable hand tracking support"
        },
        "passthrough": {
          "type": "boolean",
          "default": false,
          "description": "Enable passthrough/mixed reality"
        }
      },
      "description": "XR-specific settings"
    },
    "deployment": {
      "type": "object",
      "properties": {
        "autoInstall": {
          "type": "boolean",
          "default": true,
          "description": "Auto-install APK after build"
        },
        "autoLaunch": {
          "type": "boolean",
          "default": true,
          "description": "Auto-launch app after install"
        },
        "packageName": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)+$",
          "description": "Android package name"
        },
        "activityName": {
          "type": "string",
          "description": "Main activity class name"
        }
      },
      "description": "Post-build deployment settings"
    }
  },
  "additionalProperties": false
}

```

---

## File: unity-vr-dev/schemas/mcp-response.schema.json

**Extension:** json
**Language:** json
**Size:** 4786 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://unity-vr-dev.plugin/schemas/mcp-response.schema.json",
  "title": "MCP Response",
  "description": "JSON-RPC 2.0 response schema for Unity MCP server",
  "oneOf": [
    {
      "title": "Success Response",
      "type": "object",
      "required": [
        "jsonrpc",
        "result",
        "id"
      ],
      "properties": {
        "jsonrpc": {
          "type": "string",
          "const": "2.0"
        },
        "result": {
          "type": "object",
          "properties": {
            "content": {
              "type": "array",
              "items": {
                "type": "object",
                "required": [
                  "type"
                ],
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": [
                      "text",
                      "image",
                      "resource"
                    ]
                  },
                  "text": {
                    "type": "string",
                    "description": "Text content (when type is 'text')"
                  },
                  "data": {
                    "type": "string",
                    "description": "Base64 encoded data (when type is 'image')"
                  },
                  "mimeType": {
                    "type": "string",
                    "description": "MIME type for image content"
                  },
                  "uri": {
                    "type": "string",
                    "description": "Resource URI (when type is 'resource')"
                  }
                }
              }
            },
            "tools": {
              "type": "array",
              "items": {
                "type": "object",
                "required": [
                  "name",
                  "description"
                ],
                "properties": {
                  "name": {
                    "type": "string",
                    "pattern": "^[a-z][a-z0-9-]*$",
                    "description": "Tool identifier in kebab-case"
                  },
                  "description": {
                    "type": "string",
                    "description": "Human-readable tool description"
                  },
                  "inputSchema": {
                    "type": "object",
                    "description": "JSON Schema for tool input parameters"
                  }
                }
              },
              "description": "Tool list (for tools/list response)"
            },
            "resources": {
              "type": "array",
              "items": {
                "type": "object",
                "required": [
                  "uri",
                  "name"
                ],
                "properties": {
                  "uri": {
                    "type": "string",
                    "description": "Resource URI"
                  },
                  "name": {
                    "type": "string",
                    "description": "Human-readable resource name"
                  },
                  "description": {
                    "type": "string"
                  },
                  "mimeType": {
                    "type": "string"
                  }
                }
              },
              "description": "Resource list (for resources/list response)"
            }
          }
        },
        "id": {
          "type": [
            "integer",
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    },
    {
      "title": "Error Response",
      "type": "object",
      "required": [
        "jsonrpc",
        "error",
        "id"
      ],
      "properties": {
        "jsonrpc": {
          "type": "string",
          "const": "2.0"
        },
        "error": {
          "type": "object",
          "required": [
            "code",
            "message"
          ],
          "properties": {
            "code": {
              "type": "integer",
              "description": "JSON-RPC error code",
              "enum": [
                -32700,
                -32600,
                -32601,
                -32602,
                -32603,
                -32000
              ]
            },
            "message": {
              "type": "string",
              "description": "Human-readable error message"
            },
            "data": {
              "description": "Additional error data"
            }
          }
        },
        "id": {
          "type": [
            "integer",
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    }
  ]
}

```

---

## File: unity-vr-dev/templates/adr-template.md

**Extension:** md
**Language:** markdown
**Size:** 765 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```markdown
# ADR-NNNN: [Title]

## Status

Proposed

## Date

YYYY-MM-DD

## Context

[Describe the technical context and the problem or situation that requires a decision.
What forces are at play? What constraints exist?]

## Decision

[State the decision clearly. Explain the rationale — why this option was chosen
over alternatives.]

## Alternatives Considered

### [Alternative 1]

- **Pros**: [list benefits]
- **Cons**: [list drawbacks]
- **Why rejected**: [reason]

### [Alternative 2]

- **Pros**: [list benefits]
- **Cons**: [list drawbacks]
- **Why rejected**: [reason]

## Consequences

### Positive

- [List positive impacts]

### Negative

- [List negative impacts or trade-offs]

## References

- [Links to related ADRs, documentation, or external resources]

```

---

## File: unity-vr-dev/templates/build-config.json

**Extension:** json
**Language:** json
**Size:** 945 bytes
**Created:** 2026-01-31
**Modified:** 2026-01-31

### Code

```json
{
  "$schema": "../schemas/build-config.schema.json",
  "projectName": "MyVRApp",
  "buildTarget": "Android",
  "scriptingBackend": "IL2CPP",
  "targetArchitecture": "ARM64",
  "graphicsApi": "OpenGLES3",
  "colorSpace": "Linear",
  "minSdkVersion": 29,
  "buildSystem": "Gradle",
  "gradleCaching": true,
  "outputPath": "Builds/QuestApp.apk",
  "scenes": [
    "Assets/Scenes/Main.unity",
    "Assets/Scenes/Menu.unity"
  ],
  "keystore": {
    "useCustom": false,
    "path": "",
    "alias": ""
  },
  "buildOptions": {
    "development": true,
    "allowDebugging": true,
    "connectWithProfiler": false,
    "stripEngineCode": false
  },
  "xr": {
    "sdkVersion": "v74",
    "interactionToolkit": true,
    "handTracking": false,
    "passthrough": false
  },
  "deployment": {
    "autoInstall": true,
    "autoLaunch": true,
    "packageName": "com.company.myvrapp",
    "activityName": "com.unity3d.player.UnityPlayerActivity"
  }
}

```

---
