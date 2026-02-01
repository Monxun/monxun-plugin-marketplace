#!/usr/bin/env python3
"""Validate Flutter project structure before operations."""

import os
import sys
import json


def main():
    """Check if we're in a Flutter project."""
    # Read tool input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # No input or invalid JSON - continue
        sys.exit(0)

    # Check if command is Flutter-related
    command = input_data.get("tool_input", {}).get("command", "")
    if not any(x in command for x in ["flutter", "fastlane", "pod", "gradle"]):
        sys.exit(0)

    # Check for pubspec.yaml
    if not os.path.exists("pubspec.yaml"):
        print(
            "Warning: No pubspec.yaml found. Are you in a Flutter project?",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
