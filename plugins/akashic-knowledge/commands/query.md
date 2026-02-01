---
name: akashic:query
description: Query an Akashic knowledge base using hybrid semantic and keyword search
---

# Query Knowledge Base

Search a knowledge base using state-of-the-art hybrid retrieval.

## Usage

```
/akashic:query <kb-name> "<query>" [options]
```

## Parameters

- **kb-name**: Knowledge base to query
- **query**: Natural language search query (use quotes for multi-word)

## Options

- `--top-k`: Number of results to return (default: 10)
- `--search-type`: Search strategy - `hybrid`, `semantic`, or `keyword` (default: hybrid)
- `--rerank`: Apply ColBERT reranking (default: true)

## Examples

```bash
# Basic hybrid search
/akashic:query my-research "What are the best practices for API design?"

# Semantic-only search
/akashic:query my-research "authentication patterns" --search-type semantic

# Get more results
/akashic:query my-research "error handling" --top-k 20

# Keyword-only for exact matches
/akashic:query my-research "UserService" --search-type keyword
```

## Search Strategies

### Hybrid (Default)
Combines semantic and keyword search:
- 80% semantic (meaning-based)
- 20% keyword (exact match)
- Reciprocal Rank Fusion

### Semantic
Pure vector similarity:
- Best for conceptual queries
- Handles synonyms and paraphrasing

### Keyword
Traditional BM25:
- Best for exact terms
- Code identifiers
- Technical names

## Output Format

```json
{
  "query": "your query",
  "search_type": "hybrid",
  "result_count": 10,
  "results": [
    {
      "id": "chunk_123",
      "content": "Relevant text...",
      "source": "/path/to/document.md",
      "score": 0.95
    }
  ]
}
```

## Query Tips

1. **Be specific**: "React authentication with JWT" > "authentication"
2. **Use natural language**: Queries work best as questions
3. **Try different strategies**: Switch between hybrid/semantic/keyword

## MCP Tool

This command uses `mcp__akashic-kb__akashic_query` under the hood.
