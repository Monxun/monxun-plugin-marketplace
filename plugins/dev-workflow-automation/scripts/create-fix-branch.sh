#!/bin/bash
# Create a standardized fix branch for auto-remediation
# Usage: create-fix-branch.sh <fix-type> <run-id> [base-branch]

set -e

FIX_TYPE="${1:-unknown}"
RUN_ID="${2:-0}"
BASE_BRANCH="${3:-main}"

# Validate inputs
if [ "$RUN_ID" == "0" ]; then
    echo "Error: Run ID is required" >&2
    echo "Usage: $0 <fix-type> <run-id> [base-branch]" >&2
    exit 1
fi

# Sanitize fix type for branch name
SANITIZED_TYPE=$(echo "$FIX_TYPE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Create branch name
BRANCH_NAME="fix/auto-${TIMESTAMP}-${SANITIZED_TYPE}-run-${RUN_ID}"

# Ensure we're on a clean state
if ! git diff --quiet 2>/dev/null; then
    echo "Error: Working directory has uncommitted changes" >&2
    echo "Please commit or stash your changes first" >&2
    exit 1
fi

# Fetch latest from remote
echo "Fetching latest from remote..."
git fetch origin "$BASE_BRANCH" 2>/dev/null || true

# Create and checkout the branch
echo "Creating branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME" "origin/$BASE_BRANCH" 2>/dev/null || \
git checkout -b "$BRANCH_NAME" "$BASE_BRANCH"

# Push the branch to set up tracking
echo "Pushing branch to remote..."
git push -u origin "$BRANCH_NAME"

# Output the branch name for use by calling scripts
echo ""
echo "Branch created successfully!"
echo "BRANCH_NAME=$BRANCH_NAME"
