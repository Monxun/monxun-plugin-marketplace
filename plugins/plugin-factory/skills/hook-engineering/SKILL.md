---
name: hook-engineering
description: |
  Expert guidance for creating Claude Code hooks and lifecycle automation.
  Use when: hooks, event hooks, PreToolUse, PostToolUse, exit codes,
  hook scripts, lifecycle events, validation hooks, "create hook",
  "add hook", hook configuration, hooks.json, Stop hook, SessionStart.
  Supports: all 12 event types, command hooks, prompt hooks, exit codes.
allowed-tools: Read, Write, Edit, Bash
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Hook Engineering Skill

Create Claude Code hooks for lifecycle automation, validation, and intelligent workflow control.

## hooks.json Structure

```json
{
  "description": "Hook description",
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/script.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

## All 12 Event Types

| Event | Matcher | When Fires |
|-------|---------|------------|
| PreToolUse | Tool name | Before tool execution |
| PostToolUse | Tool name | After successful execution |
| PostToolUseFailure | Tool name | After failed execution |
| PermissionRequest | Tool name | When permission shown |
| UserPromptSubmit | (none) | When user submits prompt |
| Notification | Type | When notification sent |
| Stop | (none) | When Claude stops |
| SubagentStart | Agent name | When subagent starts |
| SubagentStop | Agent name | When subagent stops |
| SessionStart | Source | At session start |
| SessionEnd | Reason | At session end |
| PreCompact | Trigger | Before compaction |

## Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Continue, parse JSON stdout |
| 2 | Block | Stop execution, stderr to Claude |
| Other | Non-blocking | Continue, stderr to user |

## Quick Start Templates

### Validation Hook (PreToolUse)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.py"
          }
        ]
      }
    ]
  }
}
```

### Formatting Hook (PostToolUse)
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

### Quality Gate (Stop)
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/quality-gate.py"
          }
        ]
      }
    ]
  }
}
```

## Python Script Template

```python
#!/usr/bin/env python3
import json
import sys

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Validation logic
    if should_block(tool_input):
        print("Error message", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Bash Script Template

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Validation logic
if [[ "$FILE_PATH" == *"forbidden"* ]]; then
    echo "Blocked: forbidden path" >&2
    exit 2
fi

exit 0
```

## Detailed References

- [Event Types Reference](references/event-types.md)
- [Exit Codes Guide](references/exit-codes.md)
- [JSON Control Patterns](references/json-control.md)
- [Security Patterns](references/security-patterns.md)

## Best Practices

- Always use `${CLAUDE_PLUGIN_ROOT}` for paths
- Use stderr for error messages
- Set appropriate timeouts
- Test exit codes thoroughly
