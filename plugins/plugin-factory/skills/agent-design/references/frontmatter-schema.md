# Agent Frontmatter Schema

Complete reference for agent YAML frontmatter.

## Required Fields

### name
- **Type**: string
- **Pattern**: kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`)
- **Purpose**: Unique identifier for the agent

```yaml
name: code-reviewer
```

### description
- **Type**: string
- **Purpose**: When Claude should delegate to this agent

```yaml
description: |
  Expert code review specialist.
  Use when: reviewing code, checking quality, security audit.
  Proactively invoked after code changes.
```

## Optional Fields

### tools
- **Type**: list or comma-separated string
- **Default**: Inherit all from parent
- **Purpose**: Allowed tools

```yaml
tools: Read, Write, Edit, Bash
```

Or as list:
```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
```

### disallowedTools
- **Type**: list or comma-separated string
- **Purpose**: Explicitly deny tools

```yaml
disallowedTools: WebSearch, WebFetch
```

### model
- **Type**: string
- **Default**: sonnet
- **Values**: sonnet, opus, haiku, inherit

```yaml
model: haiku  # Fast for validation tasks
```

### permissionMode
- **Type**: string
- **Default**: Inherit from parent
- **Values**: default, acceptEdits, dontAsk, bypassPermissions, plan

```yaml
permissionMode: plan  # Read-only exploration
```

### skills
- **Type**: comma-separated string
- **Purpose**: Skills to inject into agent context

```yaml
skills: plugin-patterns, heuristics-engine
```

**Note**: Skill content is fully injected at startup, not loaded on-demand.

### hooks
- **Type**: object
- **Purpose**: Agent-scoped lifecycle hooks

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
```

## Complete Example

```yaml
---
name: code-reviewer
description: |
  Expert code review specialist for quality and security.
  Use when: reviewing code, checking quality, security audit,
  code analysis, finding bugs, best practices check.
  Proactively invoked after code modifications.

tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: inherit
permissionMode: plan
skills: code-review-patterns

hooks:
  Stop:
    - hooks:
        - type: command
          command: "./scripts/save-review.sh"
---

# Code Reviewer Agent

You are an expert code reviewer focusing on quality and security.

## Review Process

1. Analyze recent changes
2. Check for issues
3. Provide actionable feedback

## Focus Areas

- Code quality
- Security vulnerabilities
- Best practices
- Performance

## Output Format

### Issue
**Type**: [Bug/Security/Performance/Style]
**Severity**: [Critical/High/Medium/Low]
**Location**: file:line
**Description**: What's wrong
**Fix**: How to fix

## Constraints

- DO NOT modify files
- DO provide specific suggestions
- ALWAYS include severity
```

## Validation

```bash
# Check name format
grep '^name:' agents/*.md | \
  sed 's/.*name: //' | \
  grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'

# Check description exists
for f in agents/*.md; do
  grep -q '^description:' "$f" || echo "Missing description: $f"
done

# Validate YAML
for f in agents/*.md; do
  sed -n '/^---$/,/^---$/p' "$f" | head -n -1 | tail -n +2 | \
    python -c "import yaml, sys; yaml.safe_load(sys.stdin)" || \
    echo "Invalid YAML: $f"
done
```
