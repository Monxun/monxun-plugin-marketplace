#!/usr/bin/env python3
"""
PreToolUse hook: Validate Genesis template files before writes.

Exit codes:
- 0: Valid, continue
- 2: Invalid, block operation (stderr shown to Claude)
"""

import json
import sys
import re


def validate_genesis_manifest(content: str) -> tuple[bool, str]:
    """Validate genesis.json content."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax: {e}"

    # Required fields
    if "name" not in data:
        return False, "Missing required field: name"

    # Name validation (kebab-case)
    name = data.get("name", "")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        return False, f"Name must be kebab-case: {name}"

    # Name length
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars, max 64)"

    # Version format if present
    version = data.get("version", "1.0.0")
    if not re.match(r"^\d+\.\d+\.\d+", version):
        return False, f"Version must be semver format: {version}"

    # Prompts validation if present
    prompts = data.get("prompts", [])
    for prompt in prompts:
        if "name" not in prompt:
            return False, "Prompt missing required field: name"
        if "type" not in prompt:
            return False, f"Prompt '{prompt['name']}' missing type"
        if prompt["type"] not in [
            "string",
            "boolean",
            "number",
            "select",
            "multiselect",
        ]:
            return False, f"Invalid prompt type: {prompt['type']}"

    return True, ""


def validate_template_file(content: str) -> tuple[bool, str]:
    """Validate template file syntax."""
    # Check for balanced template blocks
    open_blocks = re.findall(r"\{\{#(\w+)", content)
    close_blocks = re.findall(r"\{\{/(\w+)", content)

    if len(open_blocks) != len(close_blocks):
        return (
            False,
            f"Unbalanced template blocks: {len(open_blocks)} opens, {len(close_blocks)} closes",
        )

    # Check for unclosed variables
    unclosed = re.findall(r"\{\{[^}]*$", content, re.MULTILINE)
    if unclosed:
        return False, f"Unclosed template variable found"

    # Check for invalid filter syntax
    invalid_filters = re.findall(r"\{\{[^}]+\|\s*\}\}", content)
    if invalid_filters:
        return False, f"Empty filter found: {invalid_filters[0]}"

    return True, ""


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No JSON input, allow operation
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")

    # Skip if not a file write
    if not file_path or not content:
        sys.exit(0)

    # Validate genesis.json
    if file_path.endswith("genesis.json"):
        valid, error = validate_genesis_manifest(content)
        if not valid:
            print(f"Genesis manifest validation failed: {error}", file=sys.stderr)
            sys.exit(2)

    # Validate template files
    if ".template" in file_path:
        valid, error = validate_template_file(content)
        if not valid:
            print(f"Template validation failed: {error}", file=sys.stderr)
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
