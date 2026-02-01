---
name: agent-design
description: |
  Expert guidance for designing Claude Code custom subagents.
  Use when: creating agents, subagent design, agent frontmatter,
  tool scoping, permission modes, agent orchestration, "create agent",
  "build agent", agent template, delegation patterns.
  Supports: frontmatter schema, tool restrictions, skill injection.
allowed-tools: Read, Write, Edit, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Agent Design Skill

Design effective Claude Code custom subagents with proper frontmatter, tool scoping, and orchestration patterns.

## Agent Structure

```markdown
---
name: agent-name
description: |
  When Claude should delegate to this agent.
  Use when: specific criteria, task types.

tools: Read, Write, Edit
disallowedTools: WebSearch
model: sonnet
permissionMode: default
skills: skill-one, skill-two
---

# Agent Title

You are a [role]. Your purpose is to [objective].

## Tasks
1. Task one
2. Task two

## Output Format
Expected structure...

## Constraints
- DO NOT...
- ALWAYS...
```

## Frontmatter Quick Reference

| Field | Required | Values |
|-------|----------|--------|
| `name` | Yes | kebab-case identifier |
| `description` | Yes | Delegation criteria |
| `tools` | No | Tool list (inherit if omitted) |
| `disallowedTools` | No | Explicitly denied tools |
| `model` | No | sonnet/opus/haiku/inherit |
| `permissionMode` | No | default/acceptEdits/dontAsk/bypassPermissions/plan |
| `skills` | No | Comma-separated skill names |
| `hooks` | No | PreToolUse/PostToolUse/Stop |

## Model Selection

| Model | Use Case | Cost | Speed |
|-------|----------|------|-------|
| haiku | Validation, clarification | Low | Fast |
| sonnet | General tasks, coding | Medium | Balanced |
| opus | Complex reasoning | High | Slower |
| inherit | Match parent | Varies | Varies |

## Tool Scoping Patterns

### Read-Only Agent
```yaml
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
permissionMode: plan
```

### Code Modification Agent
```yaml
tools: Read, Write, Edit, Bash
permissionMode: default
```

### Research Agent
```yaml
tools: Read, Grep, Glob, WebSearch
disallowedTools: Write, Edit
permissionMode: plan
```

### Orchestrator Agent
```yaml
tools: Task, Read, Bash
model: sonnet
```

## Permission Modes

| Mode | Behavior |
|------|----------|
| default | Normal permission prompts |
| acceptEdits | Auto-approve file edits |
| dontAsk | Auto-deny (allowed tools work) |
| bypassPermissions | Skip all checks (caution!) |
| plan | Read-only exploration |

## Description Guidelines

Good description includes:
- What the agent specializes in
- When to delegate to it
- Specific task types

```yaml
description: |
  Validation specialist for plugin testing.
  Use when: validating plugins, testing components,
  running integration tests, quality checks.
  Automatically invoked after construction phase.
```

## Detailed References

- [Frontmatter Schema](references/frontmatter-schema.md)
- [Tool Scoping Guide](references/tool-scoping.md)
- [Orchestration Patterns](references/orchestration-patterns.md)
