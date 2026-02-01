#!/bin/bash
#
# PostToolUse hook: Security scan for written files
#
# Exit codes:
# - 0: No issues found
# - 1: Warning (non-blocking)
# - 2: Critical issue (blocking)

# Read hook input from stdin
INPUT=$(cat)

# Extract file path from JSON input
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_result', {}).get('file_path', ''))" 2>/dev/null)

# Exit if no file path
[ -z "$FILE_PATH" ] && exit 0

# Skip if not a template file
[[ "$FILE_PATH" != *".template"* ]] && [[ "$FILE_PATH" != *"genesis.json"* ]] && exit 0

# Check if file exists
[ ! -f "$FILE_PATH" ] && exit 0

# Security patterns to check
SECRETS_PATTERNS=(
    "password\s*[=:]\s*[\"'][^\"']+[\"']"
    "secret\s*[=:]\s*[\"'][^\"']+[\"']"
    "api_key\s*[=:]\s*[\"'][^\"']+[\"']"
    "private_key\s*[=:]\s*[\"'][^\"']+[\"']"
    "-----BEGIN.*PRIVATE KEY-----"
    "aws_access_key_id\s*[=:]\s*[A-Z0-9]{20}"
    "aws_secret_access_key\s*[=:]\s*[A-Za-z0-9/+=]{40}"
)

# Check for hardcoded secrets (excluding template variables)
for pattern in "${SECRETS_PATTERNS[@]}"; do
    # Find matches that are NOT template variables
    matches=$(grep -inE "$pattern" "$FILE_PATH" 2>/dev/null | grep -v '\{\{' | grep -v '\$\{\{')
    if [ -n "$matches" ]; then
        echo "WARNING: Potential hardcoded secret in $FILE_PATH" >&2
        echo "$matches" >&2
        # Warning only, don't block
    fi
done

# Check for sensitive file patterns
FILENAME=$(basename "$FILE_PATH")
case "$FILENAME" in
    .env|*.pem|*.key|id_rsa*|*.p12|*.pfx)
        if [[ "$FILENAME" != *".example"* ]] && [[ "$FILENAME" != *".template"* ]]; then
            echo "WARNING: Sensitive file type: $FILENAME" >&2
        fi
        ;;
esac

# Check Dockerfile security patterns
if [[ "$FILE_PATH" == *"Dockerfile"* ]]; then
    # Check for running as root
    if grep -q "USER root$" "$FILE_PATH" 2>/dev/null; then
        echo "WARNING: Dockerfile runs as root" >&2
    fi

    # Check for no USER directive
    if ! grep -q "^USER " "$FILE_PATH" 2>/dev/null; then
        echo "INFO: Dockerfile has no USER directive (running as root)" >&2
    fi

    # Check for latest tag
    if grep -qE "FROM .+:latest" "$FILE_PATH" 2>/dev/null; then
        echo "WARNING: Using 'latest' tag in Dockerfile" >&2
    fi
fi

# All checks passed (or only warnings)
exit 0
