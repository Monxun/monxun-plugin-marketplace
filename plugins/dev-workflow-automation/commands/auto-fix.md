# /dev-workflow-automation:auto-fix

Manually trigger auto-fix for a specific CI/CD failure.

## Usage

```
/dev-workflow-automation:auto-fix <run-id> [options]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<run-id>` | GitHub workflow run ID to fix (required, positional or `--run-id`) |

## Options

| Option | Description |
|--------|-------------|
| `--run-id <id>` | Alternative way to specify workflow run ID |
| `--pr <number>` | PR number if fixing a PR-triggered workflow |
| `--type <type>` | Fix type: `test-failure`, `build-failure`, `security-issue`, `lint-error` |
| `--clarification <text>` | Additional context or hints for Claude |
| `--dry-run` | Analyze and show fix plan without applying changes |
| `--max-retries <n>` | Maximum retry attempts (default: 3) |

## Examples

### Fix a specific workflow run
```
/dev-workflow-automation:auto-fix 12345678
```

### Fix with type hint
```
/dev-workflow-automation:auto-fix --run-id 12345678 --type test-failure
```

### Fix with additional context
```
/dev-workflow-automation:auto-fix 12345678 --clarification "The test failure is related to database connection timeout"
```

### Dry run to see what would be fixed
```
/dev-workflow-automation:auto-fix 12345678 --dry-run
```

### Fix a PR-triggered workflow
```
/dev-workflow-automation:auto-fix 12345678 --pr 42
```

## Behavior

1. **Validate Inputs**
   - Verify workflow run ID exists
   - Check if run actually failed
   - Ensure no existing fix branch/PR

2. **Fetch Workflow Details**
   - Download artifacts from failed run
   - Retrieve failure logs
   - Identify affected files

3. **Parse Failure Details**
   - Detect failure type (test, build, security, lint)
   - Extract error messages
   - Identify root cause indicators

4. **Create Fix Branch**
   - Branch name: `fix/auto-{timestamp}-{type}-run-{id}`
   - Base: original workflow's branch

5. **Invoke Bug Fixer Agent**
   - Pass failure analysis as context
   - Include clarification if provided
   - Allow up to max-retries iterations

6. **Validate Fix**
   - Run relevant tests
   - Verify original failure is resolved
   - Check for regressions

7. **Create PR or Report**
   - On success: Create PR with fix
   - On failure: Report what was attempted

## Output

### Success Output
```
## Auto-Fix Results

✅ **Fix Applied Successfully**

- **Run ID**: 12345678
- **Type**: test-failure
- **Fix Branch**: fix/auto-20250123-test-failure-run-12345678
- **PR Created**: #123 (https://github.com/org/repo/pull/123)

### Changes Made
- `src/test/UserServiceTest.java` - Fixed null pointer exception in mock setup
- `src/main/UserService.java` - Added null check before processing

### Validation
- ✅ All tests pass
- ✅ No new warnings

**Action Required**: Please review and approve the PR before merging.
```

### Failure Output
```
## Auto-Fix Results

❌ **Fix Unsuccessful After 3 Attempts**

- **Run ID**: 12345678
- **Type**: build-failure
- **Attempts**: 3

### Analysis
The failure appears to be related to a missing dependency that requires
manual intervention to resolve.

### Attempted Fixes
1. Attempt 1: Updated dependency version (tests still failing)
2. Attempt 2: Added transitive dependency (build error persisted)
3. Attempt 3: Modified build configuration (compilation error)

### Recommended Manual Steps
1. Check if `com.example:missing-lib` is available in your repositories
2. Verify Maven settings.xml has correct repository configuration
3. Try `mvn dependency:tree` to identify conflict

### Re-trigger with Context
To retry with additional information:
```bash
/dev-workflow-automation:auto-fix 12345678 --clarification "The missing dependency should come from internal repo"
```
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Run not found` | Invalid run ID | Verify the run ID from GitHub Actions |
| `Run did not fail` | Attempting to fix successful run | Only failed runs can be auto-fixed |
| `Fix branch exists` | Duplicate fix attempt | Check existing PR or delete branch |
| `No artifacts available` | Artifacts expired or not uploaded | Run may need to be re-triggered first |

## Related Commands

- `/dev-workflow-automation:analyze-failure` - Analyze without fixing
- `/dev-workflow-automation:workflow-status` - Check auto-fix status
- `/dev-workflow-automation:auto-feature` - Implement features instead of fixes

## Implementation Notes

This command uses the `bug-fixer` agent internally with the following flow:

```
auto-fix command
    ↓
failure-analyzer agent (analyze)
    ↓
bug-fixer agent (fix)
    ↓
validation (test)
    ↓
PR creation (if success)
```

The command respects project conventions defined in `CLAUDE.md`.
