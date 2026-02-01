# Cypher Query Patterns for Knowledge Graphs

## Basic Patterns

### Node Matching

```cypher
// Match by label
MATCH (e:Entity)
RETURN e

// Match by property
MATCH (e:Entity {name: 'React'})
RETURN e

// Match with WHERE
MATCH (e:Entity)
WHERE e.type = 'Technology' AND e.created_year > 2020
RETURN e
```

### Relationship Matching

```cypher
// Direct relationship
MATCH (a:Entity)-[:USES]->(b:Entity)
RETURN a, b

// Any relationship
MATCH (a:Entity)-[r]->(b:Entity)
RETURN a, type(r), b

// Multiple relationship types
MATCH (a)-[:USES|IMPLEMENTS]->(b)
RETURN a, b
```

### Variable-Length Paths

```cypher
// 1 to 3 hops
MATCH path = (a:Entity {name: 'React'})-[*1..3]->(b)
RETURN path

// Specific relationship types
MATCH path = (a)-[:USES|DEPENDS_ON*1..4]->(b)
RETURN path

// All paths (expensive)
MATCH path = (a)-[*]->(b)
WHERE length(path) <= 5
RETURN path
```

## Advanced Patterns

### Shortest Path

```cypher
// Single shortest path
MATCH path = shortestPath(
  (a:Entity {name: 'React'})-[*]-(b:Entity {name: 'Redux'})
)
RETURN path, length(path) as hops

// All shortest paths
MATCH path = allShortestPaths(
  (a:Entity {name: 'React'})-[*]-(b:Entity {name: 'Node.js'})
)
RETURN path
```

### Aggregation

```cypher
// Count relationships
MATCH (e:Entity)-[r]->()
RETURN e.name, count(r) as relationship_count
ORDER BY relationship_count DESC
LIMIT 10

// Group by type
MATCH (e:Entity)-[r]->(t)
RETURN type(r), count(*) as count
ORDER BY count DESC

// Average path length
MATCH path = (a:Entity)-[*]-(b:Entity)
WHERE a.name = 'React'
RETURN avg(length(path)) as avg_path_length
```

### Pattern Comprehension

```cypher
// Collect related entities
MATCH (e:Entity {name: 'React'})
RETURN e, [(e)-[:USES]->(lib) | lib.name] as libraries

// Nested patterns
MATCH (tech:Entity {type: 'Technology'})
RETURN tech.name,
       [(tech)-[:USES]->(lib) | lib.name] as libraries,
       [(tech)<-[:USES]-(user) | user.name] as used_by
```

### Subqueries

```cypher
// CALL subquery
MATCH (e:Entity {type: 'Technology'})
CALL {
  WITH e
  MATCH (e)-[:USES*1..2]->(dep)
  RETURN collect(dep.name) as dependencies
}
RETURN e.name, dependencies

// EXISTS subquery
MATCH (e:Entity)
WHERE EXISTS {
  MATCH (e)-[:IMPLEMENTS]->(:Entity {type: 'Pattern'})
}
RETURN e.name
```

## Graph Algorithms

### PageRank

```cypher
// Using GDS library
CALL gds.pageRank.stream('entityGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name as name, score
ORDER BY score DESC
LIMIT 10
```

### Community Detection

```cypher
// Louvain community detection
CALL gds.louvain.stream('entityGraph')
YIELD nodeId, communityId
RETURN communityId, collect(gds.util.asNode(nodeId).name) as members
ORDER BY size(members) DESC
```

### Node Similarity

```cypher
// Jaccard similarity
CALL gds.nodeSimilarity.stream('entityGraph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name as entity1,
       gds.util.asNode(node2).name as entity2,
       similarity
ORDER BY similarity DESC
LIMIT 20
```

## Knowledge Graph Specific

### Entity Resolution

```cypher
// Find potential duplicates
MATCH (e1:Entity), (e2:Entity)
WHERE e1 <> e2
  AND e1.name =~ ('(?i)' + e2.name)
RETURN e1.name, e2.name, e1.id, e2.id
```

### Transitive Closure

```cypher
// All ancestors in hierarchy
MATCH (e:Entity {name: 'Component'})-[:IS_A*]->(ancestor)
RETURN ancestor.name as ancestor

// All descendants
MATCH (e:Entity {name: 'Pattern'})<-[:IS_A*]-(descendant)
RETURN descendant.name as descendant
```

### Temporal Queries

```cypher
// Evolution over time
MATCH (v1:Entity)-[:VERSION_OF]->(v2:Entity)
WHERE v1.release_date > v2.release_date
RETURN v2.name + ' -> ' + v1.name as evolution,
       v1.release_date - v2.release_date as days_between
ORDER BY v1.release_date
```

## Performance Tips

### Indexing

```cypher
// Create index for faster lookups
CREATE INDEX entity_name FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type FOR (e:Entity) ON (e.type);

// Composite index
CREATE INDEX entity_composite FOR (e:Entity) ON (e.type, e.name);
```

### Query Optimization

```cypher
// Use PROFILE to analyze
PROFILE
MATCH (a:Entity {name: 'React'})-[:USES*1..3]->(b)
RETURN b.name

// Limit early
MATCH (e:Entity)
WITH e
LIMIT 100
MATCH (e)-[:USES]->(lib)
RETURN e, lib
```

### Batch Operations

```cypher
// Batch create with UNWIND
UNWIND $entities as entity
MERGE (e:Entity {name: entity.name})
SET e.type = entity.type

// Batch relationship creation
UNWIND $relations as rel
MATCH (a:Entity {name: rel.from})
MATCH (b:Entity {name: rel.to})
MERGE (a)-[:USES]->(b)
```
