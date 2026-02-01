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
