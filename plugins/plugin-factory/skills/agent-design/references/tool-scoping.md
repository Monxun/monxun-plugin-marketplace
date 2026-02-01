# Tool Scoping Guide

How to configure tool access for agents.

## Available Tools

| Tool | Purpose |
|------|---------|
| Read | File reading |
| Write | File creation |
| Edit | File modification |
| Bash | Shell commands |
| Grep | Content search |
| Glob | File pattern matching |
| WebSearch | Web search |
| WebFetch | URL fetching |
| Task | Subagent delegation |
| NotebookEdit | Jupyter editing |

## Scoping Methods

### Allowlist (tools)
Explicitly list allowed tools:

```yaml
tools: Read, Grep, Glob
```

Agent can ONLY use Read, Grep, Glob.

### Denylist (disallowedTools)
Explicitly deny tools:

```yaml
disallowedTools: Write, Edit, Bash
```

Agent inherits all tools EXCEPT Write, Edit, Bash.

### Combined
Use both for precise control:

```yaml
tools: Read, Write, Edit, Bash
disallowedTools: WebSearch
```

### Inherit (default)
Omit both fields to inherit from parent conversation.

## Common Patterns

### Read-Only Agent
```yaml
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash, Task
permissionMode: plan
```

Use for: Research, exploration, analysis

### Code Editor Agent
```yaml
tools: Read, Write, Edit, Bash
```

Use for: Code modifications, file creation

### Research Agent
```yaml
tools: Read, Grep, Glob, WebSearch
disallowedTools: Write, Edit
permissionMode: plan
```

Use for: Documentation research, web lookup

### Orchestrator Agent
```yaml
tools: Task, Read, Bash
```

Use for: Coordinating other agents

### Validator Agent
```yaml
tools: Read, Bash, Grep
disallowedTools: Write, Edit
model: haiku
```

Use for: Testing, validation without modifications

### Full Access Agent
```yaml
# Omit tools field to inherit all
```

Use for: General-purpose tasks

## Bash Command Patterns

Restrict Bash to specific commands:

```yaml
tools:
  - Read
  - Bash(git *)      # Only git commands
  - Bash(npm run:*)  # Only npm run commands
  - Bash(pytest *)   # Only pytest
```

Pattern syntax:
- `*` matches any characters
- Patterns are case-sensitive

## MCP Tool Scoping

MCP tools appear as `mcp__<server>__<tool>`:

```yaml
tools:
  - Read
  - mcp__database__query  # Specific MCP tool
```

Or allow all from a server:
```yaml
tools:
  - Read
  - mcp__database__*
```

## Security Considerations

### Principle of Least Privilege
Only grant tools necessary for the task.

### Dangerous Combinations
Be careful with:
- `Bash` - Can execute arbitrary commands
- `Write` + `Bash` - Can create and execute scripts
- `bypassPermissions` + any tool - No safety checks

### Recommended Restrictions

For untrusted contexts:
```yaml
tools: Read, Grep, Glob
disallowedTools: Bash, Write, Edit, Task
permissionMode: dontAsk
```

## Validation

Test tool access:

```bash
# Create test agent
cat > test-agent.md << 'EOF'
---
name: test-agent
description: Test tool access
tools: Read, Grep
disallowedTools: Write
---
Test agent
EOF

# Agent should:
# - Be able to Read
# - Be able to Grep
# - NOT be able to Write
```
