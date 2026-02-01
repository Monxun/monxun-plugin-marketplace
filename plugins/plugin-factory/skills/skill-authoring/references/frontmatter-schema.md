# Skill Frontmatter Schema

Complete reference for SKILL.md YAML frontmatter.

## Schema Overview

```yaml
---
name: string          # Required, max 64 chars
description: string   # Required, max 1024 chars
allowed-tools: list   # Optional
model: string         # Optional
context: string       # Optional
agent: string         # Optional
hooks: object         # Optional
user-invocable: bool  # Optional
---
```

## Required Fields

### name

**Type**: string
**Max Length**: 64 characters
**Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$`

Valid names:
- `my-skill`
- `code-analyzer`
- `deploy-v2`

Invalid names:
- `My Skill` (spaces, uppercase)
- `mySkill` (camelCase)
- `my_skill` (underscores)
- `anthropic-tool` (reserved word)
- `claude-helper` (reserved word)

### description

**Type**: string
**Max Length**: 1024 characters
**Purpose**: Trigger auto-discovery and explain capability

**Format**:
```yaml
description: |
  [What the skill does - brief]
  Use when: [trigger keywords]
  Supports: [capabilities]
```

**Example**:
```yaml
description: |
  Creates and manages database migrations.
  Use when: database migration, schema change, migrate db,
  create migration, run migrations, migration script.
  Supports: PostgreSQL, MySQL, SQLite.
```

## Optional Fields

### allowed-tools

**Type**: list or comma-separated string
**Purpose**: Restrict which tools the skill can use

**List format**:
```yaml
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
```

**String format**:
```yaml
allowed-tools: Read, Write, Edit, Bash
```

**Available tools**:
- `Read` - File reading
- `Write` - File creation
- `Edit` - File modification
- `Bash` - Shell commands
- `Grep` - Content search
- `Glob` - File pattern matching
- `WebSearch` - Web search
- `WebFetch` - URL fetching
- `Task` - Subagent delegation

**Pattern restrictions**:
```yaml
allowed-tools:
  - Read
  - Bash(git *)      # Only git commands
  - Bash(npm run:*)  # Only npm run commands
```

### model

**Type**: string
**Purpose**: Override the model used

**Values**:
- `claude-sonnet-4-20250514`
- `claude-opus-4-5-20251101`
- `claude-3-5-haiku-20241022`

**Example**:
```yaml
model: claude-sonnet-4-20250514
```

### context

**Type**: string
**Purpose**: Run in isolated context

**Values**:
- `fork` - Run in separate context

**Example**:
```yaml
context: fork
agent: general-purpose
```

### agent

**Type**: string
**Purpose**: Agent type when forked

**Values**:
- `general-purpose` - Full capabilities
- `Explore` - Read-only exploration
- `Plan` - Planning mode
- Custom agent name

**Example**:
```yaml
context: fork
agent: Explore
```

### hooks

**Type**: object
**Purpose**: Skill-scoped lifecycle hooks

**Supported events**:
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `Stop` - When skill finishes

**Example**:
```yaml
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "${SKILL_DIR}/scripts/validate.sh"
          once: true
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "${SKILL_DIR}/scripts/format.sh"
```

**Special options**:
- `once: true` - Run only once per session

### user-invocable

**Type**: boolean
**Default**: true
**Purpose**: Control slash menu visibility

**Example**:
```yaml
user-invocable: false  # Hidden from /skill-name
```

## Environment Variables

Available in hook commands:
- `${SKILL_DIR}` - Skill directory path
- `${CLAUDE_PROJECT_DIR}` - Project root

## Complete Example

```yaml
---
name: database-migration
description: |
  Creates and manages database migrations.
  Use when: database migration, schema change, migrate db,
  create migration, run migrations, migration script,
  "create migration", "run migration".
  Supports: PostgreSQL, MySQL, SQLite migrations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(npm run migrate:*)
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "${SKILL_DIR}/scripts/validate-migration.sh"
---
```

## Validation

### Check name format
```bash
grep '^name:' SKILL.md | sed 's/name: //' | \
  grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'
```

### Check description length
```bash
sed -n '/^description:/,/^[a-z-]*:/p' SKILL.md | \
  head -n -1 | wc -c
# Should be <= 1024
```

### Validate YAML
```bash
sed -n '/^---$/,/^---$/p' SKILL.md | head -n -1 | tail -n +2 | \
  python -c "import yaml, sys; yaml.safe_load(sys.stdin)"
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing description | Won't trigger | Add description with keywords |
| Name > 64 chars | Won't load | Shorten name |
| Invalid name chars | Won't load | Use only lowercase, hyphens |
| Vague description | Poor matching | Add specific trigger keywords |
