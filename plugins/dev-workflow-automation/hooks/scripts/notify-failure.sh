#!/bin/bash
# Notify about CI/CD failures
# This hook can be triggered by external events (GitHub webhooks, etc.)

set -e

# Get failure details from arguments or environment
RUN_ID="${1:-$WORKFLOW_RUN_ID}"
WORKFLOW_NAME="${2:-$WORKFLOW_NAME}"
FAILURE_TYPE="${3:-$FAILURE_TYPE}"
REPO="${GITHUB_REPOSITORY:-}"

# Exit if no run ID
if [ -z "$RUN_ID" ]; then
    echo "No workflow run ID provided" >&2
    exit 1
fi

# Get repository if not set
if [ -z "$REPO" ]; then
    REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
fi

if [ -z "$REPO" ]; then
    echo "Could not determine repository" >&2
    exit 1
fi

# Fetch run details if not provided
if [ -z "$WORKFLOW_NAME" ]; then
    WORKFLOW_NAME=$(gh api "repos/$REPO/actions/runs/$RUN_ID" --jq '.name' 2>/dev/null || echo "Unknown")
fi

# Get run URL
RUN_URL="https://github.com/$REPO/actions/runs/$RUN_ID"

# Get branch
BRANCH=$(gh api "repos/$REPO/actions/runs/$RUN_ID" --jq '.head_branch' 2>/dev/null || echo "unknown")

# Get commit message
COMMIT_MSG=$(gh api "repos/$REPO/actions/runs/$RUN_ID" --jq '.head_commit.message' 2>/dev/null | head -1 || echo "")

# Format notification
cat << EOF

## 🔴 CI/CD Failure Detected

| Detail | Value |
|--------|-------|
| **Workflow** | $WORKFLOW_NAME |
| **Run ID** | [$RUN_ID]($RUN_URL) |
| **Branch** | \`$BRANCH\` |
| **Commit** | $COMMIT_MSG |

### Quick Actions

1. **Analyze**: \`/dev-workflow-automation:analyze-failure $RUN_ID\`
2. **Auto-Fix**: \`/dev-workflow-automation:auto-fix $RUN_ID\`
3. **View Logs**: [$RUN_URL]($RUN_URL)

Would you like me to investigate this failure?

EOF

exit 0
