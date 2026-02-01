---
name: rlm:search-deep
description: Perform recursive sub-search on specific chunks - the core RLM feature for deep information retrieval
allowed-tools: Read, Bash
argument-validation: required
---

# Recursive Deep Search

The key RLM innovation: dive deeper into relevant sections found in initial search.

## Usage

```
/rlm:search-deep <query> --chunks <chunk_ids>
```

## Arguments

- `$1` - What to search for within the selected chunks

## Options

- `--chunks`: Comma-separated list of chunk IDs to search within (required)
- `--parent`: Query ID of the parent search (for tracking)

## The Recursive Workflow

```
Step 1: Initial Search
   /rlm:search "authentication"
   → Returns chunks 15, 23, 47 as relevant

Step 2: Deep Search
   /rlm:search-deep "OAuth token refresh" --chunks 15,23,47
   → Searches ONLY within those chunks
   → Returns more specific results

Step 3: Even Deeper (if needed)
   /rlm:search-deep "refresh_token expiry" --chunks 15
   → Narrow down to exact implementation
```

## Why Recursive Search?

| Approach | Tokens Used | Quality |
|----------|-------------|---------|
| Full context | 10,000,000 | Poor (context rot) |
| Summarization | 50,000 | Lossy |
| RLM Recursive | 20,000 | Excellent |

The model only loads what it needs, when it needs it.

## Examples

```bash
# After finding authentication chapters
/rlm:search-deep "password hashing" --chunks 5,6,7

# Find specific function in code sections
/rlm:search-deep "validate_token" --chunks 23,24

# Track the search tree
/rlm:search-deep "error codes" --chunks 10 --parent q_0_abc123
```

## Result Structure

Results include:
- **recursive_info**: Shows this is a sub-query
- **depth**: How many levels deep this search is
- **source_chunks**: Which chunks were searched

## Maximum Depth

Default maximum recursion depth is 10 levels. This prevents:
- Infinite loops
- Excessive token usage
- Diminishing returns

## Best Practices

1. **Start broad**: Use `/rlm:search` first
2. **Identify hot spots**: Note which chunks have high relevance
3. **Go deep selectively**: Only dive into the most promising chunks
4. **Combine results**: Synthesize findings from different branches

## MCP Tool

This command uses `mcp__rlm-context__rlm_search_recursive` under the hood.
