#!/bin/bash
# Validate commands before execution
# Prevents potentially dangerous commands in automated contexts

set -e

# Get the command from stdin or argument
COMMAND="${1:-}"
if [ -z "$COMMAND" ]; then
    read -r COMMAND
fi

# Exit successfully if no command (allow through)
if [ -z "$COMMAND" ]; then
    exit 0
fi

# Define blocked patterns for automated execution
BLOCKED_PATTERNS=(
    # Destructive git operations
    "git push --force"
    "git push -f"
    "git reset --hard"
    "git clean -fd"
    "git checkout \."
    "git restore \."

    # File system destructive operations
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \*"

    # Credential exposure
    "echo.*API_KEY"
    "echo.*SECRET"
    "echo.*PASSWORD"
    "echo.*TOKEN"
    "cat.*\.env"
    "cat.*credentials"

    # Network operations that might leak data
    "curl.*-d.*secret"
    "wget.*password"
)

# Check for blocked patterns
for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$pattern"; then
        echo "BLOCKED: Command matches blocked pattern: $pattern" >&2
        exit 1
    fi
done

# Warn about potentially risky operations (but allow)
WARN_PATTERNS=(
    "git push"
    "npm publish"
    "docker push"
    "aws.*delete"
    "gh release"
)

for pattern in "${WARN_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$pattern"; then
        echo "WARNING: Command may have side effects: $COMMAND" >&2
        # Don't block, just warn
    fi
done

# Command is allowed
exit 0
