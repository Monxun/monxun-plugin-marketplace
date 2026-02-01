# /dev-workflow-automation:workflow-status

Show status of auto-remediation workflows and statistics.

## Usage

```
/dev-workflow-automation:workflow-status [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--pending` | Show only pending fix PRs awaiting review |
| `--failed` | Show failed auto-fix attempts |
| `--merged` | Show successfully merged auto-fixes |
| `--stats` | Show success/failure rate statistics |
| `--days <n>` | Time range in days (default: 7) |
| `--format <fmt>` | Output format: `table` (default), `json`, `brief` |

## Examples

### Show current status (default)
```
/dev-workflow-automation:workflow-status
```

### Show only pending reviews
```
/dev-workflow-automation:workflow-status --pending
```

### Show statistics for the last 30 days
```
/dev-workflow-automation:workflow-status --stats --days 30
```

### Show failed attempts
```
/dev-workflow-automation:workflow-status --failed
```

### JSON output for scripting
```
/dev-workflow-automation:workflow-status --format json
```

## Behavior

1. **Query GitHub API**
   - Search PRs with `auto-fix` label
   - Search PRs with `auto-feature` label
   - Search issues with `auto-fix-failed` label

2. **Categorize Results**
   - Pending review
   - In progress
   - Merged
   - Failed

3. **Calculate Statistics**
   - Success rate
   - Average fix time
   - Most common failure types

4. **Generate Report**
   - Current status summary
   - Detailed listings
   - Trends (if stats requested)

## Output

### Default Status Output
```
## Auto-Remediation Status

### Summary (Last 7 Days)
| Metric | Count |
|--------|-------|
| Total CI Failures | 15 |
| Auto-Fix Attempted | 12 |
| Successfully Fixed | 9 |
| Pending Review | 2 |
| Failed (Needs Human) | 1 |

### Pending Review (2)
| PR | Type | Branch | Age |
|----|------|--------|-----|
| [#123](link) | test-failure | fix/auto-20250122-test | 2h |
| [#125](link) | lint-error | fix/auto-20250123-lint | 30m |

### In Progress (1)
| Run | Workflow | Status | Started |
|-----|----------|--------|---------|
| [#456](link) | Backend CI | Analyzing | 5m ago |

### Recent Failures (1)
| Issue | Type | Reason | Created |
|-------|------|--------|---------|
| [#42](link) | build-failure | Dependency conflict | 1d ago |
```

### With `--stats` Output
```
## Auto-Remediation Statistics (Last 30 Days)

### Overall Performance
| Metric | Value |
|--------|-------|
| Total CI Failures | 45 |
| Auto-Fix Success Rate | 75% |
| Average Fix Time | 4.2 min |
| Human Intervention Required | 25% |

### By Failure Type
| Type | Attempts | Success Rate |
|------|----------|--------------|
| test-failure | 28 | 82% |
| lint-error | 10 | 90% |
| build-failure | 5 | 40% |
| security-issue | 2 | 50% |

### Trends
```
Success Rate Over Time
100% |        ___
 75% |    ___/   \___
 50% |___/           \___
 25% |
  0% +--------------------
     Week1  Week2  Week3  Week4
```

### Top Fixed Issues
1. Mock configuration errors (8 fixes)
2. Missing null checks (5 fixes)
3. Outdated test assertions (4 fixes)

### Common Failure Reasons (When Auto-Fix Fails)
1. External dependency issues (40%)
2. Complex refactoring needed (30%)
3. Multiple files affected (20%)
4. Infrastructure/environment (10%)
```

### Pending Only (`--pending`)
```
## Pending Auto-Fix PRs

Awaiting human review and approval.

| PR | Title | Type | Files | Created |
|----|-------|------|-------|---------|
| [#123](link) | fix: Auto-remediate test-failure from run #789 | test-failure | 2 | 2h ago |
| [#125](link) | fix: Auto-remediate lint-error from run #791 | lint-error | 1 | 30m ago |

### Quick Actions
- Review PR #123: `gh pr view 123`
- Approve PR #123: `gh pr review 123 --approve`
- Merge PR #123: `gh pr merge 123 --squash`
```

### Failed Only (`--failed`)
```
## Failed Auto-Fix Attempts

These failures require human intervention.

| Issue | Original Run | Type | Reason | Age |
|-------|--------------|------|--------|-----|
| [#42](link) | [#12345](link) | build-failure | Dependency conflict | 1d |
| [#38](link) | [#12340](link) | security-issue | Breaking change required | 3d |

### Issue #42 Details
**Type**: build-failure
**Attempts**: 3
**Root Cause**: Missing artifact `com.example:internal-lib:2.0.0`

**Suggested Manual Steps**:
1. Check internal Maven repository access
2. Verify artifact version exists
3. Update pom.xml with correct coordinates

**Re-trigger**:
```bash
/dev-workflow-automation:auto-fix 12345 --clarification "Use internal-lib:1.9.0 instead"
```
```

### JSON Output (`--format json`)
```json
{
  "period": {
    "days": 7,
    "start": "2025-01-16",
    "end": "2025-01-23"
  },
  "summary": {
    "total_failures": 15,
    "auto_fix_attempted": 12,
    "successful": 9,
    "pending_review": 2,
    "failed": 1
  },
  "pending_prs": [
    {
      "number": 123,
      "title": "fix: Auto-remediate test-failure",
      "type": "test-failure",
      "branch": "fix/auto-20250122-test",
      "created": "2025-01-22T10:30:00Z",
      "url": "https://github.com/org/repo/pull/123"
    }
  ],
  "failed_issues": [
    {
      "number": 42,
      "title": "[Auto-Fix Failed] build-failure",
      "type": "build-failure",
      "run_id": 12345,
      "created": "2025-01-22T08:00:00Z"
    }
  ],
  "statistics": {
    "success_rate": 0.75,
    "avg_fix_time_seconds": 252,
    "by_type": {
      "test-failure": { "attempts": 8, "success_rate": 0.875 },
      "lint-error": { "attempts": 3, "success_rate": 1.0 },
      "build-failure": { "attempts": 1, "success_rate": 0.0 }
    }
  }
}
```

### Brief Output (`--format brief`)
```
Auto-Fix Status (7d): 9/12 successful (75%), 2 pending review, 1 failed
Pending: PR #123 (test), PR #125 (lint)
Failed: Issue #42 (build-failure)
```

## Related Commands

- `/dev-workflow-automation:auto-fix` - Trigger a fix
- `/dev-workflow-automation:auto-feature` - Implement features
- `/dev-workflow-automation:analyze-failure` - Analyze failures

## Implementation Notes

This command queries GitHub using the `gh` CLI:
- `gh pr list --label auto-fix --state open` - Pending PRs
- `gh pr list --label auto-fix --state merged` - Merged PRs
- `gh issue list --label auto-fix-failed` - Failed attempts

Statistics are calculated by parsing PR/issue metadata and timestamps.
