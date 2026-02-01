#!/usr/bin/env python3
"""
Validate hooks.json syntax and structure.

Exit codes:
- 0: Valid
- 2: Invalid (stderr shows error)
"""

import json
import sys
import os

VALID_EVENTS = [
    'PreToolUse',
    'PostToolUse',
    'Notification',
    'Stop',
    'SubagentStop',
    'SessionStart',
    'SessionStop',
    'HistoryUpdate',
    'InvokeAgent',
    'InvokeAgentPermission',
    'Prompt',
    'Toolbar'
]

def validate_hooks(file_path: str) -> tuple[bool, str]:
    """Validate hooks.json structure."""

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, f"File not found: {file_path}"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    if 'hooks' not in data:
        return False, "Missing 'hooks' key"

    hooks = data['hooks']
    if not isinstance(hooks, dict):
        return False, "'hooks' must be an object"

    for event_type, handlers in hooks.items():
        # Validate event type
        if event_type not in VALID_EVENTS:
            return False, f"Invalid event type: {event_type}. Valid: {', '.join(VALID_EVENTS)}"

        # Validate handlers array
        if not isinstance(handlers, list):
            return False, f"{event_type} handlers must be an array"

        for i, handler in enumerate(handlers):
            if not isinstance(handler, dict):
                return False, f"{event_type}[{i}] must be an object"

            # Must have command
            if 'command' not in handler:
                return False, f"{event_type}[{i}] missing 'command'"

            command = handler['command']
            if not isinstance(command, str):
                return False, f"{event_type}[{i}] command must be a string"

            # Validate matcher if present
            if 'matcher' in handler:
                matcher = handler['matcher']
                if not isinstance(matcher, str):
                    return False, f"{event_type}[{i}] matcher must be a string"

    return True, ""

def main():
    if len(sys.argv) < 2:
        # Read from stdin for hook context
        try:
            hook_input = json.load(sys.stdin)
            file_path = hook_input.get('tool_input', {}).get('file_path', '')
        except:
            file_path = ''
    else:
        file_path = sys.argv[1]

    if not file_path or not file_path.endswith('hooks.json'):
        sys.exit(0)

    valid, error = validate_hooks(file_path)

    if valid:
        print(json.dumps({"status": "valid"}))
        sys.exit(0)
    else:
        print(f"Hook validation failed: {error}", file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
