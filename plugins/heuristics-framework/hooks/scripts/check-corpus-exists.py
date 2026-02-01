#!/usr/bin/env python3
"""
Pre-check that corpus path exists before discovery.

Exit codes:
- 0: Success (corpus exists)
- 2: Block (corpus not found)
"""

import sys
import json
import os
import re

def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    command = input_data.get("tool_input", {}).get("command", "")

    # Extract path from discover command
    # Pattern: python ... discover <path> ...
    match = re.search(r'discover\s+([^\s]+)', command)

    if not match:
        # Not a discover command we care about
        sys.exit(0)

    corpus_path = match.group(1)

    # Resolve path
    if not os.path.isabs(corpus_path):
        cwd = input_data.get("cwd", os.getcwd())
        corpus_path = os.path.join(cwd, corpus_path)

    # Check existence
    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus path does not exist: {corpus_path}", file=sys.stderr)
        print(f"[INFO] Please verify the path and try again", file=sys.stderr)
        sys.exit(2)

    # Check if it's readable
    if os.path.isdir(corpus_path):
        if not os.access(corpus_path, os.R_OK):
            print(f"[ERROR] Cannot read corpus directory: {corpus_path}", file=sys.stderr)
            sys.exit(2)

        # Check for files
        files = os.listdir(corpus_path)
        if not files:
            print(f"[WARNING] Corpus directory is empty: {corpus_path}", file=sys.stderr)
            # Don't block, just warn
    elif os.path.isfile(corpus_path):
        if not os.access(corpus_path, os.R_OK):
            print(f"[ERROR] Cannot read corpus file: {corpus_path}", file=sys.stderr)
            sys.exit(2)

    # Success
    sys.exit(0)


if __name__ == "__main__":
    main()
