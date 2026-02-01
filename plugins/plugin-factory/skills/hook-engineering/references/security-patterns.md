# Security Patterns for Hooks

Best practices for writing secure hook scripts.

## General Principles

### 1. Validate All Input
```python
#!/usr/bin/env python3
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

# Validate expected fields
tool_name = input_data.get("tool_name")
if not tool_name:
    print("Missing tool_name", file=sys.stderr)
    sys.exit(1)
```

### 2. Quote Shell Variables
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# WRONG: Unquoted variable
# rm $FILE_PATH

# RIGHT: Quoted variable
rm "$FILE_PATH"
```

### 3. Block Path Traversal
```python
import os

file_path = tool_input.get("file_path", "")

# Block path traversal
if ".." in file_path:
    print("Error: Path traversal not allowed", file=sys.stderr)
    sys.exit(2)

# Resolve to absolute path
abs_path = os.path.abspath(file_path)
allowed_dir = os.path.abspath("/allowed/directory")

if not abs_path.startswith(allowed_dir):
    print("Error: Path outside allowed directory", file=sys.stderr)
    sys.exit(2)
```

### 4. Use Absolute Paths
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
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

### 5. Protect Sensitive Files
```python
SENSITIVE_PATTERNS = [
    ".env",
    ".env.*",
    "*.key",
    "*.pem",
    "*secret*",
    "*password*",
    ".git/",
    "credentials*"
]

import fnmatch

def is_sensitive(path):
    filename = os.path.basename(path)
    for pattern in SENSITIVE_PATTERNS:
        if fnmatch.fnmatch(filename, pattern):
            return True
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

if is_sensitive(file_path):
    print("Error: Cannot modify sensitive file", file=sys.stderr)
    sys.exit(2)
```

## Specific Patterns

### Validate Bash Commands

```python
DANGEROUS_COMMANDS = [
    r'\brm\s+-rf\s+/',
    r'\bsudo\b',
    r'\bchmod\s+777\b',
    r'\bcurl\b.*\|\s*sh',
    r'\bwget\b.*\|\s*sh',
    r'\beval\b',
    r'>\s*/dev/sd',
    r'\bmkfs\b',
    r'\bdd\b.*of=/dev'
]

import re

def is_dangerous(command):
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

command = tool_input.get("command", "")
if is_dangerous(command):
    print(f"Error: Dangerous command blocked", file=sys.stderr)
    sys.exit(2)
```

### Validate Write Targets

```python
PROTECTED_PATHS = [
    "/.claude-plugin/",  # Except plugin.json
    "/.git/",
    "/node_modules/",
    "/.env"
]

def is_protected(path):
    for protected in PROTECTED_PATHS:
        if protected in path:
            # Special case: allow plugin.json
            if "/.claude-plugin/" in path and path.endswith("plugin.json"):
                return False
            return True
    return False

if is_protected(file_path):
    print("Error: Protected path", file=sys.stderr)
    sys.exit(2)
```

### Sanitize User Input

```python
import shlex

def sanitize_for_shell(value):
    """Escape value for safe shell usage"""
    return shlex.quote(value)

# When building shell commands
command = f"echo {sanitize_for_shell(user_input)}"
```

### Limit Resource Usage

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.py",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### Log Security Events

```python
import logging
import datetime

logging.basicConfig(
    filename='/tmp/claude-security.log',
    level=logging.WARNING
)

def log_security_event(event_type, details):
    logging.warning(f"{datetime.datetime.now()} - {event_type}: {details}")

# Log blocked operations
if blocked:
    log_security_event("BLOCKED_WRITE", file_path)
```

## Complete Security Hook

```python
#!/usr/bin/env python3
"""Security validation hook for write operations."""
import json
import sys
import os
import re
import fnmatch

# Configuration
SENSITIVE_PATTERNS = [".env", "*.key", "*.pem", "*secret*", "credentials*"]
PROTECTED_DIRS = ["/.git/", "/node_modules/"]
ALLOWED_IN_CLAUDE_PLUGIN = ["plugin.json"]

def validate_input():
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

def is_sensitive(path):
    filename = os.path.basename(path)
    return any(fnmatch.fnmatch(filename, p) for p in SENSITIVE_PATTERNS)

def is_protected(path):
    if ".claude-plugin/" in path:
        return not any(path.endswith(f) for f in ALLOWED_IN_CLAUDE_PLUGIN)
    return any(d in path for d in PROTECTED_DIRS)

def has_path_traversal(path):
    return ".." in path

def main():
    input_data = validate_input()
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        sys.exit(0)

    # Security checks
    if has_path_traversal(file_path):
        print("SECURITY: Path traversal detected", file=sys.stderr)
        sys.exit(2)

    if is_sensitive(file_path):
        print("SECURITY: Sensitive file modification blocked", file=sys.stderr)
        sys.exit(2)

    if is_protected(file_path):
        print("SECURITY: Protected path modification blocked", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Checklist

- [ ] Validate JSON input
- [ ] Quote shell variables
- [ ] Block path traversal
- [ ] Use absolute paths
- [ ] Protect sensitive files
- [ ] Set timeouts
- [ ] Log security events
- [ ] Test edge cases
