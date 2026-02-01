# Akashic Knowledge Architecture

## System Overview

The Akashic Knowledge plugin implements a multi-agent research and knowledge management system with the following layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Interface                     │
│  Commands: create-kb, ingest, query, discover, export, sync │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestration Layer                 │
│  orchestrator → researcher, extractor, synthesizer, etc.    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       MCP Server Layer                       │
│  Tools: akashic_create_kb, akashic_ingest, akashic_query... │
│  Resources: akashic://kb/{name}/status, /catalog            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Storage Infrastructure                     │
│  Qdrant (vectors) | Neo4j (graph) | ES (BM25) | Redis       │
└─────────────────────────────────────────────────────────────┘
```

## Agent Architecture

### Agent Hierarchy

```
orchestrator (coordinator)
├── researcher (parallel)
│   ├── Web research
│   └── Document analysis
├── extractor
│   ├── Entity extraction
│   ├── Relation extraction
│   └── Pattern identification
├── indexer
│   ├── Vector embedding
│   ├── Graph construction
│   └── BM25 indexing
├── synthesizer (AutoHD)
│   ├── Heuristic proposal
│   ├── Evaluation
│   └── Evolution
├── validator (POPPER)
│   ├── Experiment design
│   ├── Statistical testing
│   └── Evidence accumulation
└── retriever
    ├── Hybrid search
    ├── Reranking
    └── Graph augmentation
```

### Agent Capabilities

| Agent | Tools | Model | Purpose |
|-------|-------|-------|---------|
| orchestrator | Task, Read, Bash, Grep, Glob, WebSearch | sonnet | Workflow coordination |
| researcher | Read, Grep, Glob, WebSearch, WebFetch | sonnet | Information gathering |
| extractor | Read, Grep, Glob, Bash | sonnet | Pattern extraction |
| synthesizer | Read, Write, Edit, Bash, Grep, Glob | sonnet | Heuristic generation |
| validator | Read, Bash, Grep, Glob | sonnet | Statistical validation |
| indexer | Read, Write, Bash, Grep, Glob | sonnet | Multi-store indexing |
| retriever | Read, Grep, Glob, Bash | sonnet | Query execution |

## RAG Architecture

### Retrieval Pipeline

```
Query
  ↓
Query Analysis & Decomposition
  ↓
┌─────────────────────┬─────────────────────┐
│  Semantic Search    │   Keyword Search    │
│  (Qdrant)           │   (Elasticsearch)   │
│  Weight: 0.8        │   Weight: 0.2       │
└─────────────────────┴─────────────────────┘
            ↓
  Reciprocal Rank Fusion (k=60)
            ↓
  ColBERT-style Reranking
            ↓
  Graph Augmentation (Neo4j)
            ↓
  Top-K Results
```

### Contextual Embeddings

Documents are embedded with context prefix:

```
Document: {filename}
Section: {section_header}
Type: {document_type}

{chunk_content}
```

This reduces retrieval failures by ~35% compared to content-only embeddings.

### Hybrid Search Formula

```
RRF(d) = Σ 1/(k + rank_i(d))

where:
- k = 60 (smoothing constant)
- rank_i(d) = rank of document d in ranking i
```

## Heuristics Framework

### AutoHD Pipeline

```
Patterns from KB
       ↓
Initial Population (diverse proposals)
       ↓
┌─────────────────────────────────────┐
│        Evolution Loop               │
│  ┌─────────────────────────────┐   │
│  │ Evaluation (fitness scoring)│   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │ Selection (tournament)      │   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │ Reproduction (crossover)    │   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │ Mutation (parameter tuning) │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
       ↓ (iterate until convergence)
Top Heuristic Candidates
```

### POPPER Validation

```
Heuristic Candidate
       ↓
Experiment Design (falsification)
       ↓
Sequential Testing
       ↓
E-Value Calculation: E = Π e_i
       ↓
Decision:
- E > 20: Accept (strong evidence)
- α > 0.10: Reject (Type-I error too high)
- Otherwise: Continue testing
```

## Storage Architecture

### Qdrant (Vector Store)

```yaml
Collection: akashic_{kb_name}
Vectors:
  size: 1536  # OpenAI/Claude embedding dimension
  distance: Cosine
Payload:
  - content: string
  - source: string
  - section: string
  - doc_type: string
```

### Neo4j (Graph Store)

```cypher
// Node types
(:Entity {name, type, description})
(:Document {path, title, created_at})
(:Chunk {content, position})
(:Heuristic {name, domain, version})

// Relationship types
(Entity)-[:IS_A|USES|CONTAINS|RELATED_TO]->(Entity)
(Document)-[:CONTAINS]->(Chunk)
(Chunk)-[:MENTIONS]->(Entity)
(Heuristic)-[:DERIVED_FROM]->(Document)
```

### Elasticsearch (Keyword Store)

```json
{
  "mappings": {
    "properties": {
      "content": {"type": "text", "analyzer": "standard"},
      "source": {"type": "keyword"},
      "section": {"type": "keyword"},
      "doc_type": {"type": "keyword"},
      "created_at": {"type": "date"}
    }
  },
  "settings": {
    "similarity": {
      "default": {"type": "BM25", "k1": 1.2, "b": 0.75}
    }
  }
}
```

## MCP Server Architecture

### Tool Registration

```python
Tools:
- akashic_create_kb(name, scope, description)
- akashic_ingest(kb_name, source, recursive, file_patterns)
- akashic_query(kb_name, query, top_k, search_type, rerank)
- akashic_discover(kb_name, domain, iterations, validate)
- akashic_graph_traverse(kb_name, start_entity, relation_types, max_hops)
- akashic_export(kb_name, output_path, format, include_heuristics)
- akashic_status(kb_name)
```

### Resource URIs

```
akashic://kb/{name}/status   → KB health and stats
akashic://kb/{name}/catalog  → Document catalog
akashic://heuristics/{domain} → Domain heuristics
```

## Hook Architecture

| Event | Hook | Purpose |
|-------|------|---------|
| PreToolUse (ingest) | validate-corpus.py | Validate before ingestion |
| PostToolUse (create_kb) | index-on-create.py | Setup after KB creation |
| SessionEnd | persist-session.py | Save session state |
| PostToolUse (discover) | validate-heuristics.py | Check heuristic quality |

## Data Flow

### Ingestion Flow

```
Source Directory
       ↓
File Discovery (Glob patterns)
       ↓
Document Parsing (type-specific)
       ↓
Semantic Chunking (750 tokens, 75 overlap)
       ↓
Contextual Enhancement
       ↓
┌─────────────────────────────────────┐
│         Parallel Indexing           │
├─────────────┬───────────┬───────────┤
│   Qdrant    │   Neo4j   │    ES     │
│  (vectors)  │  (graph)  │  (BM25)   │
└─────────────┴───────────┴───────────┘
```

### Discovery Flow

```
Knowledge Base
       ↓
Pattern Extraction (extractor agent)
       ↓
Heuristic Proposal (synthesizer agent)
       ↓
Evolution Loop (3-10 iterations)
       ↓
POPPER Validation (validator agent)
       ↓
Documentation Generation
       ↓
Validated Heuristics + Research Documents
```

## Performance Considerations

### Latency Budget

| Operation | Target | Components |
|-----------|--------|------------|
| Simple Query | <500ms | Embed + Search + Rerank |
| Complex Query | <2s | Decompose + Multi-search + Fuse |
| Ingestion | <1s/doc | Parse + Chunk + Index |
| Discovery | <5min | Extract + Evolve + Validate |

### Scaling Considerations

1. **Horizontal**: Add Qdrant/ES shards for larger corpora
2. **Vertical**: Increase Docker resource limits
3. **Caching**: Redis for query/embedding caching
4. **Batching**: Process documents in batches of 100

## Security Model

1. **Local Storage**: All data in `~/.akashic/`
2. **Docker Networks**: Isolated `akashic-network`
3. **No External APIs**: Embeddings via local/Claude models
4. **Credential Handling**: Environment variables only
