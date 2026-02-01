---
name: rlm:clear
description: Clear loaded contexts to free memory
allowed-tools: Read, Bash
---

# Clear RLM Contexts

Remove loaded contexts from memory and storage.

## Usage

```
/rlm:clear [context_id]
```

## Arguments

- `$1` - Optional: Specific context ID to clear. Clears all if not specified.

## Examples

```bash
# Clear all contexts
/rlm:clear

# Clear specific context
/rlm:clear abc123def456
```

## When to Clear

1. **Memory management**: Large contexts consume memory
2. **Starting fresh**: New document processing session
3. **Context switching**: Moving to different project

## What Gets Cleared

- In-memory context data
- Chunk indexes
- Query history
- Statistics (reset to zero)

## Persistent Data

Context files saved to disk are NOT automatically deleted:
- `{data_dir}/{context_id}.json` - Metadata
- `{data_dir}/{context_id}.txt` - Content

Delete these manually if needed.

## MCP Tool

This command uses `mcp__rlm-context__rlm_clear` under the hood.
