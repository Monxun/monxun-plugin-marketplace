---
name: rlm:query
description: Intelligently answer questions about loaded content using recursive RLM search
allowed-tools: Read, Bash
argument-validation: required
---

# Query RLM Context

Ask questions about loaded documents and get intelligent answers using recursive search.

## Usage

```
/rlm:query <question>
```

## Arguments

- `$1` - Natural language question about the loaded content

## How It Works

This command orchestrates the full RLM workflow:

1. **Query Analysis**: Extracts keywords and search strategy from question
2. **Initial Search**: Finds relevant sections across the document
3. **Recursive Exploration**: Dives deeper into promising sections
4. **Answer Synthesis**: Combines findings into a coherent answer

## Examples

```bash
# Simple factual question
/rlm:query "What is the main algorithm described in chapter 3?"

# Complex multi-part question
/rlm:query "Compare the authentication methods discussed and their security implications"

# Code understanding
/rlm:query "How does the payment processing module handle refunds?"

# Research synthesis
/rlm:query "What are the key findings regarding context window limitations?"
```

## Query Types

### Factual Queries
"What is X?" / "When did Y happen?" / "Who created Z?"
- Quick searches for specific information
- Usually resolved in 1-2 search iterations

### Aggregation Queries
"List all..." / "Find every..." / "What are the types of..."
- Searches multiple sections
- Combines results from across the document

### Comparative Queries
"Compare X and Y" / "What's the difference between..."
- Searches for both entities
- May require recursive searches in multiple branches

### Analytical Queries
"Why does X happen?" / "How does Y work?"
- Deep recursive searches
- May need to trace through multiple sections

## Output Format

Answers include:
- **Answer**: Synthesized response to your question
- **Sources**: Chunk IDs where information was found
- **Confidence**: How certain the answer is
- **Search Path**: The recursive search journey taken

## Best Practices

1. **Be specific**: "How does the auth module validate JWT tokens?" is better than "How does auth work?"

2. **Reference document structure**: "In chapter 5..." or "In the implementation section..."

3. **Break down complex questions**: Multiple focused queries often work better than one broad question

4. **Check sources**: Review the chunks cited to verify answers

## Comparison with Native Context

| Feature | Native Context | RLM Query |
|---------|----------------|-----------|
| Max tokens | ~200K | Unlimited |
| Recall | Degrades with size | Consistent |
| Cost | Linear with size | Efficient |
| Speed | Fast | Slightly slower |

## MCP Tools Used

This command orchestrates multiple tools:
- `mcp__rlm-context__rlm_search`
- `mcp__rlm-context__rlm_search_recursive`
- `mcp__rlm-context__rlm_get_chunk`
