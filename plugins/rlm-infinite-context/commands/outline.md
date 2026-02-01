---
name: rlm:outline
description: Generate structural outline of loaded context to navigate large documents
allowed-tools: Read, Bash
---

# View Context Outline

Generate a structural map of loaded content to help navigate large documents.

## Usage

```
/rlm:outline [options]
```

## Options

- `--context`: Specific context ID (uses active session if not specified)
- `--depth`: Maximum heading depth to include (default: 3)

## What It Detects

### Markdown Headers
```markdown
# Chapter 1
## Section 1.1
### Subsection 1.1.1
```

### Code Structures
```python
def function_name():
class ClassName:
async def async_function():
```

### Book Sections
```
Chapter 1: Introduction
Section 2.1 - Methods
Part III: Results
```

### HTML Headers
```html
<h1>Main Title</h1>
<h2>Subtitle</h2>
```

## Output

```json
{
  "context_name": "research-paper.txt",
  "total_tokens": 2500000,
  "outline_items": 47,
  "outline": [
    {"title": "Introduction", "type": "markdown", "level": 1, "chunk_id": 0},
    {"title": "Background", "type": "markdown", "level": 2, "chunk_id": 3},
    {"title": "RLMServer", "type": "code", "level": 1, "chunk_id": 15}
  ]
}
```

## Examples

```bash
# Get outline of active context
/rlm:outline

# Get detailed outline with deeper headers
/rlm:outline --depth 5

# Outline specific context
/rlm:outline --context abc123def456
```

## Using the Outline

The outline helps you:

1. **Navigate**: Jump to specific sections by chunk_id
2. **Plan searches**: Know where to look for information
3. **Understand structure**: See how the document is organized
4. **Target queries**: Reference specific sections in questions

## MCP Tool

This command uses `mcp__rlm-context__rlm_outline` under the hood.
