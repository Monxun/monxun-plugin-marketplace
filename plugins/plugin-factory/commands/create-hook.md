---
name: create-hook
description: Create event hooks with validation scripts for plugin automation
allowed-tools: Read, Write, Edit, Bash, Glob
argument-validation: optional
---

# Create Hook Command

Generate hooks.json configuration and hook scripts.

## Usage

```
/plugin-factory:create-hook <event-type> [target-plugin]
```

## Arguments

- `$1` - Event type (PreToolUse, PostToolUse, Stop, etc.)
- `$2` - Target plugin directory (optional)

## Workflow

Delegates to `hook-builder` agent which:

1. Validates event type against 12 supported types
2. Creates/updates hooks.json
3. Generates hook script with proper exit codes
4. Sets executable permissions
5. Tests hook execution

## Injected Skills

- `hook-engineering` - Event types, exit codes, JSON control

## Event Types

| Event | Timing | Use Case |
|-------|--------|----------|
| PreToolUse | Before tool | Validation, blocking |
| PostToolUse | After tool | Logging, transformation |
| Stop | Session end | Cleanup, reporting |
| SessionStart | Session begin | Context injection |

## Exit Codes

- `0` - Success, continue (parse JSON if present)
- `2` - Block operation (stderr shown to Claude)
- Other - Non-blocking error, continues

## Example

```bash
# Create a pre-tool validation hook
/plugin-factory:create-hook PreToolUse

# Create session start hook
/plugin-factory:create-hook SessionStart ./my-plugin
```
