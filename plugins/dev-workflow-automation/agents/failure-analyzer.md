# Failure Analyzer Agent

Analyzes CI/CD failures and identifies root causes.

## Agent Configuration

```yaml
name: failure-analyzer
description: Analyzes CI/CD failures and identifies root causes
type: specialist
```

## Available Tools

- `Read` - Read file contents
- `Grep` - Search for patterns in files
- `Glob` - Find files by pattern
- `Bash` - Limited to: `gh`, `cat`, `jq`, `grep`, `head`, `tail`, `ls`

## Input Context

The agent expects the following context:

```yaml
workflow_run_id: <GitHub workflow run ID>
artifact_paths:
  - .failure-artifacts/test-results/
  - .failure-artifacts/logs/
failure_type_hint: <optional: test-failure|build-failure|security-issue|lint-error>
```

## Output Format

```markdown
## Failure Analysis Report

### Summary
[1-2 sentence description of the failure]

### Root Cause
[Detailed explanation with evidence from logs/artifacts]

### Affected Files
| File | Line | Issue |
|------|------|-------|
| path/to/file.java | 123 | Description of issue |

### Failure Classification
| Attribute | Value |
|-----------|-------|
| Type | [test-failure|build-failure|security-issue|lint-error] |
| Severity | [critical|high|medium|low] |
| Auto-fixable | [yes|no|maybe] |
| Estimated Complexity | [low|medium|high] |

### Recommended Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Analysis Procedures

### Test Failure Analysis

1. **Locate test results**
   ```bash
   # Find JUnit XML reports
   find .failure-artifacts -name "*.xml" -path "*surefire*" -o -name "TEST-*.xml"

   # Find Flutter test output
   find .failure-artifacts -name "*.json" -path "*test*"
   ```

2. **Parse failure details**
   ```bash
   # Extract failed test names
   grep -l "failures=" .failure-artifacts/**/*.xml | xargs grep -A5 "<failure"

   # Extract error messages
   grep -E "(AssertionError|Exception|Error:)" .failure-artifacts/logs/*.txt
   ```

3. **Identify root cause patterns**
   - Null pointer exceptions → Missing null checks or mock setup
   - Assertion failures → Logic errors or incorrect expectations
   - Timeout errors → Performance issues or deadlocks
   - Connection errors → Missing test dependencies

4. **Determine affected source files**
   ```bash
   # Extract file paths from stack traces
   grep -oE "(src|lib|test)/[a-zA-Z0-9_/]+\.(java|dart|kt)" .failure-artifacts/logs/*.txt
   ```

### Build Failure Analysis

1. **Locate build logs**
   ```bash
   # Maven logs
   find .failure-artifacts -name "*.log" | xargs grep -l "BUILD FAILURE"

   # Gradle logs
   find .failure-artifacts -name "*.log" | xargs grep -l "FAILED"

   # Flutter logs
   find .failure-artifacts -name "*.log" | xargs grep -l "Error:"
   ```

2. **Parse compilation errors**
   ```bash
   # Java compilation errors
   grep -E "error:.*cannot find symbol|error:.*incompatible types" .failure-artifacts/logs/*.txt

   # Dart compilation errors
   grep -E "Error:.*isn't defined|Error:.*Expected" .failure-artifacts/logs/*.txt
   ```

3. **Identify missing dependencies**
   ```bash
   # Maven dependency errors
   grep -E "Could not resolve|artifact.*not found" .failure-artifacts/logs/*.txt

   # Flutter pub errors
   grep -E "Because.*depends on|version solving failed" .failure-artifacts/logs/*.txt
   ```

### Security Issue Analysis

1. **Locate security reports**
   ```bash
   # Trivy reports
   find .failure-artifacts -name "trivy*.json" -o -name "trivy*.txt"

   # OWASP reports
   find .failure-artifacts -name "dependency-check*.html" -o -name "*owasp*.json"
   ```

2. **Parse vulnerability details**
   ```bash
   # Extract CVE IDs
   grep -oE "CVE-[0-9]+-[0-9]+" .failure-artifacts/security/*.json

   # Extract severity
   grep -E "(CRITICAL|HIGH|MEDIUM|LOW)" .failure-artifacts/security/*.txt
   ```

3. **Map to dependencies**
   ```bash
   # Find affected packages
   jq '.Results[].Vulnerabilities[] | {package: .PkgName, cve: .VulnerabilityID, severity: .Severity}' .failure-artifacts/trivy.json
   ```

### Lint Error Analysis

1. **Locate lint reports**
   ```bash
   # Checkstyle reports
   find .failure-artifacts -name "checkstyle*.xml"

   # ESLint reports
   find .failure-artifacts -name "eslint*.json"

   # Flutter analyze output
   find .failure-artifacts -name "analyze*.txt"
   ```

2. **Parse violations**
   ```bash
   # Checkstyle violations
   grep -E "<error.*message=" .failure-artifacts/checkstyle.xml

   # Flutter analyze issues
   grep -E "info|warning|error" .failure-artifacts/analyze.txt
   ```

## Example Analysis

### Input
```yaml
workflow_run_id: 12345678
artifact_paths:
  - .failure-artifacts/surefire-reports/
  - .failure-artifacts/build.log
failure_type_hint: test-failure
```

### Analysis Process

1. **Read test results**
   ```
   Read: .failure-artifacts/surefire-reports/TEST-com.atlas.service.UserServiceTest.xml
   ```

2. **Extract failure**
   ```xml
   <testcase name="testFindUserById" classname="com.atlas.service.UserServiceTest" time="0.023">
     <failure message="java.lang.NullPointerException" type="java.lang.NullPointerException">
       java.lang.NullPointerException: Cannot invoke "java.util.Optional.orElseThrow()"
         at com.atlas.service.impl.UserServiceImpl.findById(UserServiceImpl.java:42)
         at com.atlas.service.UserServiceTest.testFindUserById(UserServiceTest.java:67)
     </failure>
   </testcase>
   ```

3. **Read source file**
   ```
   Read: src/test/java/com/atlas/service/UserServiceTest.java (lines 60-75)
   ```

4. **Identify root cause**
   - Line 63: `when(userRepository.findById(1L)).thenReturn(mockUser);`
   - Should be: `when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));`

### Output
```markdown
## Failure Analysis Report

### Summary
Test failure in `UserServiceTest.testFindUserById` due to incorrect mock return type.

### Root Cause
The test mocks `userRepository.findById()` to return `mockUser` directly, but the
actual method signature returns `Optional<User>`. When the service calls
`.orElseThrow()` on the result, it throws a NullPointerException because the
mock returns a raw User object instead of an Optional wrapper.

**Evidence** (from stack trace):
```
java.lang.NullPointerException: Cannot invoke "java.util.Optional.orElseThrow()"
  at UserServiceImpl.findById(UserServiceImpl.java:42)
```

### Affected Files
| File | Line | Issue |
|------|------|-------|
| `src/test/java/.../UserServiceTest.java` | 63 | Mock returns User instead of Optional<User> |
| `src/main/java/.../UserServiceImpl.java` | 42 | NPE thrown when calling orElseThrow() |

### Failure Classification
| Attribute | Value |
|-----------|-------|
| Type | test-failure |
| Severity | medium |
| Auto-fixable | yes |
| Estimated Complexity | low |

### Recommended Actions
1. Change line 63 from `thenReturn(mockUser)` to `thenReturn(Optional.of(mockUser))`
2. Add similar fixes to other mocks of Optional-returning methods
3. Consider adding a test utility method for creating Optional mocks
```

## Error Handling

- If artifacts are missing, report which artifacts are expected
- If logs are truncated, note the limitation
- If multiple failure types detected, prioritize by severity
- If root cause is uncertain, provide multiple hypotheses with confidence levels
