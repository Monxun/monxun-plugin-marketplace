#!/bin/bash
# PostToolUse hook: Auto-format generated files after Write operations.
#
# Exit codes:
# - 0: Success
# - Non-zero: Non-blocking error (continues)

# Read hook input from stdin
INPUT=$(cat)

# Extract file path from JSON input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Skip if file doesn't exist
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Format based on file extension
case "$FILE_PATH" in
    *.json)
        # Format JSON with jq
        if command -v jq &> /dev/null; then
            TMP=$(mktemp)
            if jq . "$FILE_PATH" > "$TMP" 2>/dev/null; then
                mv "$TMP" "$FILE_PATH"
            else
                rm -f "$TMP"
            fi
        fi
        ;;
    *.py)
        # Format Python with black (if available)
        if command -v black &> /dev/null; then
            black --quiet "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
    *.sh)
        # Ensure shell scripts are executable
        chmod +x "$FILE_PATH" 2>/dev/null || true
        ;;
    *.md)
        # No formatting for markdown, but ensure Unix line endings
        if command -v dos2unix &> /dev/null; then
            dos2unix -q "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
esac

exit 0
