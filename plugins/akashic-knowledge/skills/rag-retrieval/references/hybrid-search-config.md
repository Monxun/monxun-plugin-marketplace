# Hybrid Search Configuration

## Search Strategy Tuning

### Weight Configuration

```yaml
hybrid_search:
  semantic_weight: 0.8    # Vector similarity weight
  keyword_weight: 0.2     # BM25 weight
  rrf_k: 60               # RRF constant (higher = more uniform)
```

### When to Adjust Weights

| Scenario | Semantic | Keyword | Notes |
|----------|----------|---------|-------|
| General queries | 0.8 | 0.2 | Default |
| Technical docs | 0.6 | 0.4 | More exact matches |
| Code search | 0.4 | 0.6 | Identifiers matter |
| Conceptual | 0.9 | 0.1 | Meaning over words |

## Vector Search Configuration

### Qdrant Settings

```python
search_params = {
    "hnsw_ef": 128,           # Search accuracy (higher = better, slower)
    "exact": False,           # Use approximate search
    "quantization": {
        "rescore": True,      # Rescore after quantized search
        "oversampling": 2.0   # Candidate oversampling
    }
}
```

### Contextual Embeddings

Prepend context to improve retrieval:

```python
def create_contextual_embedding(chunk: str, metadata: dict) -> list[float]:
    """
    Context template for embedding:
    Document: {filename}
    Section: {section_header}
    Type: {document_type}

    {chunk_content}
    """
    context = f"""Document: {metadata['filename']}
Section: {metadata.get('section', 'Main')}
Type: {metadata.get('doc_type', 'text')}

{chunk}"""

    return embedding_model.encode(context)
```

## BM25 Configuration

### Elasticsearch Settings

```json
{
  "settings": {
    "index": {
      "similarity": {
        "custom_bm25": {
          "type": "BM25",
          "k1": 1.2,
          "b": 0.75
        }
      }
    }
  }
}
```

### Parameter Tuning

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| k1 | 1.2 | 0.5-2.0 | Term frequency saturation |
| b | 0.75 | 0.0-1.0 | Length normalization |

- **Higher k1**: More weight to repeated terms
- **Higher b**: More penalty for longer documents

## Reciprocal Rank Fusion

### Algorithm

```python
def reciprocal_rank_fusion(
    rankings: list[list[str]],
    k: int = 60
) -> dict[str, float]:
    """
    Combine multiple rankings into unified score.

    RRF(d) = Σ 1/(k + rank_i(d))
    """
    scores = defaultdict(float)

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1.0 / (k + rank)

    return dict(sorted(scores.items(), key=lambda x: -x[1]))
```

### K Parameter Selection

| k Value | Behavior |
|---------|----------|
| 20 | Strongly favor top ranks |
| 60 | Balanced (default) |
| 100 | More uniform weighting |

## Query Expansion

### Synonym Expansion

```python
def expand_query(query: str) -> list[str]:
    """
    Generate query variations:
    1. Original query
    2. Synonym replacements
    3. Related terms
    """
    variations = [query]

    # Add synonym variations
    for word in tokenize(query):
        if word in SYNONYM_MAP:
            for synonym in SYNONYM_MAP[word]:
                variations.append(query.replace(word, synonym))

    return variations[:5]  # Limit variations
```

### Hypothetical Document Embeddings (HyDE)

```python
def hyde_expansion(query: str) -> str:
    """
    Generate hypothetical answer document for better retrieval.
    """
    prompt = f"""Write a short paragraph that would answer: {query}
    Be specific and include relevant technical details."""

    hypothetical = llm.generate(prompt)
    return hypothetical
```

## Performance Optimization

### Caching Strategy

```python
cache_config = {
    "query_cache_ttl": 300,      # 5 minutes
    "embedding_cache_size": 1000, # Recent embeddings
    "result_cache_ttl": 60        # 1 minute
}
```

### Batch Processing

```python
async def batch_search(queries: list[str], kb_name: str) -> list[Results]:
    """
    Process multiple queries efficiently:
    1. Batch embed queries
    2. Parallel search execution
    3. Aggregate results
    """
    # Batch embed
    embeddings = embedding_model.encode_batch(queries)

    # Parallel search
    tasks = [
        search_single(emb, kb_name)
        for emb in embeddings
    ]
    results = await asyncio.gather(*tasks)

    return results
```
