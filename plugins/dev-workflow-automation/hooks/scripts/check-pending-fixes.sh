#!/bin/bash
# Check for pending auto-fix PRs and recent failures
# This hook runs at session start to inform the user of CI/CD status

set -e

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    exit 0  # Silently exit if gh not available
fi

# Check if authenticated
if ! gh auth status &> /dev/null 2>&1; then
    exit 0  # Silently exit if not authenticated
fi

# Get repository from environment or detect from git
REPO="${GITHUB_REPOSITORY:-}"
if [ -z "$REPO" ]; then
    REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
fi

if [ -z "$REPO" ]; then
    exit 0  # Can't determine repository
fi

# Output file for hook results
OUTPUT=""

# Check for pending auto-fix PRs
PENDING_PRS=$(gh pr list --repo "$REPO" --label "auto-fix" --state open --json number,title --jq 'length' 2>/dev/null || echo "0")

if [ "$PENDING_PRS" -gt 0 ]; then
    OUTPUT="${OUTPUT}📋 **$PENDING_PRS pending auto-fix PR(s)** awaiting review\n"

    # List the PRs
    PR_LIST=$(gh pr list --repo "$REPO" --label "auto-fix" --state open --json number,title --jq '.[] | "  - PR #\(.number): \(.title)"' 2>/dev/null || echo "")
    if [ -n "$PR_LIST" ]; then
        OUTPUT="${OUTPUT}${PR_LIST}\n"
    fi
fi

# Check for failed auto-fix issues
FAILED_ISSUES=$(gh issue list --repo "$REPO" --label "auto-fix-failed" --state open --json number --jq 'length' 2>/dev/null || echo "0")

if [ "$FAILED_ISSUES" -gt 0 ]; then
    OUTPUT="${OUTPUT}⚠️  **$FAILED_ISSUES failed auto-fix attempt(s)** need human attention\n"
fi

# Check for recent CI failures (last 24 hours)
RECENT_FAILURES=$(gh run list --repo "$REPO" --status failure --limit 5 --json databaseId,createdAt,name --jq '[.[] | select(.createdAt > (now - 86400 | todate))] | length' 2>/dev/null || echo "0")

if [ "$RECENT_FAILURES" -gt 0 ]; then
    OUTPUT="${OUTPUT}🔴 **$RECENT_FAILURES CI failure(s)** in the last 24 hours\n"
fi

# Output results if any
if [ -n "$OUTPUT" ]; then
    echo -e "\n## CI/CD Status\n"
    echo -e "$OUTPUT"
    echo -e "\nUse \`/dev-workflow-automation:workflow-status\` for details.\n"
fi

exit 0
