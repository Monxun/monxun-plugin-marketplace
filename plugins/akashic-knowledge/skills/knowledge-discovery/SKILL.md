---
name: knowledge-discovery
description: |
  Research pattern discovery and knowledge synthesis from corpus.
  Use when: discovering patterns in documents, synthesizing research findings,
  building knowledge bases from corpora, "discover patterns", "research corpus",
  "analyze documents", "find patterns", "knowledge synthesis".
triggers:
  - discover patterns
  - research corpus
  - analyze documents
  - find patterns
  - knowledge synthesis
  - build knowledge base
---

# Knowledge Discovery Skill

Transform document corpora into structured knowledge through pattern discovery, entity extraction, and research synthesis.

## Quick Start

```bash
# Create knowledge base and discover patterns
/akashic:create-kb my-research project
/akashic:ingest ./docs --recursive
/akashic:discover my-research --domain "software-architecture"
```

## Core Capabilities

### 1. Corpus Ingestion
Ingest documents from directories, files, or URLs:
- Automatic file type detection
- Semantic chunking with context preservation
- Multi-store indexing (vector, graph, keyword)

### 2. Pattern Discovery
Extract patterns and relationships:
- Entity recognition (concepts, technologies, components)
- Relation extraction (hierarchical, associative, temporal)
- Pattern frequency analysis

### 3. Knowledge Synthesis
Generate structured knowledge outputs:
- Research summaries with citations
- Entity-relationship graphs
- Heuristic functions for pattern matching

## Workflow

```
Corpus → Ingestion → Chunking → Indexing → Extraction → Synthesis
                                    ↓           ↓           ↓
                               Vector DB    Graph DB    Heuristics
```

## Usage Patterns

### Pattern Discovery
```
"Discover patterns in the authentication module"
"Find common design patterns in this codebase"
"Identify recurring themes in documentation"
```

### Research Synthesis
```
"Synthesize research on microservices best practices"
"Create knowledge summary from these papers"
"Build pattern library from code examples"
```

### Knowledge Base Creation
```
"Create a project knowledge base from ./src"
"Build searchable index of documentation"
"Index codebase for semantic search"
```

## Output Formats

| Format | Use Case |
|--------|----------|
| Markdown | Research reports, summaries |
| JSON | Structured data, API responses |
| JSON-LD | Semantic web, linked data |
| Cypher | Graph database queries |

## Quality Metrics

- **Extraction Precision**: >85% accurate entities
- **Pattern Coverage**: >90% of significant patterns
- **Synthesis Quality**: Coherent, well-cited outputs

## References

For detailed implementation:
- @references/extraction-patterns.md - Entity and relation extraction
- @references/synthesis-strategies.md - Knowledge synthesis approaches
- @references/indexing-config.md - Multi-store indexing configuration
