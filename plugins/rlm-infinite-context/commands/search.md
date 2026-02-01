---
name: rlm:search
description: Search through loaded RLM context using keywords, regex, or semantic sections
allowed-tools: Read, Bash
argument-validation: required
---

# Search RLM Context

Search through loaded content using the RLM recursive search system.

## Usage

```
/rlm:search <query> [options]
```

## Arguments

- `$1` - Search query (keywords, regex pattern, or section name)

## Options

- `--type`: Search type (auto, keyword, regex, section)
- `--top-k`: Number of results (default: 5)
- `--context`: Specific context ID to search

## Search Types

### Auto (Default)
Automatically detects the best search strategy:
- Uses regex if query contains special characters
- Uses section search for chapter/function queries
- Falls back to keyword search

### Keyword Search
```bash
/rlm:search "authentication error handling" --type keyword
```
Finds chunks containing specified keywords.

### Regex Search
```bash
/rlm:search "def\s+\w+_handler\(" --type regex
```
Powerful pattern matching for code and structured content.

### Section Search
```bash
/rlm:search "Chapter 5" --type section
```
Finds document sections, headers, and logical divisions.

## Examples

```bash
# Find all mentions of a concept
/rlm:search "recursive language model"

# Find specific code patterns
/rlm:search "class.*Controller" --type regex

# Find chapters or sections
/rlm:search "Introduction" --type section

# Get more results
/rlm:search "error handling" --top-k 10
```

## Understanding Results

Each result includes:
- **chunk_id**: Unique identifier for the chunk
- **relevance**: Score from 0-1 indicating match quality
- **content**: The matched content (truncated if large)
- **position**: Character position in original document

## Recursive Searching

After finding relevant chunks, use `/rlm:search-deep` to:
1. Take chunk IDs from results
2. Search deeper within those chunks
3. Find specific details in relevant sections

This is the core RLM innovation - recursive depth!

## MCP Tool

This command uses `mcp__rlm-context__rlm_search` under the hood.
