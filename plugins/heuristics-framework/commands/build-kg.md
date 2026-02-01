# Build Knowledge Graph Command

Construct a knowledge graph from extracted patterns or heuristics.

## Usage

```
/heuristics-framework:build-kg <input-path> [options]
```

## Arguments

- `$1` - Path to patterns JSON or heuristics directory (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--output <path>` - Output graph file (default: knowledge-graph.json)
- `--format <json|neo4j|rdf>` - Output format (default: json)
- `--schema <path>` - Custom entity/relation schema
- `--resolve-entities` - Enable entity resolution (default: true)
- `--neo4j-uri <uri>` - Neo4j connection for direct import

## Workflow

This command delegates to the `heuristics-kg-builder` agent to:

1. **Extract** entities from patterns/heuristics
2. **Extract** relationships as (S, P, O) triples
3. **Resolve** duplicate entities
4. **Fuse** knowledge from multiple sources
5. **Export** to specified format

## Injected Skills

- `kg-construction` - Knowledge graph methodology

## Example

```bash
# Build KG from patterns
/heuristics-framework:build-kg ./patterns.json

# Export to Neo4j format
/heuristics-framework:build-kg ./heuristics/ --format neo4j

# Direct Neo4j import
/heuristics-framework:build-kg ./patterns.json --neo4j-uri bolt://localhost:7687
```

## Output Formats

### JSON (default)

```json
{
  "nodes": [
    {"@id": "entity:x", "@type": "Heuristic", "label": "..."}
  ],
  "edges": [
    {"source": "entity:x", "predicate": "APPLIES_TO", "target": "entity:y"}
  ]
}
```

### Neo4j Cypher

```cypher
CREATE (h:Heuristic {id: '...', name: '...'})
CREATE (d:Domain {id: '...', name: '...'})
CREATE (h)-[:APPLIES_TO]->(d)
```

### RDF/Turtle

```turtle
@prefix hf: <https://heuristics-framework.dev/> .
hf:early-return a hf:Heuristic ;
    hf:appliesTo hf:software-engineering .
```

## Relation Types

| Predicate | Description |
|-----------|-------------|
| DEPENDS_ON | Entity requires another |
| CONTRADICTS | Mutually exclusive |
| SPECIALIZES | More specific version |
| APPLIES_TO | Heuristic → Domain |
| VALIDATES | Evidence → Heuristic |
