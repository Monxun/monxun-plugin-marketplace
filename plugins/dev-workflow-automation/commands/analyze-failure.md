# /dev-workflow-automation:analyze-failure

Analyze a CI/CD failure without creating a fix. Returns root cause analysis and recommendations.

## Usage

```
/dev-workflow-automation:analyze-failure <run-id> [options]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<run-id>` | GitHub workflow run ID to analyze (required) |

## Options

| Option | Description |
|--------|-------------|
| `--run-id <id>` | Alternative way to specify workflow run ID |
| `--logs` | Include full failure logs in output |
| `--suggest-fix` | Include specific fix suggestions |
| `--verbose` | Show detailed analysis process |
| `--format <fmt>` | Output format: `markdown` (default), `json`, `brief` |

## Examples

### Basic analysis
```
/dev-workflow-automation:analyze-failure 12345678
```

### Analysis with fix suggestions
```
/dev-workflow-automation:analyze-failure 12345678 --suggest-fix
```

### Full analysis with logs
```
/dev-workflow-automation:analyze-failure 12345678 --logs --suggest-fix
```

### Brief summary
```
/dev-workflow-automation:analyze-failure 12345678 --format brief
```

### JSON output for scripting
```
/dev-workflow-automation:analyze-failure 12345678 --format json
```

## Behavior

1. **Fetch Workflow Run**
   - Retrieve run metadata
   - Identify workflow type and trigger

2. **Download Artifacts**
   - Test results (JUnit XML, surefire reports)
   - Build logs
   - Security scan outputs

3. **Parse Failure Details**
   - Extract error messages
   - Identify failure patterns
   - Locate affected code

4. **Classify Failure**
   - Determine failure type
   - Assess severity
   - Evaluate auto-fixability

5. **Generate Analysis**
   - Root cause determination
   - Impact assessment
   - Fix recommendations (if requested)

## Output

### Standard Analysis Output
```
## Failure Analysis Report

### Summary
Test failure in `UserServiceTest` due to null pointer exception when
mocking repository response.

### Root Cause
The test `testFindUserById` expects `userRepository.findById()` to return
an Optional containing a User object, but the mock is configured to return
`null` instead of `Optional.empty()`.

**Evidence**:
```
java.lang.NullPointerException: Cannot invoke "java.util.Optional.orElseThrow()"
  at com.atlas.service.impl.UserServiceImpl.findById(UserServiceImpl.java:42)
  at com.atlas.service.UserServiceTest.testFindUserById(UserServiceTest.java:67)
```

### Affected Files
| File | Line | Issue |
|------|------|-------|
| `src/test/java/.../UserServiceTest.java` | 67 | Incorrect mock setup |
| `src/main/java/.../UserServiceImpl.java` | 42 | NPE thrown here |

### Failure Classification
| Attribute | Value |
|-----------|-------|
| Type | `test-failure` |
| Severity | `medium` |
| Auto-fixable | `yes` |
| Estimated Complexity | `low` |

### Recommended Actions
1. Update mock setup in `UserServiceTest.java:55` to return `Optional.of(user)` instead of `user`
2. Alternatively, configure mock to return `Optional.empty()` for negative test cases
3. Consider adding null-safety annotations to service methods
```

### With `--suggest-fix` Output
```
### Suggested Fix

**File**: `src/test/java/com/atlas/service/UserServiceTest.java`

**Current Code** (line 55):
```java
when(userRepository.findById(1L)).thenReturn(mockUser);
```

**Fixed Code**:
```java
when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));
```

**Explanation**: The repository returns `Optional<User>`, not `User` directly.
The mock must return an Optional wrapper.

**Confidence**: High (95%)

To apply this fix automatically:
```
/dev-workflow-automation:auto-fix 12345678
```
```

### With `--logs` Output
```
### Full Failure Logs

<details>
<summary>Click to expand logs</summary>

```
[INFO] Running com.atlas.service.UserServiceTest
[ERROR] Tests run: 5, Failures: 1, Errors: 0, Skipped: 0
[ERROR] testFindUserById(com.atlas.service.UserServiceTest)
Time elapsed: 0.023 s  <<< FAILURE!
java.lang.NullPointerException: Cannot invoke "java.util.Optional.orElseThrow()"
  at com.atlas.service.impl.UserServiceImpl.findById(UserServiceImpl.java:42)
  at com.atlas.service.UserServiceTest.testFindUserById(UserServiceTest.java:67)
...
```

</details>
```

### JSON Output (`--format json`)
```json
{
  "run_id": 12345678,
  "workflow": "Backend CI",
  "status": "failure",
  "analysis": {
    "summary": "Test failure in UserServiceTest",
    "root_cause": "Incorrect mock return type",
    "type": "test-failure",
    "severity": "medium",
    "auto_fixable": true,
    "complexity": "low"
  },
  "affected_files": [
    {
      "path": "src/test/java/com/atlas/service/UserServiceTest.java",
      "line": 67,
      "issue": "Incorrect mock setup"
    }
  ],
  "recommendations": [
    "Update mock to return Optional.of(user)"
  ],
  "suggested_fix": {
    "file": "src/test/java/com/atlas/service/UserServiceTest.java",
    "line": 55,
    "before": "when(userRepository.findById(1L)).thenReturn(mockUser);",
    "after": "when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));",
    "confidence": 0.95
  }
}
```

### Brief Output (`--format brief`)
```
Run #12345678: TEST FAILURE (medium severity)
Root Cause: Incorrect mock return type in UserServiceTest.java:55
Auto-fixable: Yes
Fix: /dev-workflow-automation:auto-fix 12345678
```

## Failure Types

| Type | Indicators | Typical Causes |
|------|-----------|----------------|
| `test-failure` | AssertionError, test failures | Logic bugs, mock issues, data setup |
| `build-failure` | Compilation errors, BUILD FAILED | Syntax errors, missing imports |
| `security-issue` | CVE-, CRITICAL, HIGH severity | Vulnerable dependencies |
| `lint-error` | checkstyle, eslint warnings | Code style violations |
| `dependency-error` | Could not resolve, artifact not found | Missing or incompatible deps |
| `infrastructure` | Timeout, connection refused | CI environment issues |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Run not found` | Invalid or expired run ID | Check run ID is correct |
| `Artifacts not available` | Artifacts expired (90 days) | Re-run workflow to generate new artifacts |
| `Access denied` | Insufficient permissions | Ensure you have read access to the repo |

## Related Commands

- `/dev-workflow-automation:auto-fix` - Automatically fix the failure
- `/dev-workflow-automation:workflow-status` - View recent failures
- `/dev-workflow-automation:auto-feature` - Implement features

## Implementation Notes

This command uses the `failure-analyzer` agent to:
1. Parse test results (JUnit XML, surefire reports)
2. Analyze build logs (Maven, Gradle, Flutter)
3. Process security scans (Trivy, OWASP)
4. Identify patterns in error messages

The analysis is read-only and does not modify any files.
