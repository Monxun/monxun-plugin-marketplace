# JSON Control Patterns

Advanced JSON output patterns for hook control.

## Overview

Hooks can return JSON to stdout (with exit 0) to control Claude's behavior.

## Common Fields

All hook types support these optional fields:

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "systemMessage": "string"
}
```

| Field | Type | Purpose |
|-------|------|---------|
| `continue` | bool | false stops Claude |
| `stopReason` | string | Message when stopping |
| `suppressOutput` | bool | Hide from transcript |
| `systemMessage` | string | Warning to user |

## PreToolUse Control

### Allow Tool
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved: safe operation"
  }
}
```

### Deny Tool
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked: security policy"
  }
}
```

### Ask User
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Please confirm this operation"
  }
}
```

### Modify Input
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "file_path": "/safe/path/file.txt",
      "content": "modified content"
    }
  }
}
```

### Complete Example
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

# Auto-approve documentation files
if file_path.endswith((".md", ".txt", ".json")):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Auto-approved: documentation file"
        },
        "suppressOutput": True
    }
    print(json.dumps(output))
    sys.exit(0)

# Ask for other files
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Non-doc file - please confirm"
    }
}
print(json.dumps(output))
sys.exit(0)
```

## PermissionRequest Control

### Allow Permission
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

### Deny Permission
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "This command is not allowed",
      "interrupt": true
    }
  }
}
```

## PostToolUse Control

### Inject Context
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Note: This file was auto-formatted"
  }
}
```

### Block with Feedback
```json
{
  "decision": "block",
  "reason": "Linting failed - please fix errors",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Errors found:\n- Line 10: unused variable"
  }
}
```

### Complete Example
```python
#!/usr/bin/env python3
import json
import sys
import subprocess

input_data = json.load(sys.stdin)
file_path = input_data.get("tool_input", {}).get("file_path", "")

# Run linter on written files
if file_path.endswith((".py", ".js", ".ts")):
    result = subprocess.run(
        ["eslint", file_path] if file_path.endswith(".js") else ["ruff", file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        output = {
            "decision": "block",
            "reason": f"Linting failed for {file_path}",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": result.stdout
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

## UserPromptSubmit Control

### Block Prompt
```json
{
  "decision": "block",
  "reason": "Prompt contains sensitive information"
}
```

### Add Context
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Current time: 2026-01-15 12:00:00"
  }
}
```

### Plain Text Alternative
For simple context, just print to stdout:
```bash
echo "Current directory: $(pwd)"
echo "Git branch: $(git branch --show-current)"
exit 0
```

## Stop Control

### Allow Stop
```json
{}
```
Or just exit 0 with no output.

### Block Stop
```json
{
  "decision": "block",
  "reason": "Cannot stop: tests not run yet"
}
```

### Complete Example
```python
#!/usr/bin/env python3
import json
import sys
import os

input_data = json.load(sys.stdin)

# Prevent infinite loops
if input_data.get("stop_hook_active", False):
    sys.exit(0)

# Check for required files
required = ["README.md", ".claude-plugin/plugin.json"]
missing = [f for f in required if not os.path.exists(f)]

if missing:
    output = {
        "decision": "block",
        "reason": f"Missing required files: {', '.join(missing)}"
    }
    print(json.dumps(output))
    sys.exit(0)

sys.exit(0)
```

## SessionStart Control

### Inject Context
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project: my-plugin\nEnvironment: development"
  }
}
```

## Prompt-Based Hooks

For intelligent decisions, use prompt-based hooks:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if all tasks are complete. Context: $ARGUMENTS. Respond with {\"ok\": true} or {\"ok\": false, \"reason\": \"...\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Prompt hooks use Haiku for fast evaluation.
