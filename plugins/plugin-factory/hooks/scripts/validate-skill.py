#!/usr/bin/env python3
"""
PreToolUse hook: Validate SKILL.md structure before edits.

Exit codes:
- 0: Valid, continue
- 2: Invalid, block operation (stderr shown to Claude)
"""

import json
import sys
import re
import yaml

def validate_skill(file_path: str, content: str) -> tuple[bool, str]:
    """Validate SKILL.md content."""

    # Only validate SKILL.md files
    if not file_path.endswith('SKILL.md'):
        return True, ""

    # Check for frontmatter
    if not content.startswith('---'):
        return False, "SKILL.md must start with YAML frontmatter (---)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Required frontmatter fields
    required = ['name', 'description']
    missing = [f for f in required if f not in frontmatter]
    if missing:
        return False, f"Missing frontmatter fields: {', '.join(missing)}"

    # Name validation (kebab-case)
    name = frontmatter.get('name', '')
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        return False, f"Skill name must be kebab-case: {name}"

    # Description length
    desc = frontmatter.get('description', '')
    if len(desc) > 1024:
        return False, f"Description too long ({len(desc)} chars, max 1024)"

    # Check for trigger keywords in description
    keywords = ['use when', 'supports', 'trigger']
    desc_lower = desc.lower()
    if not any(kw in desc_lower for kw in keywords):
        return False, "Description should include trigger keywords (use when:, supports:)"

    # Line count check (progressive disclosure)
    lines = content.count('\n') + 1
    if lines > 500:
        return False, f"SKILL.md too long ({lines} lines, max 500). Use references/ for detailed docs"

    return True, ""

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # For Edit tool, we need to check the file after edit
    # Read current content and apply edit
    old_string = tool_input.get('old_string', '')
    new_string = tool_input.get('new_string', '')

    if not file_path.endswith('SKILL.md'):
        sys.exit(0)

    # Try to read existing file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Apply the edit
        if old_string:
            content = content.replace(old_string, new_string, 1)
    except FileNotFoundError:
        # New file, check new_string as content
        content = new_string

    valid, error = validate_skill(file_path, content)

    if valid:
        sys.exit(0)
    else:
        print(f"Skill validation failed: {error}", file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()
