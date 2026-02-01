#!/usr/bin/env python3
"""
PreToolUse hook: Validate plugin.json manifest before writes.

Exit codes:
- 0: Valid, continue
- 2: Invalid, block operation (stderr shown to Claude)
"""

import json
import sys
import os
import re

def validate_manifest(file_path: str, content: str) -> tuple[bool, str]:
    """Validate plugin.json content."""

    # Only validate plugin.json files
    if not file_path.endswith('plugin.json'):
        return True, ""

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax: {e}"

    # Required fields
    required = ['name', 'version', 'description']
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"

    # Name validation (kebab-case)
    name = data.get('name', '')
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        return False, f"Name must be kebab-case: {name}"

    # Name length
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars, max 64)"

    # Version format (semver)
    version = data.get('version', '')
    if not re.match(r'^\d+\.\d+\.\d+', version):
        return False, f"Version must be semver format: {version}"

    # Description length
    desc = data.get('description', '')
    if len(desc) > 1024:
        return False, f"Description too long ({len(desc)} chars, max 1024)"

    return True, ""

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No JSON input, allow operation
        sys.exit(0)

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    content = tool_input.get('content', '')

    # Skip if not a file write
    if not file_path or not content:
        sys.exit(0)

    valid, error = validate_manifest(file_path, content)

    if valid:
        sys.exit(0)
    else:
        print(f"Manifest validation failed: {error}", file=sys.stderr)
        sys.exit(2)  # Block operation

if __name__ == '__main__':
    main()
