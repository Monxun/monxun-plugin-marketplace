# /dev-workflow-automation:auto-feature

Implement a feature from a GitHub issue or inline description.

## Usage

```
/dev-workflow-automation:auto-feature [options]
```

## Options

| Option | Description |
|--------|-------------|
| `--issue <number>` | GitHub issue number to implement |
| `--description <text>` | Inline feature description (alternative to issue) |
| `--target-branch <branch>` | Branch to create PR against (default: `develop`) |
| `--dry-run` | Show implementation plan without making changes |
| `--scope <scope>` | Limit scope: `backend`, `frontend`, `both` (default: auto-detect) |

## Examples

### Implement from GitHub issue
```
/dev-workflow-automation:auto-feature --issue 42
```

### Implement from inline description
```
/dev-workflow-automation:auto-feature --description "Add a dark mode toggle to the settings screen"
```

### Specify target branch
```
/dev-workflow-automation:auto-feature --issue 42 --target-branch main
```

### Backend-only implementation
```
/dev-workflow-automation:auto-feature --issue 42 --scope backend
```

### Dry run to see implementation plan
```
/dev-workflow-automation:auto-feature --issue 42 --dry-run
```

## Behavior

1. **Extract Requirements**
   - Parse issue body for acceptance criteria
   - Identify mentioned files/components
   - Detect scope (backend/frontend/both)

2. **Create Feature Branch**
   - Branch name: `feature/auto-{issue}-{slug}`
   - Base: specified target branch

3. **Research Codebase**
   - Find relevant existing patterns
   - Identify files to modify
   - Check for similar implementations

4. **Plan Implementation**
   - Design approach based on existing patterns
   - Identify all files to create/modify
   - Plan test coverage

5. **Implement Feature**
   - Create/modify files as planned
   - Follow project coding conventions
   - Add appropriate comments

6. **Write Tests**
   - Unit tests for new functionality
   - Integration tests if needed
   - Update existing tests if modified

7. **Validate**
   - Run full test suite
   - Check for lint/style violations
   - Verify build succeeds

8. **Create PR**
   - Link to original issue
   - Include implementation summary
   - Add labels: `auto-feature`, `needs-review`

## Output

### Success Output
```
## Feature Implementation Results

✅ **Feature Implemented Successfully**

- **Issue**: #42 - Add dark mode toggle to settings
- **Feature Branch**: feature/auto-42-dark-mode-toggle
- **PR Created**: #123 (https://github.com/org/repo/pull/123)
- **Target Branch**: develop

### Implementation Summary
Implemented dark mode toggle with system preference detection and
persistent user preference storage.

### Files Created
- `lib/providers/theme_provider.dart` - Theme state management
- `lib/widgets/settings/dark_mode_toggle.dart` - Toggle widget

### Files Modified
- `lib/screens/settings/settings_screen.dart` - Added toggle to settings
- `lib/main.dart` - Integrated ThemeProvider
- `lib/themes/app_theme.dart` - Added dark theme colors

### Tests Added
- `test/providers/theme_provider_test.dart` - 5 test cases
- `test/widgets/dark_mode_toggle_test.dart` - 3 test cases

### Validation
- ✅ All tests pass (42 passed, 0 failed)
- ✅ No lint warnings
- ✅ Build successful

**Action Required**: Please review the PR and verify it meets your expectations.
```

### Failure Output
```
## Feature Implementation Results

⚠️ **Partial Implementation - Tests Failing**

- **Issue**: #42 - Add dark mode toggle to settings
- **Feature Branch**: feature/auto-42-dark-mode-toggle
- **Status**: Implementation complete but tests failing

### What Was Implemented
- Dark mode toggle widget
- Theme provider for state management
- Dark theme color scheme

### Issues Encountered
The implementation is complete but some existing tests are failing due to
changes in the theme structure.

### Failing Tests
1. `test/widgets/common/app_button_test.dart` - Theme color mismatch
2. `test/screens/home_test.dart` - Missing theme provider in test setup

### Recommended Actions
1. Update test fixtures to include ThemeProvider
2. Review theme color usage in affected widgets

### Re-trigger with Context
```bash
/dev-workflow-automation:auto-feature --issue 42 --description "Focus on fixing the test setup for theme provider integration"
```
```

## Issue Format

For best results, format your GitHub issues with clear structure:

```markdown
## Description
Brief description of the feature.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes (Optional)
Any specific implementation hints or constraints.

## Affected Components (Optional)
- Settings screen
- User preferences
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Issue not found` | Invalid issue number | Verify issue exists in repository |
| `Issue not a feature request` | Missing `feature-request` label | Add appropriate label to issue |
| `No requirements found` | Empty or unclear issue body | Update issue with clear requirements |
| `Scope ambiguous` | Can't determine backend/frontend | Use `--scope` option explicitly |

## Related Commands

- `/dev-workflow-automation:auto-fix` - Fix bugs instead of features
- `/dev-workflow-automation:analyze-failure` - Analyze CI failures
- `/dev-workflow-automation:workflow-status` - Check implementation status

## Implementation Notes

This command uses the `feature-implementer` agent with the following flow:

```
auto-feature command
    ↓
requirements extraction
    ↓
codebase research (Explore agent)
    ↓
feature-implementer agent
    ↓
test suite execution
    ↓
PR creation (if tests pass)
```

The implementation follows patterns defined in `CLAUDE.md`:
- Backend: Java/Spring Boot conventions
- Frontend: Dart/Flutter conventions
- Tests required for all new functionality
