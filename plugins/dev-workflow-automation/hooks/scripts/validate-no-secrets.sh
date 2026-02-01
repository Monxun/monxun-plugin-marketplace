#!/bin/bash
# Validate that command output doesn't contain secrets
# This hook runs after Bash commands to check for accidental secret exposure

set -e

# Get the output to check from stdin
OUTPUT=""
while IFS= read -r line; do
    OUTPUT="${OUTPUT}${line}"$'\n'
done

# Exit successfully if no output
if [ -z "$OUTPUT" ]; then
    exit 0
fi

# Define secret patterns to detect
SECRET_PATTERNS=(
    # API Keys
    "sk-[a-zA-Z0-9]{32,}"                    # OpenAI API keys
    "AKIA[0-9A-Z]{16}"                        # AWS Access Key ID
    "ghp_[a-zA-Z0-9]{36}"                     # GitHub Personal Access Token
    "gho_[a-zA-Z0-9]{36}"                     # GitHub OAuth Token
    "github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}"  # GitHub Fine-grained PAT

    # Private Keys
    "-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"
    "-----BEGIN PGP PRIVATE KEY BLOCK-----"

    # Passwords in common formats
    "password[\"']?\\s*[:=]\\s*[\"'][^\"']{8,}"
    "passwd[\"']?\\s*[:=]\\s*[\"'][^\"']{8,}"
    "pwd[\"']?\\s*[:=]\\s*[\"'][^\"']{8,}"

    # JWT tokens
    "eyJ[a-zA-Z0-9_-]*\\.eyJ[a-zA-Z0-9_-]*\\.[a-zA-Z0-9_-]*"

    # Generic secrets
    "secret[\"']?\\s*[:=]\\s*[\"'][^\"']{8,}"
    "token[\"']?\\s*[:=]\\s*[\"'][^\"']{16,}"
    "api_key[\"']?\\s*[:=]\\s*[\"'][^\"']{16,}"
)

# Check for secret patterns
FOUND_SECRETS=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    if echo "$OUTPUT" | grep -qiE "$pattern"; then
        echo "WARNING: Potential secret detected in output matching pattern: $pattern" >&2
        FOUND_SECRETS=1
    fi
done

if [ $FOUND_SECRETS -eq 1 ]; then
    echo "⚠️  Sensitive data may have been exposed in the output above." >&2
    echo "Please review and ensure no secrets are committed or logged." >&2
    # Don't block, just warn - the output has already been shown
fi

exit 0
