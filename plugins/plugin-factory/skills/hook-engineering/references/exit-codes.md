# Exit Codes Reference

Complete guide to hook script exit code semantics.

## Exit Code Summary

| Code | Name | Behavior |
|------|------|----------|
| 0 | Success | Continue, parse JSON stdout |
| 2 | Block | Stop execution, stderr to Claude |
| 1, 3+ | Non-blocking | Continue, stderr shown in verbose |

## Exit Code 0: Success

### Behavior
- Hook succeeded
- Execution continues
- JSON stdout parsed for control
- Plain stdout shown in verbose mode

### Without JSON
```bash
#!/bin/bash
echo "Validation passed"
exit 0
```
Output shown in verbose mode (Ctrl+O).

### With JSON Control
```python
import json
import sys

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}
print(json.dumps(output))
sys.exit(0)
```

## Exit Code 2: Block

### Behavior
- **PreToolUse**: Blocks tool execution
- **PermissionRequest**: Denies permission
- **Stop**: Prevents Claude from stopping
- **SubagentStop**: Prevents subagent from finishing
- stderr message shown to Claude

### Example: Block Write
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
file_path = input_data.get("tool_input", {}).get("file_path", "")

if ".claude-plugin/" in file_path and not file_path.endswith("plugin.json"):
    print("ERROR: Only plugin.json allowed in .claude-plugin/", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

### Example: Prevent Stop
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)

# Check for incomplete tasks
if not all_tasks_complete():
    print("Cannot stop: Tasks incomplete", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

## Other Exit Codes: Non-blocking

### Behavior
- Non-blocking error
- Execution continues
- stderr shown in verbose mode only
- Does NOT affect Claude's behavior

### Example
```bash
#!/bin/bash
echo "Warning: Something minor happened" >&2
exit 1  # Non-blocking, continues
```

## Event-Specific Behavior

| Event | Exit 0 | Exit 2 | Other |
|-------|--------|--------|-------|
| PreToolUse | Continue, parse JSON | Block tool | Continue |
| PostToolUse | Continue, parse JSON | Show stderr to Claude | Continue |
| PermissionRequest | Continue, parse JSON | Deny permission | Continue |
| Stop | Allow stop | Prevent stop | Continue |
| SubagentStop | Allow finish | Prevent finish | Continue |
| UserPromptSubmit | Process prompt | Block prompt | Continue |
| SessionStart | Continue | Show error | Continue |
| SessionEnd | Continue | N/A | Continue |
| Notification | Continue | N/A | Continue |

## JSON Output with Exit 0

When exit code is 0, stdout is parsed for JSON:

### PreToolUse Control
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Explanation",
    "updatedInput": {
      "file_path": "modified/path"
    }
  }
}
```

### PostToolUse Control
```json
{
  "decision": "block",
  "reason": "Explanation for Claude",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra context for Claude"
  }
}
```

### Stop Control
```json
{
  "decision": "block",
  "reason": "Reason to continue working"
}
```

### Common Fields
```json
{
  "continue": false,
  "stopReason": "Message to user",
  "suppressOutput": true,
  "systemMessage": "Warning message"
}
```

## Best Practices

### 1. Use Exit 2 for Blocking
```python
if should_block:
    print("Clear error message", file=sys.stderr)
    sys.exit(2)
```

### 2. Use Exit 0 for Success/Control
```python
if valid:
    output = {"hookSpecificOutput": {...}}
    print(json.dumps(output))
    sys.exit(0)
```

### 3. Avoid Exit 1 for Intentional Blocks
```python
# WRONG: Exit 1 doesn't block
sys.exit(1)

# RIGHT: Exit 2 blocks
sys.exit(2)
```

### 4. Always stderr for Errors
```python
# WRONG: stdout for errors
print("Error")

# RIGHT: stderr for errors
print("Error", file=sys.stderr)
```

## Debugging

### Test Exit Codes
```bash
# Run hook manually
echo '{"tool_name":"Write","tool_input":{}}' | ./script.py
echo "Exit code: $?"
```

### Check Output
```bash
# Capture stdout and stderr
echo '{"tool_name":"Write"}' | ./script.py > stdout.txt 2> stderr.txt
echo "Exit: $?"
cat stdout.txt
cat stderr.txt
```
