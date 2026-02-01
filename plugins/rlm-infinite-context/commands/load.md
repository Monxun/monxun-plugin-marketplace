---
name: rlm:load
description: Load a document or file into RLM infinite context storage for recursive searching
allowed-tools: Read, Bash, Glob
argument-validation: required
---

# Load Context into RLM

Load documents into the RLM (Recursive Language Model) system for processing contexts beyond the model's native context window.

## Usage

```
/rlm:load <source> [options]
```

## Arguments

- `$1` - Source path (file, directory, or URL)

## Options

- `--name`: Name for this context (default: filename)
- `--recursive`: Recursively load directory contents
- `--patterns`: File patterns to include (default: *.md,*.txt,*.py,*.js,*.ts)
- `--chunk-size`: Target chunk size in characters (default: 4000)

## Examples

```bash
# Load a single large file
/rlm:load ./massive-codebase.txt

# Load entire directory
/rlm:load ./docs --recursive

# Load with custom name
/rlm:load ./research-paper.pdf --name "MIT RLM Paper"
```

## How It Works

The RLM technique stores your content outside the model's context window:

1. **Chunking**: Content is split into overlapping chunks (~4000 chars each)
2. **Indexing**: Chunks are indexed for fast keyword and regex search
3. **Storage**: Content persists in external storage, not context window
4. **Searching**: Model uses tools to search through stored content

## Benefits

- Process documents with **10M+ tokens** (vs ~200K native limit)
- **No information loss** (unlike summarization)
- **Cost efficient** - only relevant chunks enter context
- **Recursive depth** - dive deeper into relevant sections

## Token Estimation

| Content Size | Estimated Tokens | Chunks |
|--------------|------------------|--------|
| 100 KB | ~25K | ~25 |
| 1 MB | ~250K | ~250 |
| 10 MB | ~2.5M | ~2500 |
| 100 MB | ~25M | ~25000 |

## Workflow

After loading, use these commands:
1. `/rlm:outline` - View document structure
2. `/rlm:search` - Search for specific content
3. `/rlm:query` - Answer questions about the content

## MCP Tool

This command uses `mcp__rlm-context__rlm_load` under the hood.
