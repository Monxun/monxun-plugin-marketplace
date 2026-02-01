---
name: graph-reasoning
description: |
  Knowledge graph traversal and multi-hop reasoning.
  Use when: traversing knowledge graphs, finding relationships, multi-hop queries,
  "graph query", "find connections", "relationship path", "entity links",
  "knowledge graph", "graph traversal".
triggers:
  - graph query
  - find connections
  - relationship path
  - entity links
  - knowledge graph
  - graph traversal
  - multi-hop reasoning
---

# Graph Reasoning Skill

Execute multi-hop queries and relationship traversal on knowledge graphs for complex reasoning tasks.

## Quick Start

```bash
# Find connections between entities
/akashic:graph my-research --start "React" --relation "USES" --hops 3

# Discover relationship paths
/akashic:graph my-research --path "React" "Redux" --max-hops 4
```

## Graph Structure

### Node Types
| Type | Description | Properties |
|------|-------------|------------|
| Entity | Concepts, technologies | name, type, description |
| Document | Source documents | path, title, date |
| Chunk | Document sections | content, position |
| Heuristic | Generated rules | name, domain, confidence |

### Edge Types
| Type | Description | Direction |
|------|-------------|-----------|
| IS_A | Type hierarchy | child → parent |
| USES | Dependencies | user → used |
| CONTAINS | Containment | container → contained |
| RELATED_TO | Association | bidirectional |
| MENTIONED_IN | Document reference | entity → document |

## Query Patterns

### 1. Neighborhood Exploration
Find all entities connected to a starting point:

```cypher
MATCH (start:Entity {name: $entity})-[r*1..2]-(connected)
RETURN start, r, connected
```

### 2. Path Finding
Find paths between two entities:

```cypher
MATCH path = shortestPath(
  (a:Entity {name: $start})-[*..5]-(b:Entity {name: $end})
)
RETURN path
```

### 3. Pattern Matching
Find entities matching a pattern:

```cypher
MATCH (tech:Entity {type: 'Technology'})
  -[:USES]->(lib:Entity {type: 'Library'})
  -[:IMPLEMENTS]->(pattern:Entity {type: 'Pattern'})
RETURN tech, lib, pattern
```

### 4. Aggregation Queries
Count relationships and compute statistics:

```cypher
MATCH (e:Entity)-[r]->()
RETURN e.name, type(r), count(*) as count
ORDER BY count DESC
```

## Multi-Hop Reasoning

### Traversal Strategy

```
Start Entity
     ↓
  [Hop 1] Direct relationships
     ↓
  [Hop 2] Secondary connections
     ↓
  [Hop 3] Tertiary links
     ↓
  Result aggregation
```

### Hop Configuration

| Hops | Use Case | Latency |
|------|----------|---------|
| 1 | Direct relationships | <50ms |
| 2 | Extended context | <100ms |
| 3 | Broad exploration | <200ms |
| 4+ | Deep reasoning | <500ms |

### Decay Factor

Apply relevance decay with distance:

```python
def calculate_relevance(path_length: int, base_score: float) -> float:
    """
    Relevance decays exponentially with path length.
    decay_factor = 0.7 per hop
    """
    return base_score * (0.7 ** path_length)
```

## Output Format

### Traversal Results
```json
{
  "start": "React",
  "traversal_depth": 3,
  "nodes_visited": 45,
  "paths": [
    {
      "path": ["React", "USES", "Babel", "COMPILES", "JavaScript"],
      "length": 2,
      "relevance": 0.49
    }
  ],
  "entities": [
    {"name": "Babel", "type": "Tool", "connections": 12}
  ]
}
```

### Path Results
```json
{
  "from": "React",
  "to": "Redux",
  "paths_found": 3,
  "shortest_path": {
    "length": 2,
    "path": ["React", "USES", "react-redux", "USES", "Redux"]
  }
}
```

## Integration with RAG

Graph reasoning enhances RAG retrieval:

1. **Entity Identification**: Extract entities from query
2. **Graph Expansion**: Find related entities via traversal
3. **Document Retrieval**: Get documents mentioning related entities
4. **Result Fusion**: Combine with vector search results

## References

For advanced patterns:
- @references/cypher-patterns.md - Cypher query examples
- @references/reasoning-algorithms.md - Graph algorithms
- @references/optimization.md - Query optimization
