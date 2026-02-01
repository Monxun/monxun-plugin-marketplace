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
