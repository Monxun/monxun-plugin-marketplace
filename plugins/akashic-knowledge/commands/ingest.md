---
name: akashic:ingest
description: Ingest documents into an Akashic knowledge base from directory, files, or URLs
---

# Ingest Documents

Ingest documents into an existing knowledge base for indexing and search.

## Usage

```
/akashic:ingest <kb-name> <source> [options]
```

## Parameters

- **kb-name**: Target knowledge base name
- **source**: Path to directory, file, or URL to ingest

## Options

- `--recursive`: Recursively process directories (default: true)
- `--patterns`: File patterns to include (default: *.md,*.txt,*.py,*.js,*.ts)
- `--chunk-size`: Target chunk size in tokens (default: 750)
- `--overlap`: Chunk overlap in tokens (default: 75)

## Examples

```bash
# Ingest entire directory
/akashic:ingest my-research ./docs

# Ingest specific file patterns
/akashic:ingest my-research ./src --patterns "*.py,*.md"

# Ingest single file
/akashic:ingest my-research ./README.md

# Non-recursive directory scan
/akashic:ingest my-research ./docs --recursive false
```

## Supported File Types

| Extension | Handler | Chunking Strategy |
|-----------|---------|-------------------|
| `.md` | Markdown | By headers/sections |
| `.txt` | Plain text | By paragraphs |
| `.py` | Python | By functions/classes |
| `.js/.ts` | JavaScript | By functions/exports |
| `.json` | JSON | By top-level keys |
| `.ipynb` | Notebook | By cells |

## Processing Pipeline

1. **Scan**: Find files matching patterns
2. **Parse**: Extract content based on file type
3. **Chunk**: Split into semantic chunks with overlap
4. **Contextualize**: Add document context to chunks
5. **Index**: Store in vector, keyword, and graph stores

## Output

```json
{
  "success": true,
  "ingested_count": 150,
  "files": ["file1.md", "file2.py", "..."],
  "total_in_kb": 350
}
```

## MCP Tool

This command uses `mcp__akashic-kb__akashic_ingest` under the hood.
