#!/bin/bash
# Validate that written files don't contain secrets
# This hook runs after Edit/Write operations

set -e

# Get the file path from argument or environment
FILE_PATH="${1:-$TOOL_FILE_PATH}"

# Exit successfully if no file path
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Skip if file doesn't exist
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Define patterns that shouldn't be in code files
SECRET_PATTERNS=(
    # API Keys (actual values, not placeholders)
    "sk-[a-zA-Z0-9]{32,}"                    # OpenAI API keys
    "AKIA[0-9A-Z]{16}"                        # AWS Access Key ID
    "ghp_[a-zA-Z0-9]{36}"                     # GitHub PAT

    # Private Keys
    "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"

    # Hardcoded passwords (not in example/test contexts)
    "password\\s*=\\s*[\"'][^\"']{8,}[\"']"
)

# Files to skip (test files, examples, etc.)
SKIP_PATTERNS=(
    "*_test.*"
    "*Test.*"
    "*.test.*"
    "*example*"
    "*sample*"
    "*.md"
    "*.txt"
)

# Check if file should be skipped
BASENAME=$(basename "$FILE_PATH")
for pattern in "${SKIP_PATTERNS[@]}"; do
    if [[ "$BASENAME" == $pattern ]]; then
        exit 0
    fi
done

# Check file contents for secrets
FOUND_SECRETS=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -qiE "$pattern" "$FILE_PATH" 2>/dev/null; then
        echo "⚠️  WARNING: Potential secret detected in $FILE_PATH" >&2
        echo "Pattern matched: $pattern" >&2
        FOUND_SECRETS=1
    fi
done

if [ $FOUND_SECRETS -eq 1 ]; then
    echo "" >&2
    echo "Please review the file and ensure no real secrets are committed." >&2
    echo "If this is a false positive (e.g., example/placeholder), you can ignore this warning." >&2
    # Don't block - allow the write but warn
fi

exit 0
