# RLM Performance Optimization

## Chunk Size Tuning

### Default Settings
```python
CHUNK_SIZE = 4000  # characters (~1000 tokens)
OVERLAP = 200      # characters (~50 tokens)
```

### Optimization by Content Type

| Content Type | Chunk Size | Overlap | Rationale |
|--------------|------------|---------|-----------|
| Prose/Articles | 4000 | 200 | Natural paragraph boundaries |
| Code | 2000 | 100 | Function/class boundaries |
| JSON/XML | 3000 | 150 | Structure boundaries |
| Logs | 5000 | 50 | Line-based, less overlap needed |
| Mixed | 4000 | 200 | Balanced default |

### When to Adjust

**Increase chunk size when:**
- Content is highly connected
- Searches need more context
- Memory is not a concern

**Decrease chunk size when:**
- Content is highly segmented
- Precision is more important than recall
- Memory is limited

## Query Optimization

### Search Strategy Selection

```python
# Decision tree for search type
if has_regex_chars(query):
    search_type = "regex"
elif is_section_reference(query):
    search_type = "section"  
else:
    search_type = "keyword"
```

### Keyword Query Tips

1. **Use specific terms**: "OAuth2 token refresh" > "authentication"
2. **Include domain vocabulary**: Use terms from the document
3. **Avoid stop words**: Skip "the", "and", "is"

### Regex Query Tips

1. **Anchor when possible**: `^def` is faster than just `def`
2. **Use character classes**: `[a-z]+` > `\w+` for lowercase only
3. **Avoid backtracking**: `[^"]*` > `.*?` for quoted strings

## Recursive Search Optimization

### Depth Strategy

```
Depth 0: Broad search, identify hot spots
Depth 1: Narrow to promising chunks
Depth 2: Extract specific details
Depth 3+: Rare, for complex queries only
```

### Chunk Selection

**Good selection:**
```python
# Take top 3-5 chunks by relevance
selected_chunks = [r.chunk_id for r in results[:5] if r.relevance > 0.3]
```

**Avoid:**
```python
# Too many chunks = expensive
selected_chunks = [r.chunk_id for r in results]  # Could be 50+ chunks!
```

### Early Termination

Stop recursing when:
- Confidence is high enough
- Results are getting repetitive
- Depth exceeds 3-4 levels

## Memory Management

### Context Lifecycle

```python
# Load only what you need
load_context(document)

# Search and extract
results = search(query)

# Clear when done
clear_context(context_id)
```

### Large Document Strategies

For 100MB+ documents:

1. **Selective loading**: Load sections incrementally
2. **Aggressive clearing**: Clear after each query session
3. **Index persistence**: Keep indexes, reload content as needed

## Token Efficiency

### Cost Calculation

```python
# Approximate cost per search
tokens_per_search = num_results * avg_chunk_size / 4
cost_per_1M_tokens = 0.003  # Varies by model
search_cost = tokens_per_search * cost_per_1M_tokens / 1_000_000
```

### Comparison: RLM vs Full Context

| Scenario | Full Context | RLM | Savings |
|----------|--------------|-----|---------|
| 1M tokens, 1 query | 1M | 20K | 98% |
| 1M tokens, 10 queries | 10M | 200K | 98% |
| 10M tokens, 1 query | 10M | 30K | 99.7% |

## Benchmarking

### Measuring Performance

```python
import time

# Load time
start = time.time()
load_context(content)
load_time = time.time() - start

# Search time
start = time.time()
results = search(query)
search_time = time.time() - start

# Tokens processed
tokens = sum(len(r.content) // 4 for r in results)
```

### Performance Targets

| Operation | Target | Acceptable |
|-----------|--------|------------|
| Load (per MB) | <100ms | <500ms |
| Search | <100ms | <500ms |
| Recursive | <200ms | <1s |

## Scaling Considerations

### Single Document Limits

| Metric | Recommended | Maximum |
|--------|-------------|---------|
| Document size | <100MB | 1GB |
| Chunks | <10,000 | 100,000 |
| Tokens | <25M | 250M |

### Multi-Document Scenarios

For document collections:
1. Load documents separately
2. Search across all contexts
3. Merge and rank results
