---
name: rlm:status
description: View loaded contexts, statistics, and RLM session information
allowed-tools: Read, Bash
---

# RLM Status

View information about loaded contexts and session statistics.

## Usage

```
/rlm:status [options]
```

## Options

- `--stats`: Show detailed statistics including query depth distribution
- `--context`: Show details for specific context ID

## Output

### Contexts List
```json
{
  "contexts": [
    {
      "id": "abc123def456",
      "name": "research-paper.txt",
      "tokens": 2500000,
      "chunks": 2500,
      "created_at": "2026-01-18T10:30:00"
    }
  ],
  "active_session": "abc123def456"
}
```

### Statistics (with --stats)
```json
{
  "session_stats": {
    "total_queries": 45,
    "total_tokens_processed": 180000,
    "max_depth_reached": 4,
    "contexts_loaded": 2
  },
  "query_depth_distribution": {
    "0": 20,
    "1": 15,
    "2": 7,
    "3": 3
  },
  "configuration": {
    "max_depth": 10,
    "chunk_size": 4000,
    "overlap": 200
  }
}
```

## Examples

```bash
# Quick status check
/rlm:status

# Detailed statistics
/rlm:status --stats

# Check specific context
/rlm:status --context abc123def456
```

## Understanding Statistics

### Query Depth Distribution
Shows how many searches happened at each recursion level:
- **Depth 0**: Initial searches
- **Depth 1**: First-level recursive searches
- **Depth 2+**: Deeper explorations

Higher max depth reached indicates complex queries requiring deep exploration.

### Token Efficiency
Compare `total_tokens_processed` with `total tokens in contexts`:
- Low ratio = efficient searches
- High ratio = may need to optimize queries

## MCP Tools

This command uses:
- `mcp__rlm-context__rlm_list`
- `mcp__rlm-context__rlm_stats`
