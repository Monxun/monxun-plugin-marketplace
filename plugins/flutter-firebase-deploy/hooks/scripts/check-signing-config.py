#!/usr/bin/env python3
"""Check signing configuration after file writes."""

import os
import sys
import json


def main():
    """Warn about sensitive files being written."""
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    # Check for sensitive files
    sensitive_files = ["key.properties", ".jks", ".keystore", ".p12", ".p8"]

    if any(s in file_path for s in sensitive_files):
        print(
            "Note: Sensitive signing file detected. Ensure it's in .gitignore.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
