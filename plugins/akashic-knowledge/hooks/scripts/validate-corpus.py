#!/usr/bin/env python3
"""
Pre-ingest validation hook for Akashic Knowledge plugin.

Validates corpus before ingestion:
- Checks source path exists
- Validates file patterns
- Estimates corpus size
- Warns about potential issues

Exit codes:
- 0: Validation passed, continue
- 2: Validation failed, block operation
"""

import json
import os
import sys
from pathlib import Path


def validate_corpus(tool_input: dict) -> tuple[bool, str]:
    """Validate corpus before ingestion."""
    source = tool_input.get("source", "")
    kb_name = tool_input.get("kb_name", "")

    errors = []
    warnings = []

    # Check KB name
    if not kb_name:
        errors.append("Knowledge base name is required")

    # Check source path
    source_path = Path(source)
    if not source_path.exists():
        errors.append(f"Source path does not exist: {source}")
    elif source_path.is_dir():
        # Count files
        patterns = tool_input.get("file_patterns", ["*.md", "*.txt", "*.py"])
        file_count = 0
        total_size = 0

        for pattern in patterns:
            for file_path in source_path.rglob(pattern):
                file_count += 1
                total_size += file_path.stat().st_size

        if file_count == 0:
            warnings.append(f"No files found matching patterns: {patterns}")

        if total_size > 100 * 1024 * 1024:  # 100MB
            warnings.append(
                f"Large corpus detected: {total_size / 1024 / 1024:.1f}MB. "
                "Ingestion may take a while."
            )

        if file_count > 1000:
            warnings.append(
                f"Large number of files: {file_count}. "
                "Consider using more specific patterns."
            )

    # Check for sensitive files
    sensitive_patterns = [".env", "credentials", "secret", "private", "password"]
    if source_path.is_dir():
        for sensitive in sensitive_patterns:
            matches = list(source_path.rglob(f"*{sensitive}*"))
            if matches:
                warnings.append(
                    f"Potentially sensitive files detected: {[str(m) for m in matches[:3]]}"
                )

    if errors:
        return False, "Validation failed:\n" + "\n".join(f"- {e}" for e in errors)

    message = "Validation passed."
    if warnings:
        message += "\nWarnings:\n" + "\n".join(f"- {w}" for w in warnings)

    return True, message


def main():
    """Main entry point."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_input = hook_input.get("tool_input", {})

    passed, message = validate_corpus(tool_input)

    if passed:
        print(message)
        sys.exit(0)
    else:
        print(message, file=sys.stderr)
        sys.exit(2)  # Block operation


if __name__ == "__main__":
    main()
