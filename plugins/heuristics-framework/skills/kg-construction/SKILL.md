---
name: kg-construction
description: |
  Knowledge graph construction using LLM-empowered extraction pipelines.
  Use when: building entity-relationship graphs, entity extraction (NER),
  relation extraction, entity resolution, knowledge fusion, GraphRAG.
  Supports: schema-based and schema-free approaches.
---

# Knowledge Graph Construction Skill

## Quick Start

Build structured knowledge graphs from unstructured text using LLM-powered extraction.

### Core Pipeline

```
1. EXTRACT: Identify entities (NER)
2. RELATE: Extract relationships as triples
3. RESOLVE: Deduplicate and merge entities
4. FUSE: Integrate across sources
5. STORE: Persist to graph database
```

## Construction Approaches

### Schema-Based (Top-Down)

```
Predefined ontology → LLM extraction → Structured graph

Pros: High precision, interpretable
Cons: Limited flexibility
Use: Enterprise KG, domain-specific apps
```

### Schema-Free (Bottom-Up)

```
Raw data → LLM extraction → Dynamic schema induction

Pros: Flexible, discovers new patterns
Cons: May need cleanup
Use: Exploratory analysis, new domains
```

## Core Workflow

### Step 1: Entity Extraction

```python
ENTITY_TYPES = [
    "Heuristic",   # Documented rule
    "Domain",      # Area of applicability
    "Concept",     # Abstract principle
    "Pattern",     # Recurring structure
    "Evidence",    # Supporting data
]
```

### Step 2: Relation Extraction

Common predicates:
| Predicate | Description |
|-----------|-------------|
| DEPENDS_ON | Requires another entity |
| CONTRADICTS | Mutually exclusive |
| SPECIALIZES | More specific version |
| APPLIES_TO | Heuristic → Domain |
| VALIDATES | Evidence → Heuristic |

### Step 3: Entity Resolution

```
Group by normalized name
↓
Fuzzy match (>0.9 similarity)
↓
Alias detection
↓
Merge with conflict resolution
```

### Step 4: Knowledge Fusion

Trust ordering for conflicts:
1. Primary sources (code, official docs)
2. Secondary sources (tutorials, blogs)
3. Derived sources (LLM extractions)

## Output Format

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

## Quality Metrics

| Metric | Target |
|--------|--------|
| Entity precision | >0.85 |
| Relation precision | >0.80 |
| Resolution accuracy | >0.90 |
| Graph connectivity | >0.70 |

## Additional Resources

- For entity extraction: [entity-extraction.md](references/entity-extraction.md)
- For Neo4j integration: [neo4j-integration.md](references/neo4j-integration.md)
- For GraphRAG patterns: [graphrag-patterns.md](references/graphrag-patterns.md)

## Research Foundation

Based on: "LLM-empowered Knowledge Graph Construction Survey"
- Paper: arxiv.org/abs/2510.20345
- Tools: FalkorDB, LangChain Graph Transformer, Neo4j Builder
