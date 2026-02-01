# CI/CD Remediation Skill

Auto-invoked skill for CI/CD failure detection and remediation.

## Triggers

This skill is automatically invoked when the user mentions:
- "CI failure"
- "workflow failed"
- "test failure"
- "build failed"
- "fix the build"
- "fix the pipeline"
- "pipeline error"
- "tests are failing"
- "build is broken"

## Purpose

Provides intelligent assistance for diagnosing and fixing CI/CD pipeline failures,
including test failures, build errors, security issues, and lint violations.

## Capabilities

1. **Failure Analysis**
   - Parse error logs and test results
   - Identify root causes
   - Classify failure types

2. **Automated Remediation**
   - Suggest fixes based on patterns
   - Apply common fix patterns
   - Validate fixes with tests

3. **GitHub Integration**
   - Fetch workflow run details
   - Download artifacts
   - Create fix branches and PRs

## Usage

When triggered, the skill will:

1. **Detect Context**
   - Check for recent failed workflow runs
   - Look for error messages in conversation
   - Identify relevant files

2. **Offer Assistance**
   ```
   I noticed you're dealing with a CI/CD failure. I can help with:

   1. **Analyze** - Deep dive into the failure logs
   2. **Auto-Fix** - Attempt automatic remediation
   3. **Guide** - Walk through manual fix steps

   Which would you like me to do?
   ```

3. **Execute Based on Choice**

### Analysis Mode

```markdown
## Failure Analysis

I've analyzed the recent CI failure. Here's what I found:

### Summary
[Brief description]

### Root Cause
[Detailed explanation]

### Affected Files
- file1.java:123
- file2.dart:45

### Recommended Fix
[Specific fix recommendation]

Would you like me to apply this fix automatically?
```

### Auto-Fix Mode

```markdown
## Applying Auto-Fix

I'm going to:
1. Create a fix branch: `fix/auto-{description}`
2. Apply the following changes: [summary]
3. Run tests to validate
4. Create a PR if successful

Proceeding...

[... execution output ...]

✅ Fix applied successfully!
PR created: #123 - [link]

Please review and approve the PR to merge the fix.
```

### Guide Mode

```markdown
## Manual Fix Guide

Here's how to fix this issue:

### Step 1: Understand the Error
[Explanation of what went wrong]

### Step 2: Locate the Problem
```bash
# Commands to find the issue
```

### Step 3: Apply the Fix
```java
// Code changes needed
```

### Step 4: Validate
```bash
# Commands to verify the fix
```

Would you like me to walk you through any of these steps?
```

## Integration with Commands

This skill integrates with the plugin commands:

| Command | When to Use |
|---------|-------------|
| `/dev-workflow-automation:analyze-failure <run-id>` | Detailed analysis of specific run |
| `/dev-workflow-automation:auto-fix <run-id>` | Apply automatic fix |
| `/dev-workflow-automation:workflow-status` | Check overall CI health |

## Proactive Behavior

When working with the user and a CI failure is detected:

1. **Alert the user**
   ```
   ⚠️ I noticed the CI pipeline just failed. Would you like me to investigate?
   ```

2. **Offer quick actions**
   ```
   Quick actions:
   - `/dev-workflow-automation:analyze-failure 12345678`
   - View logs: [link to GitHub Actions]
   ```

3. **Prevent broken commits**
   ```
   Before committing, I noticed the tests might fail due to [issue].
   Should I fix this first?
   ```

## Example Interactions

### Example 1: User mentions failure
```
User: The CI build failed again

Claude: I can help with that CI failure. Let me check the recent workflow runs...

[Fetches recent runs]

I found a failed run from 10 minutes ago:
- **Workflow**: Backend CI
- **Run**: #12345678
- **Error Type**: Test failure

Would you like me to:
1. **Analyze** - Deep dive into what went wrong
2. **Auto-fix** - Try to fix it automatically
3. **Show logs** - Display the error details
```

### Example 2: User asks to fix
```
User: Fix the failing tests

Claude: I'll analyze and fix the failing tests.

[Analyzing run #12345678...]

Found the issue: Mock configuration error in `UserServiceTest`

Applying fix:
- Modified `UserServiceTest.java` (3 lines changed)
- All tests now pass

Creating PR...

✅ Fix ready for review: PR #42
https://github.com/org/repo/pull/42

Please review the changes and approve to merge.
```

### Example 3: User wants to understand
```
User: Why is the build broken?

Claude: Let me analyze the recent failure...

## Build Failure Analysis

### What Happened
The build failed during the test phase with a `NullPointerException`.

### Root Cause
The test `testFindUserById` expects the repository mock to return an `Optional<User>`,
but it's currently configured to return just `User`. When the service calls
`.orElseThrow()`, it fails because it receives a raw object instead of an Optional.

### Where It Broke
- `UserServiceTest.java:63` - Mock returns wrong type
- `UserServiceImpl.java:42` - NPE thrown here

### How to Fix
Change the mock configuration from:
```java
when(repository.findById(1L)).thenReturn(user);
```
To:
```java
when(repository.findById(1L)).thenReturn(Optional.of(user));
```

Would you like me to apply this fix?
```

## Configuration

The skill behavior can be customized in the plugin configuration:

```json
{
  "skills": {
    "cicd-remediation": {
      "auto_detect": true,
      "proactive_alerts": true,
      "auto_fix_threshold": "high_confidence",
      "require_confirmation": true
    }
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `auto_detect` | true | Automatically detect CI failures |
| `proactive_alerts` | true | Alert user about new failures |
| `auto_fix_threshold` | "high_confidence" | When to suggest auto-fix |
| `require_confirmation` | true | Ask before applying fixes |
