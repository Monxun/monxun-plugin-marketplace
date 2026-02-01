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
