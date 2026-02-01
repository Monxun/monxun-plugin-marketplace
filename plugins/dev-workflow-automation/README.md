# Dev Workflow Automation Plugin

A comprehensive Claude Code plugin that automates bug detection, remediation, and feature implementation through GitHub Actions workflows.

## Features

- **Auto-trigger on CI/CD failures** - No manual labeling required
- **Self-hosted runner execution** - Uses your Max subscription Claude Code session
- **Comprehensive failure handling** - Creates issues, comments on runs, supports follow-up prompts
- **Full scope support** - Both bug fixes AND feature implementation
- **Human approval required** - All automated changes require PR approval before merge

## Quick Start

### 1. Install the Plugin

Copy the plugin directory to your Claude Code plugins location:

```bash
cp -r claude-code-plugins/workflows/dev-workflow-automation ~/.claude/plugins/
```

Or add to your project's `.claude/plugins/` directory.

### 2. Copy Workflows to Repository

Copy the GitHub Actions workflows to your repository:

```bash
cp claude-code-plugins/workflows/dev-workflow-automation/workflows/*.yml .github/workflows/
```

### 3. Configure Self-Hosted Runner

Ensure you have a self-hosted runner configured with:
- Labels: `self-hosted`, `macOS`, `ARM64`
- Claude Code CLI installed and authenticated
- `gh` CLI installed and authenticated

### 4. Use the Plugin

```bash
# Analyze a CI failure
/dev-workflow-automation:analyze-failure <run-id>

# Auto-fix a failure
/dev-workflow-automation:auto-fix <run-id>

# Implement a feature from an issue
/dev-workflow-automation:auto-feature --issue 42

# Check workflow status
/dev-workflow-automation:workflow-status
```

## Architecture

```
dev-workflow-automation/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/
│   ├── auto-fix.md           # /dev-workflow-automation:auto-fix
│   ├── auto-feature.md       # /dev-workflow-automation:auto-feature
│   ├── analyze-failure.md    # /dev-workflow-automation:analyze-failure
│   └── workflow-status.md    # /dev-workflow-automation:workflow-status
├── agents/
│   ├── failure-analyzer.md   # Analyzes CI/CD failures
│   ├── bug-fixer.md          # Implements bug fixes
│   └── feature-implementer.md # Implements features
├── skills/
│   └── cicd-remediation/
│       └── SKILL.md          # Auto-invoked for CI/CD issues
├── hooks/
│   ├── hooks.json            # Hook configuration
│   └── scripts/              # Hook scripts
├── workflows/
│   ├── auto-remediate.yml    # Main remediation workflow
│   ├── feature-request.yml   # Feature implementation workflow
│   └── claude-code-base.yml  # Reusable Claude Code workflow
├── scripts/
│   ├── parse-test-results.py # Parse test failure details
│   ├── parse-security-scan.py # Parse security findings
│   └── create-fix-branch.sh  # Branch creation helper
└── README.md
```

## Commands

### `/dev-workflow-automation:auto-fix`

Manually trigger auto-fix for a specific CI/CD failure.

```bash
# Basic usage
/dev-workflow-automation:auto-fix 12345678

# With type hint
/dev-workflow-automation:auto-fix --run-id 12345678 --type test-failure

# With clarification
/dev-workflow-automation:auto-fix 12345678 --clarification "Database timeout issue"

# Dry run
/dev-workflow-automation:auto-fix 12345678 --dry-run
```

### `/dev-workflow-automation:auto-feature`

Implement a feature from a GitHub issue or inline description.

```bash
# From issue
/dev-workflow-automation:auto-feature --issue 42

# Inline description
/dev-workflow-automation:auto-feature --description "Add dark mode toggle"

# Specify target branch
/dev-workflow-automation:auto-feature --issue 42 --target-branch main
```

### `/dev-workflow-automation:analyze-failure`

Analyze a CI failure without creating a fix.

```bash
# Basic analysis
/dev-workflow-automation:analyze-failure 12345678

# With fix suggestions
/dev-workflow-automation:analyze-failure 12345678 --suggest-fix

# Include logs
/dev-workflow-automation:analyze-failure 12345678 --logs
```

### `/dev-workflow-automation:workflow-status`

Show status of auto-remediation workflows.

```bash
# Default status (7 days)
/dev-workflow-automation:workflow-status

# Pending PRs only
/dev-workflow-automation:workflow-status --pending

# Statistics
/dev-workflow-automation:workflow-status --stats --days 30
```

## GitHub Actions Workflows

### Auto-Remediate (`auto-remediate.yml`)

Automatically triggers on CI/CD failures to analyze and fix issues.

**Triggers:**
- `workflow_run` completed with failure (auto-triggers on all failures)
- `workflow_dispatch` for manual trigger with clarification

**Flow:**
1. Check for duplicate fix attempts
2. Download artifacts and parse failure details
3. Create fix branch
4. Execute Claude Code CLI to analyze and fix
5. Run validation tests
6. Create PR if successful, or create issue if failed

### Feature Request (`feature-request.yml`)

Implements features from GitHub issues.

**Triggers:**
- Issues labeled with `feature-request` AND `auto-implement`
- `workflow_dispatch` with feature description

**Flow:**
1. Extract requirements from issue
2. Create feature branch
3. Execute Claude Code CLI to implement
4. Run tests
5. Create PR linked to issue

### Claude Code Base (`claude-code-base.yml`)

Reusable workflow for Claude Code execution.

**Why Self-Hosted CLI?**

| Aspect | API Action | Self-Hosted CLI |
|--------|-----------|-----------------|
| Authentication | ANTHROPIC_API_KEY | Your Max subscription |
| Configuration | Limited | Full .claude/ config |
| Skills/Plugins | Not available | All installed plugins |
| Cost | Per-token billing | Included in subscription |

## Configuration

### Plugin Configuration

The plugin can be configured via `plugin.json`:

```json
{
  "configuration": {
    "maxRetries": 3,
    "maxTurns": 15,
    "createIssueOnFailure": true,
    "commentOnFailedRun": true,
    "requirePRApproval": true
  }
}
```

### Self-Hosted Runner Setup

1. **Install runner:**
   ```bash
   # Follow GitHub's self-hosted runner setup
   # https://docs.github.com/en/actions/hosting-your-own-runners
   ```

2. **Install Claude Code:**
   ```bash
   npm install -g @anthropic-ai/claude-code
   claude auth login
   ```

3. **Install dependencies:**
   ```bash
   brew install gh jq python3
   gh auth login
   ```

4. **Configure runner labels:**
   - `self-hosted`
   - `macOS`
   - `ARM64`

## Failure Handling

When auto-fix fails after maximum retry attempts:

1. **GitHub Issue Created**
   - Title: `[Auto-Fix Failed] {type} in {workflow}`
   - Full error analysis and attempted fixes
   - Labels: `auto-fix-failed`, `needs-human`, `priority:high`

2. **Comment on Failed Run**
   - Analysis of what was tried
   - Link to created issue
   - Suggested manual steps

3. **Follow-Up Dispatch Support**
   - Re-trigger with additional context:
     ```bash
     gh workflow run auto-remediate.yml \
       -f failure_run_id=12345678 \
       -f fix_type=test-failure \
       -f clarification="Additional context"
     ```

## Security

- **No secrets in commits** - Hooks validate file contents
- **Command validation** - Prevents dangerous operations
- **PR approval required** - All changes need human review
- **Audit trail** - Full logging in PR descriptions

## Troubleshooting

### Plugin not loading

```bash
# Check plugin structure
ls -la ~/.claude/plugins/dev-workflow-automation/

# Verify plugin.json
cat ~/.claude/plugins/dev-workflow-automation/.claude-plugin/plugin.json | jq
```

### Workflows not triggering

```bash
# Check workflow permissions
gh api repos/{owner}/{repo}/actions/permissions

# View recent runs
gh run list --workflow auto-remediate.yml
```

### Claude CLI not working on runner

```bash
# Check Claude is installed
which claude
claude --version

# Check authentication
claude auth status
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a PR

## License

MIT License - See LICENSE file for details.

## Related

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Atlas Project](https://github.com/Atlas-AI-Labs/Atlas)
