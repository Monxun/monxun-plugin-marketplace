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
