---
name: rag-retrieval
description: |
  Agentic RAG queries with hybrid search and intelligent retrieval.
  Use when: querying knowledge bases, semantic search, finding information,
  "search knowledge base", "find in docs", "query kb", "retrieve information",
  "hybrid search", "semantic search".
triggers:
  - search knowledge base
  - find in docs
  - query kb
  - retrieve information
  - hybrid search
  - semantic search
  - ask knowledge base
---

# RAG Retrieval Skill

Execute intelligent queries against knowledge bases using state-of-the-art hybrid retrieval with semantic search, keyword matching, and graph augmentation.

## Quick Start

```bash
# Query existing knowledge base
/akashic:query my-research "What are the best practices for API design?"

# Search with specific options
/akashic:query my-research "authentication patterns" --search-type hybrid --top-k 10
```

## Retrieval Strategies

### 1. Hybrid Search (Default)
Combines semantic and keyword search with Reciprocal Rank Fusion:
- **80% Semantic**: Contextual embeddings for meaning
- **20% Keyword**: BM25 for exact matches
- **RRF Fusion**: Optimal rank combination

### 2. Semantic-Only
Pure vector similarity search:
- Best for conceptual queries
- Handles synonyms and paraphrasing
- Lower latency

### 3. Keyword-Only
Traditional BM25 search:
- Best for exact term matching
- Technical identifiers
- Code symbols

## Query Decomposition

Complex queries are automatically decomposed:

```
Input: "How do microservices handle authentication and what are common pitfalls?"

Decomposed:
1. "How do microservices handle authentication?"
2. "What authentication patterns are used in microservices?"
3. "What are common pitfalls in microservice authentication?"
```

## Reranking Pipeline

```
Initial Results (top-100)
         ↓
  ColBERT Reranking
         ↓
  Graph Augmentation
         ↓
  Final Results (top-k)
```

### ColBERT Reranking
Late interaction scoring for +2-3% precision:
- Token-level similarity matching
- MaxSim aggregation
- Efficient GPU acceleration

### Graph Augmentation
Multi-hop entity expansion:
- Identify entities in top results
- Traverse knowledge graph
- Add related documents

## Usage Examples

### Simple Query
```
"Find information about caching strategies"
```

### Comparative Query
```
"Compare Redis and Memcached for session storage"
```

### Multi-hop Query
```
"What papers cite the work that introduced transformer attention?"
```

### Code-focused Query
```
"Find examples of dependency injection in Python"
```

## Output Format

Results include:
- **Content**: Relevant text snippets
- **Source**: Document path and section
- **Score**: Relevance score (0-1)
- **Context**: Related entities from graph

## Performance Targets

| Metric | Target | Description |
|--------|--------|-------------|
| Pass@10 | >95% | Answer in top 10 results |
| MRR | >0.8 | Mean Reciprocal Rank |
| Latency | <500ms | Query response time |

## References

For advanced configuration:
- @references/hybrid-search-config.md - Search strategy tuning
- @references/reranking-models.md - Reranking options
- @references/query-expansion.md - Query enhancement techniques
