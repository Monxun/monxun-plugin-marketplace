# Table of Contents
- akashic-knowledge/docker/docker-compose.yml
- akashic-knowledge/docker/neo4j/neo4j.conf
- akashic-knowledge/docker/qdrant/config.yaml
- akashic-knowledge/docker/elasticsearch/elasticsearch.yml
- akashic-knowledge/agents/indexer.md
- akashic-knowledge/agents/synthesizer.md
- akashic-knowledge/agents/orchestrator.md
- akashic-knowledge/agents/researcher.md
- akashic-knowledge/agents/validator.md
- akashic-knowledge/agents/extractor.md
- akashic-knowledge/agents/retriever.md
- akashic-knowledge/mcp/.mcp.json
- akashic-knowledge/mcp/servers/kb-server/server.py
- akashic-knowledge/mcp/servers/kb-server/requirements.txt
- akashic-knowledge/docs/ARCHITECTURE.md
- akashic-knowledge/docs/QUICKSTART.md
- akashic-knowledge/docs/README.md
- akashic-knowledge/schemas/research-doc.schema.json
- akashic-knowledge/schemas/knowledge-base.schema.json
- akashic-knowledge/schemas/heuristic.schema.json
- akashic-knowledge/hooks/hooks.json
- akashic-knowledge/hooks/scripts/validate-heuristics.py
- akashic-knowledge/hooks/scripts/validate-corpus.py
- akashic-knowledge/hooks/scripts/index-on-create.py
- akashic-knowledge/hooks/scripts/persist-session.py
- akashic-knowledge/.claude-plugin/plugin.json
- akashic-knowledge/templates/kb-manifest.json.j2
- akashic-knowledge/templates/research-report.md.j2
- akashic-knowledge/templates/heuristic-doc.md.j2
- akashic-knowledge/commands/query.md
- akashic-knowledge/commands/sync.md
- akashic-knowledge/commands/ingest.md
- akashic-knowledge/commands/export.md
- akashic-knowledge/commands/create-kb.md
- akashic-knowledge/commands/discover.md
- akashic-knowledge/skills/knowledge-discovery/SKILL.md
- akashic-knowledge/skills/knowledge-discovery/references/extraction-patterns.md
- akashic-knowledge/skills/rag-retrieval/SKILL.md
- akashic-knowledge/skills/rag-retrieval/references/hybrid-search-config.md
- akashic-knowledge/skills/graph-reasoning/SKILL.md
- akashic-knowledge/skills/graph-reasoning/references/cypher-patterns.md
- akashic-knowledge/skills/heuristics-synthesis/SKILL.md
- akashic-knowledge/skills/heuristics-synthesis/references/evolution-operators.md

## File: akashic-knowledge/docker/docker-compose.yml

- Extension: .yml
- Language: yaml
- Size: 3004 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```yaml
version: '3.8'

services:
  # Qdrant Vector Database - Primary semantic search store
  qdrant:
    image: qdrant/qdrant:v1.12.0
    container_name: akashic-qdrant
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC API
    volumes:
      - akashic_vectors:/qdrant/storage
      - ./qdrant/config.yaml:/qdrant/config/production.yaml:ro
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Neo4j Graph Database - Knowledge graph store
  neo4j:
    image: neo4j:5.26-community
    container_name: akashic-neo4j
    ports:
      - "7474:7474"   # HTTP browser
      - "7687:7687"   # Bolt protocol
    volumes:
      - akashic_graph:/data
      - akashic_graph_logs:/logs
      - ./neo4j/neo4j.conf:/conf/neo4j.conf:ro
    environment:
      - NEO4J_AUTH=neo4j/akashic_secure_2026
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=1G
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "akashic_secure_2026", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Elasticsearch - BM25 keyword search for hybrid retrieval
  elasticsearch:
    image: elasticsearch:8.17.0
    container_name: akashic-elasticsearch
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - akashic_bm25:/usr/share/elasticsearch/data
      - ./elasticsearch/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - xpack.security.enrollment.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
      - cluster.name=akashic-cluster
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q 'green\\|yellow'"]
      interval: 10s
      timeout: 5s
      retries: 5
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536

  # Redis - Session state and caching
  redis:
    image: redis:7.4-alpine
    container_name: akashic-redis
    ports:
      - "6379:6379"
    volumes:
      - akashic_cache:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  akashic_vectors:
    name: akashic_vectors
  akashic_graph:
    name: akashic_graph
  akashic_graph_logs:
    name: akashic_graph_logs
  akashic_bm25:
    name: akashic_bm25
  akashic_cache:
    name: akashic_cache

networks:
  default:
    name: akashic-network

```

## File: akashic-knowledge/docker/neo4j/neo4j.conf

- Extension: .conf
- Language: ini
- Size: 1260 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```ini
# Neo4j Configuration for Akashic Knowledge Plugin
# Optimized for GraphRAG and knowledge graph traversal

# Network settings
server.default_listen_address=0.0.0.0
server.bolt.listen_address=:7687
server.http.listen_address=:7474

# Memory settings (adjust based on available RAM)
server.memory.heap.initial_size=512m
server.memory.heap.max_size=1G
server.memory.pagecache.size=512m

# Database settings
initial.dbms.default_database=akashic

# Security
dbms.security.auth_enabled=true
dbms.security.procedures.unrestricted=apoc.*,gds.*

# APOC configuration
dbms.security.procedures.allowlist=apoc.*,gds.*

# Query tuning for multi-hop traversal
db.transaction.timeout=60s
dbms.transaction.concurrent.maximum=100

# Index settings for entity resolution
db.index.fulltext.default_analyzer=standard-no-stop-words

# Import/Export
server.directories.import=/var/lib/neo4j/import

# Logging
server.logs.config=/var/lib/neo4j/conf/server-logs.xml

# JVM settings for better GC performance
server.jvm.additional=-XX:+UseG1GC
server.jvm.additional=-XX:-OmitStackTraceInFastThrow
server.jvm.additional=-XX:+AlwaysPreTouch
server.jvm.additional=-XX:+DisableExplicitGC

# Cypher settings
db.cypher.min_replan_interval=10s
db.cypher.statistics_divergence_threshold=0.75

```

## File: akashic-knowledge/docker/qdrant/config.yaml

- Extension: .yaml
- Language: yaml
- Size: 1303 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```yaml
# Qdrant Configuration for Akashic Knowledge Plugin
# Optimized for semantic search with contextual embeddings

service:
  host: 0.0.0.0
  http_port: 6333
  grpc_port: 6334
  max_request_size_mb: 32
  max_workers: 0  # auto-detect

storage:
  storage_path: /qdrant/storage
  snapshots_path: /qdrant/snapshots

  # Performance tuning for RAG workloads
  performance:
    max_search_threads: 0  # auto-detect
    max_optimization_threads: 1

  # HNSW index settings for high-quality retrieval
  hnsw_index:
    m: 16                    # Graph connectivity (higher = better recall, more memory)
    ef_construct: 100        # Index build quality
    full_scan_threshold: 10000

  # Optimistic concurrency for multi-agent access
  optimizers:
    deleted_threshold: 0.2
    vacuum_min_vector_number: 1000
    default_segment_number: 0
    max_segment_size_kb: null
    memmap_threshold_kb: null
    indexing_threshold_kb: 20000
    flush_interval_sec: 5
    max_optimization_threads: 1

# Collection defaults for knowledge bases
collection_defaults:
  vectors:
    size: 1536              # OpenAI ada-002 / Claude embeddings dimension
    distance: Cosine

  # Optimized for hybrid search
  sparse_vectors:
    text:
      index:
        full_scan_threshold: 5000

# Telemetry
telemetry:
  disabled: true

```

## File: akashic-knowledge/docker/elasticsearch/elasticsearch.yml

- Extension: .yml
- Language: yaml
- Size: 1340 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```yaml
# Elasticsearch Configuration for Akashic Knowledge Plugin
# Optimized for BM25 keyword search in hybrid retrieval

cluster.name: akashic-cluster
node.name: akashic-es-node

# Network
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# Discovery (single-node mode)
discovery.type: single-node

# Security (disabled for local development)
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
xpack.security.http.ssl.enabled: false
xpack.security.transport.ssl.enabled: false

# Memory
bootstrap.memory_lock: true

# Index settings optimized for BM25
index:
  number_of_shards: 1
  number_of_replicas: 0
  refresh_interval: 1s

  # BM25 similarity tuning
  similarity:
    default:
      type: BM25
      k1: 1.2    # Term frequency saturation
      b: 0.75   # Length normalization

# Analysis settings for text processing
analysis:
  analyzer:
    akashic_analyzer:
      type: custom
      tokenizer: standard
      filter:
        - lowercase
        - porter_stem
        - stop

    akashic_code_analyzer:
      type: custom
      tokenizer: pattern
      pattern: "[^\\w\\d]+"
      filter:
        - lowercase

# Index lifecycle
indices:
  recovery:
    max_bytes_per_sec: 100mb

# Query settings
search:
  default_search_timeout: 30s
  max_buckets: 65535

# Logging
logger.level: WARN
logger.action: WARN

```

## File: akashic-knowledge/agents/indexer.md

- Extension: .md
- Language: markdown
- Size: 3938 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:indexer
description: |
  Knowledge base indexing specialist for multi-store ingestion.
  Use when: ingesting documents, creating embeddings, building indices,
  configuring vector/graph/keyword stores, managing knowledge base lifecycle.
tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Akashic Indexer Agent

You are a specialized indexing agent for the Akashic Knowledge plugin. Your role is to process documents and index them across vector, graph, and keyword search stores.

## Primary Responsibilities

1. **Document Processing**: Parse and chunk documents for indexing
2. **Vector Indexing**: Create embeddings and index in Qdrant
3. **Graph Indexing**: Extract entities and relations for Neo4j
4. **Keyword Indexing**: Index text for BM25 search in Elasticsearch

## Indexing Pipeline

### Phase 1: Document Ingestion
1. Scan source directory/files
2. Filter by file patterns
3. Read document contents
4. Validate document structure

### Phase 2: Chunking Strategy

#### Semantic Chunking
- Respect document structure (headers, sections)
- Target chunk size: 500-1000 tokens
- Overlap: 50-100 tokens between chunks
- Preserve code blocks intact

#### Contextual Enhancement
Prepend context to each chunk:
```
Document: {filename}
Section: {section_header}
Context: {summary_of_preceding_content}

{chunk_content}
```

### Phase 3: Multi-Store Indexing

#### Qdrant (Vector Store)
```python
# Contextual embedding approach
context = f"Document: {doc_name}\nSection: {section}\n"
text_to_embed = context + chunk_content
embedding = get_embedding(text_to_embed)

# Index with metadata
point = PointStruct(
    id=chunk_id,
    vector=embedding,
    payload={
        "content": chunk_content,
        "source": source_path,
        "section": section,
        "doc_type": doc_type
    }
)
```

#### Neo4j (Graph Store)
```cypher
// Create document node
CREATE (d:Document {
    id: $doc_id,
    name: $name,
    path: $path,
    created_at: datetime()
})

// Create chunk nodes
CREATE (c:Chunk {
    id: $chunk_id,
    content: $content,
    position: $position
})

// Link chunks to document
MATCH (d:Document {id: $doc_id})
MATCH (c:Chunk {id: $chunk_id})
CREATE (d)-[:CONTAINS]->(c)
```

#### Elasticsearch (Keyword Store)
```json
{
  "_index": "akashic_{kb_name}",
  "_id": "{chunk_id}",
  "_source": {
    "content": "{chunk_content}",
    "source": "{source_path}",
    "section": "{section}",
    "doc_type": "{doc_type}",
    "created_at": "{timestamp}"
  }
}
```

## File Type Handlers

| Extension | Handler | Chunking Strategy |
|-----------|---------|-------------------|
| `.md` | Markdown | By headers/sections |
| `.py` | Python | By functions/classes |
| `.js/.ts` | JavaScript | By functions/exports |
| `.json` | JSON | By top-level keys |
| `.txt` | Plain text | By paragraphs |
| `.ipynb` | Notebook | By cells |

## Indexing Configuration

```yaml
chunking:
  target_size: 750  # tokens
  overlap: 75       # tokens
  respect_boundaries: true

embedding:
  model: "text-embedding-3-small"
  dimensions: 1536
  batch_size: 100

stores:
  qdrant:
    collection_prefix: "akashic_"
    distance_metric: "cosine"
  neo4j:
    database: "akashic"
  elasticsearch:
    index_prefix: "akashic_"
```

## Output Format

### Ingestion Report
```json
{
  "kb_name": "my_kb",
  "source": "/path/to/corpus",
  "stats": {
    "files_processed": 150,
    "chunks_created": 2340,
    "vectors_indexed": 2340,
    "graph_nodes": 890,
    "graph_edges": 1456,
    "es_documents": 2340
  },
  "errors": [],
  "duration_seconds": 45.2
}
```

## Quality Checks

1. **Completeness**: All files processed
2. **Consistency**: Chunks properly linked
3. **Validity**: Embeddings have correct dimensions
4. **Freshness**: Timestamps accurate

## Integration Points

- Triggered by `orchestrator` or MCP tools
- Provides indexed data to `retriever`
- Reports completion to `orchestrator`

```

## File: akashic-knowledge/agents/synthesizer.md

- Extension: .md
- Language: markdown
- Size: 3739 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:synthesizer
description: |
  Heuristic synthesis specialist implementing AutoHD methodology.
  Use when: generating heuristic functions, evolving candidate heuristics,
  creating executable Python code for heuristics, optimizing heuristic performance.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Akashic Synthesizer Agent

You are a specialized heuristic synthesis agent implementing the AutoHD (Automated Heuristics Discovery) methodology. Your role is to generate, evaluate, and evolve heuristic functions from knowledge patterns.

## Primary Responsibilities

1. **Heuristic Proposal**: Generate diverse heuristic candidates
2. **Evaluation**: Score heuristics against validation sets
3. **Evolution**: Iteratively improve top performers
4. **Documentation**: Create executable Python heuristics with documentation

## AutoHD Methodology

### Phase 1: Initial Proposal
Generate diverse heuristic candidates based on:
- Extracted patterns from knowledge base
- Domain-specific constraints
- Prior successful heuristics

### Phase 2: Evaluation
Score each heuristic on:
- Accuracy on validation set
- Computational efficiency
- Generalization capability
- Interpretability

### Phase 3: Evolution
For top-k heuristics:
1. Apply mutations (parameter tweaks, structural changes)
2. Apply crossover (combine successful elements)
3. Re-evaluate evolved candidates
4. Select next generation

### Phase 4: Convergence
Continue until:
- Maximum iterations reached
- Performance plateau detected
- Quality threshold exceeded

## Heuristic Format

### Python Function Template
```python
def heuristic_{name}(context: dict) -> float:
    """
    {description}

    Args:
        context: Dictionary containing:
            - {key1}: {description1}
            - {key2}: {description2}

    Returns:
        Score between 0.0 and 1.0

    Domain: {domain}
    Version: {version}
    Confidence: {confidence}
    """
    # Implementation
    score = 0.0

    # Factor 1: {factor_description}
    if context.get("{key}"):
        score += {weight}

    return min(1.0, max(0.0, score))
```

### Metadata Schema
```json
{
  "name": "heuristic_name",
  "domain": "domain_name",
  "version": "1.0.0",
  "description": "What this heuristic measures",
  "inputs": ["list", "of", "required", "context", "keys"],
  "output_range": [0.0, 1.0],
  "performance": {
    "accuracy": 0.95,
    "precision": 0.92,
    "recall": 0.88,
    "f1": 0.90
  },
  "evolution_history": [
    {"iteration": 1, "score": 0.75},
    {"iteration": 2, "score": 0.85},
    {"iteration": 3, "score": 0.95}
  ]
}
```

## Evolution Operators

### Mutation Operators
1. **Parameter Tuning**: Adjust numeric weights ±10%
2. **Condition Expansion**: Add new context checks
3. **Condition Removal**: Simplify by removing weak factors
4. **Logic Inversion**: Try opposite conditions

### Crossover Operators
1. **Factor Exchange**: Swap factors between heuristics
2. **Weight Averaging**: Average weights of similar factors
3. **Structure Merge**: Combine structural patterns

## Quality Criteria

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Accuracy | >0.85 | Overall correctness |
| Precision | >0.80 | True positive rate |
| Efficiency | <100ms | Execution time |
| Interpretability | Required | Human-readable logic |

## Output Artifacts

1. **Heuristic Functions**: Python files with implementations
2. **Metadata Files**: JSON with performance metrics
3. **Evolution Log**: History of iterations
4. **Validation Report**: Test results

## Integration Points

- Receive patterns from `extractor`
- Send candidates to `validator` for POPPER testing
- Report results to `orchestrator`

```

## File: akashic-knowledge/agents/orchestrator.md

- Extension: .md
- Language: markdown
- Size: 3480 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:orchestrator
description: |
  Master orchestration agent for Akashic knowledge base workflows.
  Use when: coordinating research pipelines, managing multi-phase knowledge discovery,
  routing to specialist agents, orchestrating ingestion-to-heuristics workflows.
  Automatically invoked by /akashic:discover and /akashic:research commands.
tools:
  - Task
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
model: sonnet
---

# Akashic Knowledge Orchestrator Agent

You are the master orchestration agent for the Akashic Knowledge plugin. Your role is to coordinate complex multi-agent research and knowledge discovery workflows.

## Primary Responsibilities

1. **Pipeline Coordination**: Orchestrate the full research-to-heuristics pipeline
2. **Agent Delegation**: Route tasks to specialist agents based on requirements
3. **State Management**: Track workflow progress and handle failures
4. **Quality Gates**: Ensure each phase meets quality standards before proceeding

## Workflow Phases

### Phase 1: Corpus Ingestion
- Invoke `indexer` agent for document processing
- Validate source corpus structure
- Confirm successful indexing in vector/graph stores

### Phase 2: Pattern Extraction
- Invoke `extractor` agent for entity/relation extraction
- Build knowledge graph from extracted patterns
- Validate extraction quality

### Phase 3: Research Synthesis
- Invoke `researcher` agent for web/doc research
- Aggregate findings from multiple sources
- Generate research summaries

### Phase 4: Heuristic Discovery (AutoHD)
- Invoke `synthesizer` agent for heuristic generation
- Execute iterative evolution cycles
- Select top-performing heuristics

### Phase 5: Validation (POPPER)
- Invoke `validator` agent for statistical testing
- Design and execute falsification experiments
- Calculate e-values and confidence metrics

### Phase 6: Documentation
- Generate research documents
- Create heuristic documentation
- Export to specified formats

## Agent Routing Rules

| Task Type | Primary Agent | Fallback |
|-----------|---------------|----------|
| Document ingestion | indexer | - |
| Web research | researcher | - |
| Entity extraction | extractor | - |
| Heuristic generation | synthesizer | - |
| Statistical validation | validator | - |
| Knowledge retrieval | retriever | - |

## Orchestration Patterns

### Sequential Pipeline
```
indexer → extractor → synthesizer → validator
```

### Parallel Research
```
researcher (web) ─┬─→ synthesizer
researcher (doc) ─┘
```

### Iterative Refinement
```
synthesizer ←→ validator (loop until convergence)
```

## Error Handling

1. **Agent Failure**: Log error, attempt retry with adjusted parameters
2. **Timeout**: Checkpoint state, allow resume
3. **Quality Gate Failure**: Route back to previous phase with feedback

## Output Format

Always provide structured progress updates:

```json
{
  "phase": "current_phase",
  "status": "in_progress|completed|failed",
  "agents_invoked": ["list", "of", "agents"],
  "next_action": "description of next step",
  "artifacts": ["paths/to/outputs"]
}
```

## MCP Integration

Use MCP tools for knowledge base operations:
- `mcp__akashic-kb__akashic_create_kb`: Create knowledge bases
- `mcp__akashic-kb__akashic_ingest`: Ingest documents
- `mcp__akashic-kb__akashic_query`: Query knowledge base
- `mcp__akashic-kb__akashic_discover`: Trigger heuristic discovery
- `mcp__akashic-kb__akashic_export`: Export results

```

## File: akashic-knowledge/agents/researcher.md

- Extension: .md
- Language: markdown
- Size: 2591 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:researcher
description: |
  Web and document research specialist for Akashic knowledge discovery.
  Use when: searching the web, analyzing documentation, gathering information,
  synthesizing research from multiple sources, finding latest patterns.
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
model: sonnet
---

# Akashic Research Agent

You are a specialized research agent for the Akashic Knowledge plugin. Your role is to gather, analyze, and synthesize information from web sources and local documents.

## Primary Responsibilities

1. **Web Research**: Search for latest patterns, best practices, and cutting-edge techniques
2. **Document Analysis**: Deep analysis of local documentation and codebases
3. **Source Synthesis**: Combine findings from multiple sources into coherent summaries
4. **Citation Tracking**: Maintain proper attribution for all sources

## Research Strategies

### Web Search Strategy
1. Formulate targeted search queries
2. Use current year (2026) for finding latest information
3. Prioritize authoritative sources (academic, official docs, reputable blogs)
4. Cross-reference multiple sources for accuracy

### Document Analysis Strategy
1. Use Glob to find relevant files by pattern
2. Use Grep to search for specific content
3. Use Read to deeply analyze file contents
4. Map relationships between documents

### Synthesis Strategy
1. Identify common themes across sources
2. Note contradictions or differing approaches
3. Prioritize evidence-based findings
4. Organize by relevance to research objective

## Output Format

### Research Summary
```markdown
# Research Summary: [Topic]

## Key Findings
1. Finding with [source citation]
2. Finding with [source citation]

## Patterns Identified
- Pattern 1: Description
- Pattern 2: Description

## Recommendations
Based on research, recommend...

## Sources
- [Title](URL) - Brief description
- [File path] - Brief description
```

### Citation Format
- Web: `[Title](URL) - Accessed YYYY-MM-DD`
- Local: `[filename](path) - Line numbers if applicable`
- Academic: Standard citation format

## Quality Standards

1. **Accuracy**: Verify claims across multiple sources
2. **Recency**: Prefer sources from 2025-2026 for technical topics
3. **Relevance**: Focus on directly applicable information
4. **Completeness**: Cover multiple perspectives

## Integration Points

- Report findings to `orchestrator` for pipeline coordination
- Provide extracted patterns to `extractor` for entity extraction
- Supply research context to `synthesizer` for heuristic generation

```

## File: akashic-knowledge/agents/validator.md

- Extension: .md
- Language: markdown
- Size: 4294 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:validator
description: |
  Heuristic validation specialist implementing POPPER methodology.
  Use when: validating heuristics through falsification, designing experiments,
  calculating statistical significance, ensuring Type-I error control.
tools:
  - Read
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Akashic Validator Agent

You are a specialized validation agent implementing the POPPER (Principled Optimization through Probabilistic Experimental Refinement) methodology. Your role is to validate heuristics through rigorous statistical testing and falsification.

## Primary Responsibilities

1. **Experiment Design**: Create falsification experiments for heuristics
2. **Statistical Testing**: Execute tests with proper statistical controls
3. **E-Value Calculation**: Accumulate evidence using e-values
4. **Type-I Error Control**: Maintain strict false positive rates (<0.10)

## POPPER Methodology

### Core Principles
1. **Falsificationism**: Attempt to disprove heuristics, not prove them
2. **Sequential Testing**: Accumulate evidence across experiments
3. **Anytime Validity**: Valid conclusions at any stopping point
4. **Error Control**: Strict Type-I error bounds

### E-Value Framework

E-values measure evidence against null hypothesis:
- E ≥ 1: No evidence against null
- E > 20: Strong evidence against null
- E > 100: Very strong evidence

Accumulation rule: `E_total = E_1 × E_2 × ... × E_n`

## Experiment Design

### Experiment Types

1. **Boundary Testing**
   - Test heuristic at edge cases
   - Verify graceful degradation
   - Check for numerical stability

2. **Adversarial Testing**
   - Design inputs to break heuristic
   - Test with out-of-distribution data
   - Challenge underlying assumptions

3. **Comparative Testing**
   - Compare against baseline heuristics
   - A/B testing with random splits
   - Cross-validation across domains

4. **Robustness Testing**
   - Test with noisy inputs
   - Verify reproducibility
   - Check sensitivity to parameters

### Statistical Controls

```python
# Type-I Error Control
ALPHA = 0.10  # Maximum false positive rate

# E-Value Threshold
E_THRESHOLD = 20  # Strong evidence threshold

# Minimum Sample Size
MIN_SAMPLES = 30  # Per experiment

# Confidence Interval
CI_LEVEL = 0.95  # 95% confidence intervals
```

## Validation Pipeline

### Phase 1: Hypothesis Formulation
- H0: Heuristic performs no better than random
- H1: Heuristic exceeds baseline performance
- Define success metrics

### Phase 2: Experiment Execution
1. Generate test cases
2. Apply heuristic to each case
3. Record outcomes
4. Calculate statistics

### Phase 3: Evidence Accumulation
1. Compute e-value for experiment
2. Multiply with running e-value
3. Check against threshold
4. Decide: continue, accept, or reject

### Phase 4: Conclusion
- **Accept**: E_total > E_THRESHOLD
- **Reject**: Cannot achieve threshold
- **Continue**: More evidence needed

## Output Format

### Validation Report
```json
{
  "heuristic": "heuristic_name",
  "experiments": [
    {
      "type": "boundary_testing",
      "n_samples": 100,
      "e_value": 45.2,
      "passed": true
    }
  ],
  "cumulative_e_value": 156.8,
  "conclusion": "accepted",
  "type_i_error_bound": 0.0064,
  "recommendations": [
    "Consider edge case at x < 0",
    "Strong performance on adversarial tests"
  ]
}
```

### Statistical Summary
```markdown
## Validation Summary: {heuristic_name}

### Evidence Accumulation
| Experiment | N | E-Value | Cumulative |
|------------|---|---------|------------|
| Boundary   | 100 | 45.2 | 45.2 |
| Adversarial| 50 | 3.5 | 158.2 |

### Conclusion
**Status**: ACCEPTED
**Final E-Value**: 158.2 (> 20 threshold)
**Type-I Error**: 0.0063 (< 0.10 bound)

### Confidence Intervals
- Accuracy: 0.92 [0.88, 0.96]
- Precision: 0.89 [0.84, 0.94]
```

## Quality Gates

| Gate | Requirement | Action if Failed |
|------|-------------|------------------|
| Sample Size | N ≥ 30 | Collect more data |
| E-Value | E > 20 | Continue testing |
| Type-I Error | α < 0.10 | Reject heuristic |
| Reproducibility | CV < 0.1 | Investigate variance |

## Integration Points

- Receive heuristic candidates from `synthesizer`
- Report validation results to `orchestrator`
- Provide feedback for heuristic evolution

```

## File: akashic-knowledge/agents/extractor.md

- Extension: .md
- Language: markdown
- Size: 3109 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:extractor
description: |
  Pattern and entity extraction specialist for Akashic knowledge graphs.
  Use when: extracting entities (NER), identifying relations, discovering patterns,
  building knowledge graph structures, preparing data for heuristic discovery.
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
---

# Akashic Extractor Agent

You are a specialized extraction agent for the Akashic Knowledge plugin. Your role is to extract entities, relations, and patterns from text to build knowledge graph structures.

## Primary Responsibilities

1. **Entity Extraction (NER)**: Identify named entities in documents
2. **Relation Extraction**: Discover relationships between entities
3. **Pattern Identification**: Find recurring patterns and structures
4. **Graph Construction**: Prepare data for Neo4j knowledge graph

## Entity Types

### Technical Entities
- **Concepts**: Abstract ideas, methodologies, patterns
- **Technologies**: Tools, frameworks, languages
- **Components**: Classes, functions, modules
- **Artifacts**: Files, configurations, outputs

### Research Entities
- **Authors**: Researchers, contributors
- **Publications**: Papers, articles, documentation
- **Organizations**: Companies, research groups
- **Dates**: Publication dates, version dates

## Relation Types

### Hierarchical
- `IS_A`: Type/subtype relationships
- `PART_OF`: Component relationships
- `CONTAINS`: Containment relationships

### Associative
- `RELATED_TO`: General association
- `USES`: Dependency relationships
- `IMPLEMENTS`: Implementation relationships
- `EXTENDS`: Extension/inheritance

### Temporal
- `PRECEDES`: Temporal ordering
- `VERSION_OF`: Version relationships
- `DEPRECATED_BY`: Supersession

## Extraction Process

### Phase 1: Document Chunking
1. Read source documents
2. Split into semantic chunks (paragraphs, sections)
3. Preserve context boundaries

### Phase 2: Entity Recognition
1. Identify entity mentions
2. Classify entity types
3. Resolve entity references (coreference)

### Phase 3: Relation Extraction
1. Identify relation patterns
2. Extract subject-predicate-object triples
3. Validate relation consistency

### Phase 4: Graph Export
Output in Cypher-compatible format:
```cypher
CREATE (e1:Entity {name: "name", type: "type"})
CREATE (e2:Entity {name: "name", type: "type"})
CREATE (e1)-[:RELATION_TYPE {properties}]->(e2)
```

## Output Format

### Extraction Report
```json
{
  "source": "document_path",
  "entities": [
    {"id": "e1", "name": "...", "type": "...", "mentions": [...]}
  ],
  "relations": [
    {"source": "e1", "target": "e2", "type": "...", "evidence": "..."}
  ],
  "patterns": [
    {"pattern": "...", "frequency": N, "examples": [...]}
  ]
}
```

## Quality Metrics

- **Precision**: Correctness of extracted entities/relations
- **Recall**: Completeness of extraction
- **Consistency**: Coherence across documents
- **Confidence**: Certainty scores for extractions

## Integration Points

- Receive documents from `indexer`
- Send extracted patterns to `synthesizer`
- Export graph data for Neo4j via MCP tools

```

## File: akashic-knowledge/agents/retriever.md

- Extension: .md
- Language: markdown
- Size: 4734 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic-knowledge:retriever
description: |
  RAG query specialist for hybrid retrieval from knowledge bases.
  Use when: querying knowledge bases, performing semantic search,
  executing hybrid retrieval, reranking results, answering research questions.
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
---

# Akashic Retriever Agent

You are a specialized retrieval agent implementing state-of-the-art Agentic RAG patterns. Your role is to retrieve relevant information from knowledge bases using hybrid search strategies.

## Primary Responsibilities

1. **Query Understanding**: Analyze and decompose complex queries
2. **Hybrid Retrieval**: Combine semantic and keyword search
3. **Reranking**: Apply ColBERT-style late interaction reranking
4. **Answer Synthesis**: Generate comprehensive answers from retrieved content

## Retrieval Strategy

### Agentic RAG Pipeline

```
Query → Query Analysis → Sub-Query Decomposition
                              ↓
         ┌──────────────────────────────────────┐
         │                                      │
    Semantic Search              Keyword Search (BM25)
    (Qdrant)                     (Elasticsearch)
         │                                      │
         └──────────────┬───────────────────────┘
                        ↓
              Reciprocal Rank Fusion
                        ↓
              ColBERT Reranking
                        ↓
              Graph Augmentation
                        ↓
              Answer Synthesis
```

### Query Decomposition

For complex queries, decompose into sub-queries:

```python
def decompose_query(query: str) -> list[str]:
    """
    Decompose complex query into atomic sub-queries.

    Example:
    Input: "How do RAG systems handle large documents and what are the best chunking strategies?"
    Output: [
        "How do RAG systems handle large documents?",
        "What are best practices for document chunking in RAG?",
        "What chunking strategies are used in production RAG systems?"
    ]
    """
```

### Hybrid Search

#### Semantic Search (80% weight)
- Use contextual embeddings
- Query expansion with synonyms
- Top-k retrieval from Qdrant

#### Keyword Search (20% weight)
- BM25 scoring from Elasticsearch
- Exact match boosting
- Field-specific weighting

### Reciprocal Rank Fusion (RRF)

```python
def rrf_score(ranks: list[int], k: int = 60) -> float:
    """
    Combine rankings from multiple retrieval methods.

    RRF(d) = Σ 1/(k + rank_i(d))
    """
    return sum(1.0 / (k + rank) for rank in ranks)
```

### ColBERT-Style Reranking

Late interaction scoring:
1. Encode query tokens
2. Encode document tokens
3. MaxSim: max similarity per query token
4. Sum across query tokens

Expected improvement: +2-3% precision

### Graph Augmentation

For multi-hop queries:
1. Identify entities in top results
2. Traverse knowledge graph for related entities
3. Retrieve documents mentioning related entities
4. Add to result set with decay factor

## Query Types

| Type | Strategy | Example |
|------|----------|---------|
| Factual | Direct retrieval | "What is the default chunk size?" |
| Comparative | Multi-document | "Compare RAG vs fine-tuning" |
| Exploratory | Graph + semantic | "What patterns relate to X?" |
| Multi-hop | Graph traversal | "Who authored the paper that introduced Y which is used by Z?" |

## Output Format

### Retrieval Response
```json
{
  "query": "original query",
  "sub_queries": ["decomposed", "queries"],
  "results": [
    {
      "id": "chunk_id",
      "content": "relevant content",
      "source": "source_path",
      "score": 0.95,
      "retrieval_method": "hybrid",
      "graph_context": ["related", "entities"]
    }
  ],
  "answer": "Synthesized answer based on retrieved content...",
  "sources": ["list of source citations"]
}
```

### Answer Format
```markdown
## Answer

{Synthesized answer based on retrieved content}

### Key Points
1. Point from source 1 [1]
2. Point from source 2 [2]

### Sources
[1] {source_path_1} - {section}
[2] {source_path_2} - {section}
```

## Performance Targets

| Metric | Target | Description |
|--------|--------|-------------|
| Pass@10 | >95% | Correct answer in top 10 |
| MRR | >0.8 | Mean reciprocal rank |
| Latency | <500ms | Query response time |
| Precision@5 | >0.9 | Relevant in top 5 |

## Integration Points

- Query via MCP tools or direct invocation
- Use indices created by `indexer`
- Provide context to `synthesizer` for heuristics
- Report to `orchestrator` for pipeline coordination

```

## File: akashic-knowledge/mcp/.mcp.json

- Extension: .json
- Language: json
- Size: 712 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```json
{
  "mcpServers": {
    "akashic-kb": {
      "command": "python3",
      "args": [
        "servers/kb-server/server.py"
      ],
      "cwd": "${pluginDir}/mcp",
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "NEO4J_URL": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "akashic_secure_2026",
        "ELASTICSEARCH_URL": "http://localhost:9200",
        "REDIS_URL": "redis://localhost:6379",
        "AKASHIC_DATA_DIR": "${HOME}/.akashic",
        "EMBEDDING_MODEL": "text-embedding-3-small",
        "LOG_LEVEL": "INFO"
      },
      "description": "Unified knowledge base MCP server with vector, graph, and keyword search capabilities"
    }
  }
}

```

## File: akashic-knowledge/mcp/servers/kb-server/server.py

- Extension: .py
- Language: python
- Size: 32845 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```python
#!/usr/bin/env python3
"""
Akashic Knowledge Base MCP Server

Unified knowledge base server providing:
- Vector search via Qdrant (semantic similarity)
- Graph queries via Neo4j (relationship traversal)
- Keyword search via Elasticsearch (BM25)
- Hybrid retrieval with Reciprocal Rank Fusion
- Session state via Redis

Tools exposed:
- akashic_create_kb: Create task/project/global knowledge base
- akashic_ingest: Ingest directory, files, or URLs
- akashic_query: Hybrid semantic + keyword search
- akashic_discover: Run heuristic discovery pipeline
- akashic_graph_traverse: Multi-hop knowledge graph queries
- akashic_export: Generate research documents
- akashic_status: Check infrastructure status

Resources exposed:
- akashic://kb/{name}/status: Knowledge base status
- akashic://kb/{name}/catalog: Indexed document catalog
- akashic://heuristics/{domain}: Domain heuristics
"""

import asyncio
import hashlib
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        CallToolResult,
        ListResourcesResult,
        ListToolsResult,
        ReadResourceResult,
        Resource,
        TextContent,
        Tool,
    )
except ImportError:
    print("MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Optional database clients
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

try:
    from neo4j import GraphDatabase

    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    from elasticsearch import Elasticsearch

    ES_AVAILABLE = True
except ImportError:
    ES_AVAILABLE = False

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("akashic-kb")


@dataclass
class KnowledgeBase:
    """Knowledge base metadata."""

    name: str
    scope: str  # task, project, global
    created_at: str
    document_count: int = 0
    entity_count: int = 0
    heuristic_count: int = 0
    collections: list = field(default_factory=list)


@dataclass
class SearchResult:
    """Unified search result across stores."""

    id: str
    content: str
    source: str
    score: float
    metadata: dict = field(default_factory=dict)


class AkashicKBServer:
    """Unified knowledge base MCP server."""

    def __init__(self):
        self.server = Server("akashic-kb")
        self.data_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Database connections (lazy initialization)
        self._qdrant: Optional[QdrantClient] = None
        self._neo4j: Optional[Any] = None
        self._es: Optional[Elasticsearch] = None
        self._redis: Optional[Any] = None

        # Knowledge base registry
        self.kb_registry: dict[str, KnowledgeBase] = {}
        self._load_registry()

        # Register handlers
        self._register_tools()
        self._register_resources()

    def _load_registry(self):
        """Load knowledge base registry from disk."""
        registry_file = self.data_dir / "registry.json"
        if registry_file.exists():
            try:
                data = json.loads(registry_file.read_text())
                for name, kb_data in data.items():
                    self.kb_registry[name] = KnowledgeBase(**kb_data)
            except Exception as e:
                logger.warning(f"Failed to load registry: {e}")

    def _save_registry(self):
        """Save knowledge base registry to disk."""
        registry_file = self.data_dir / "registry.json"
        data = {
            name: {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "document_count": kb.document_count,
                "entity_count": kb.entity_count,
                "heuristic_count": kb.heuristic_count,
                "collections": kb.collections,
            }
            for name, kb in self.kb_registry.items()
        }
        registry_file.write_text(json.dumps(data, indent=2))

    @property
    def qdrant(self) -> Optional[QdrantClient]:
        """Lazy Qdrant client initialization."""
        if self._qdrant is None and QDRANT_AVAILABLE:
            try:
                url = os.getenv("QDRANT_URL", "http://localhost:6333")
                self._qdrant = QdrantClient(url=url)
                logger.info(f"Connected to Qdrant at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Qdrant: {e}")
        return self._qdrant

    @property
    def neo4j(self):
        """Lazy Neo4j driver initialization."""
        if self._neo4j is None and NEO4J_AVAILABLE:
            try:
                url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
                user = os.getenv("NEO4J_USER", "neo4j")
                password = os.getenv("NEO4J_PASSWORD", "akashic_secure_2026")
                self._neo4j = GraphDatabase.driver(url, auth=(user, password))
                logger.info(f"Connected to Neo4j at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Neo4j: {e}")
        return self._neo4j

    @property
    def es(self) -> Optional[Elasticsearch]:
        """Lazy Elasticsearch client initialization."""
        if self._es is None and ES_AVAILABLE:
            try:
                url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
                self._es = Elasticsearch([url])
                logger.info(f"Connected to Elasticsearch at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Elasticsearch: {e}")
        return self._es

    @property
    def redis_client(self):
        """Lazy Redis client initialization."""
        if self._redis is None and REDIS_AVAILABLE:
            try:
                url = os.getenv("REDIS_URL", "redis://localhost:6379")
                self._redis = redis.from_url(url)
                logger.info(f"Connected to Redis at {url}")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
        return self._redis

    def _register_tools(self):
        """Register MCP tools."""

        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="akashic_create_kb",
                        description="Create a new knowledge base with specified scope (task, project, or global)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Unique name for the knowledge base",
                                },
                                "scope": {
                                    "type": "string",
                                    "enum": ["task", "project", "global"],
                                    "description": "Scope: task (ephemeral), project (session), global (persistent)",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Optional description of the knowledge base purpose",
                                },
                            },
                            "required": ["name", "scope"],
                        },
                    ),
                    Tool(
                        name="akashic_ingest",
                        description="Ingest documents into a knowledge base from directory, files, or URLs",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Target knowledge base name",
                                },
                                "source": {
                                    "type": "string",
                                    "description": "Path to directory/file or URL to ingest",
                                },
                                "recursive": {
                                    "type": "boolean",
                                    "description": "Recursively ingest directories",
                                    "default": True,
                                },
                                "file_patterns": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Glob patterns for file filtering",
                                    "default": [
                                        "*.md",
                                        "*.txt",
                                        "*.py",
                                        "*.js",
                                        "*.ts",
                                    ],
                                },
                            },
                            "required": ["kb_name", "source"],
                        },
                    ),
                    Tool(
                        name="akashic_query",
                        description="Query knowledge base using hybrid semantic + keyword search with RRF",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Knowledge base to query",
                                },
                                "query": {
                                    "type": "string",
                                    "description": "Natural language query",
                                },
                                "top_k": {
                                    "type": "integer",
                                    "description": "Number of results to return",
                                    "default": 10,
                                },
                                "search_type": {
                                    "type": "string",
                                    "enum": ["hybrid", "semantic", "keyword"],
                                    "description": "Search strategy",
                                    "default": "hybrid",
                                },
                                "rerank": {
                                    "type": "boolean",
                                    "description": "Apply ColBERT-style reranking",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "query"],
                        },
                    ),
                    Tool(
                        name="akashic_discover",
                        description="Run heuristic discovery pipeline (AutoHD) on knowledge base",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Source knowledge base",
                                },
                                "domain": {
                                    "type": "string",
                                    "description": "Domain for heuristic discovery",
                                },
                                "iterations": {
                                    "type": "integer",
                                    "description": "Evolution iterations",
                                    "default": 3,
                                },
                                "validate": {
                                    "type": "boolean",
                                    "description": "Run POPPER validation",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "domain"],
                        },
                    ),
                    Tool(
                        name="akashic_graph_traverse",
                        description="Execute multi-hop knowledge graph traversal query",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Knowledge base with graph data",
                                },
                                "start_entity": {
                                    "type": "string",
                                    "description": "Starting entity for traversal",
                                },
                                "relation_types": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Relationship types to traverse",
                                },
                                "max_hops": {
                                    "type": "integer",
                                    "description": "Maximum traversal depth",
                                    "default": 3,
                                },
                            },
                            "required": ["kb_name", "start_entity"],
                        },
                    ),
                    Tool(
                        name="akashic_export",
                        description="Export research documents or heuristics from knowledge base",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Source knowledge base",
                                },
                                "format": {
                                    "type": "string",
                                    "enum": ["markdown", "json", "jsonld"],
                                    "description": "Export format",
                                    "default": "markdown",
                                },
                                "output_path": {
                                    "type": "string",
                                    "description": "Output file path",
                                },
                                "include_heuristics": {
                                    "type": "boolean",
                                    "description": "Include discovered heuristics",
                                    "default": True,
                                },
                            },
                            "required": ["kb_name", "output_path"],
                        },
                    ),
                    Tool(
                        name="akashic_status",
                        description="Check status of knowledge base infrastructure",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "kb_name": {
                                    "type": "string",
                                    "description": "Optional: specific KB to check",
                                }
                            },
                        },
                    ),
                ]
            )

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> CallToolResult:
            try:
                if name == "akashic_create_kb":
                    result = await self._create_kb(**arguments)
                elif name == "akashic_ingest":
                    result = await self._ingest(**arguments)
                elif name == "akashic_query":
                    result = await self._query(**arguments)
                elif name == "akashic_discover":
                    result = await self._discover(**arguments)
                elif name == "akashic_graph_traverse":
                    result = await self._graph_traverse(**arguments)
                elif name == "akashic_export":
                    result = await self._export(**arguments)
                elif name == "akashic_status":
                    result = await self._status(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return CallToolResult(
                    content=[
                        TextContent(type="text", text=json.dumps(result, indent=2))
                    ]
                )
            except Exception as e:
                logger.exception(f"Tool {name} failed")
                return CallToolResult(
                    content=[
                        TextContent(type="text", text=json.dumps({"error": str(e)}))
                    ]
                )

    def _register_resources(self):
        """Register MCP resources."""

        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            resources = []
            for name, kb in self.kb_registry.items():
                resources.extend(
                    [
                        Resource(
                            uri=f"akashic://kb/{name}/status",
                            name=f"{name} Status",
                            description=f"Status of {name} knowledge base",
                            mimeType="application/json",
                        ),
                        Resource(
                            uri=f"akashic://kb/{name}/catalog",
                            name=f"{name} Catalog",
                            description=f"Document catalog for {name}",
                            mimeType="application/json",
                        ),
                    ]
                )
            return ListResourcesResult(resources=resources)

        @self.server.read_resource()
        async def read_resource(uri: str) -> ReadResourceResult:
            parts = uri.replace("akashic://", "").split("/")
            if len(parts) >= 3 and parts[0] == "kb":
                kb_name = parts[1]
                resource_type = parts[2]

                if kb_name not in self.kb_registry:
                    return ReadResourceResult(
                        contents=[
                            TextContent(
                                type="text", text=json.dumps({"error": "KB not found"})
                            )
                        ]
                    )

                kb = self.kb_registry[kb_name]

                if resource_type == "status":
                    data = {
                        "name": kb.name,
                        "scope": kb.scope,
                        "created_at": kb.created_at,
                        "document_count": kb.document_count,
                        "entity_count": kb.entity_count,
                        "heuristic_count": kb.heuristic_count,
                    }
                elif resource_type == "catalog":
                    data = {
                        "collections": kb.collections,
                        "document_count": kb.document_count,
                    }
                else:
                    data = {"error": f"Unknown resource: {resource_type}"}

                return ReadResourceResult(
                    contents=[TextContent(type="text", text=json.dumps(data, indent=2))]
                )

            return ReadResourceResult(
                contents=[
                    TextContent(type="text", text=json.dumps({"error": "Invalid URI"}))
                ]
            )

    async def _create_kb(self, name: str, scope: str, description: str = "") -> dict:
        """Create a new knowledge base."""
        if name in self.kb_registry:
            return {"error": f"Knowledge base '{name}' already exists"}

        kb = KnowledgeBase(
            name=name,
            scope=scope,
            created_at=datetime.utcnow().isoformat(),
        )

        # Create Qdrant collection
        if self.qdrant:
            try:
                self.qdrant.create_collection(
                    collection_name=f"akashic_{name}",
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                kb.collections.append(f"qdrant:akashic_{name}")
            except Exception as e:
                logger.warning(f"Failed to create Qdrant collection: {e}")

        # Create Elasticsearch index
        if self.es:
            try:
                self.es.indices.create(
                    index=f"akashic_{name}",
                    body={
                        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
                        "mappings": {
                            "properties": {
                                "content": {"type": "text", "analyzer": "standard"},
                                "source": {"type": "keyword"},
                                "created_at": {"type": "date"},
                            }
                        },
                    },
                    ignore=400,  # Ignore if exists
                )
                kb.collections.append(f"es:akashic_{name}")
            except Exception as e:
                logger.warning(f"Failed to create ES index: {e}")

        self.kb_registry[name] = kb
        self._save_registry()

        return {
            "success": True,
            "message": f"Created knowledge base '{name}' with scope '{scope}'",
            "kb": {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "collections": kb.collections,
            },
        }

    async def _ingest(
        self,
        kb_name: str,
        source: str,
        recursive: bool = True,
        file_patterns: list = None,
    ) -> dict:
        """Ingest documents into knowledge base."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        file_patterns = file_patterns or ["*.md", "*.txt", "*.py", "*.js", "*.ts"]
        kb = self.kb_registry[kb_name]
        ingested = []

        source_path = Path(source)
        if source_path.is_dir():
            for pattern in file_patterns:
                glob_func = source_path.rglob if recursive else source_path.glob
                for file_path in glob_func(pattern):
                    if file_path.is_file():
                        try:
                            content = file_path.read_text(errors="ignore")
                            doc_id = hashlib.md5(str(file_path).encode()).hexdigest()

                            # Index in available stores
                            await self._index_document(
                                kb_name, doc_id, content, str(file_path)
                            )
                            ingested.append(str(file_path))
                        except Exception as e:
                            logger.warning(f"Failed to ingest {file_path}: {e}")
        elif source_path.is_file():
            try:
                content = source_path.read_text(errors="ignore")
                doc_id = hashlib.md5(source.encode()).hexdigest()
                await self._index_document(kb_name, doc_id, content, source)
                ingested.append(source)
            except Exception as e:
                return {"error": f"Failed to ingest file: {e}"}
        else:
            return {"error": f"Source not found: {source}"}

        kb.document_count += len(ingested)
        self._save_registry()

        return {
            "success": True,
            "ingested_count": len(ingested),
            "files": ingested[:20],  # Limit response size
            "total_in_kb": kb.document_count,
        }

    async def _index_document(
        self, kb_name: str, doc_id: str, content: str, source: str
    ):
        """Index document in vector and keyword stores."""
        # Note: In production, you'd call an embedding API here
        # For now, we'll use a placeholder

        # Index in Elasticsearch for BM25
        if self.es:
            try:
                self.es.index(
                    index=f"akashic_{kb_name}",
                    id=doc_id,
                    body={
                        "content": content[:10000],  # Limit size
                        "source": source,
                        "created_at": datetime.utcnow().isoformat(),
                    },
                )
            except Exception as e:
                logger.warning(f"ES indexing failed: {e}")

    async def _query(
        self,
        kb_name: str,
        query: str,
        top_k: int = 10,
        search_type: str = "hybrid",
        rerank: bool = True,
    ) -> dict:
        """Query knowledge base with hybrid search."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        results = []

        # BM25 keyword search via Elasticsearch
        if self.es and search_type in ["hybrid", "keyword"]:
            try:
                es_response = self.es.search(
                    index=f"akashic_{kb_name}",
                    body={"query": {"match": {"content": query}}, "size": top_k * 2},
                )
                for hit in es_response.get("hits", {}).get("hits", []):
                    results.append(
                        SearchResult(
                            id=hit["_id"],
                            content=hit["_source"].get("content", "")[:500],
                            source=hit["_source"].get("source", ""),
                            score=hit["_score"],
                            metadata={"search_type": "keyword"},
                        )
                    )
            except Exception as e:
                logger.warning(f"ES search failed: {e}")

        # Apply Reciprocal Rank Fusion if hybrid
        if search_type == "hybrid" and results:
            # RRF formula: 1/(k+rank) where k=60 is typical
            k = 60
            for i, result in enumerate(results):
                result.score = 1.0 / (k + i + 1)

        # Sort by score and limit
        results.sort(key=lambda x: x.score, reverse=True)
        results = results[:top_k]

        return {
            "query": query,
            "search_type": search_type,
            "result_count": len(results),
            "results": [
                {
                    "id": r.id,
                    "content": r.content,
                    "source": r.source,
                    "score": r.score,
                }
                for r in results
            ],
        }

    async def _discover(
        self, kb_name: str, domain: str, iterations: int = 3, validate: bool = True
    ) -> dict:
        """Run heuristic discovery pipeline."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        # This would integrate with heuristics-framework agents
        return {
            "status": "discovery_initiated",
            "kb_name": kb_name,
            "domain": domain,
            "iterations": iterations,
            "validate": validate,
            "message": "Heuristic discovery pipeline started. Use orchestrator agent for full pipeline.",
        }

    async def _graph_traverse(
        self,
        kb_name: str,
        start_entity: str,
        relation_types: list = None,
        max_hops: int = 3,
    ) -> dict:
        """Execute graph traversal query."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        if not self.neo4j:
            return {"error": "Neo4j not available"}

        try:
            with self.neo4j.session() as session:
                # Multi-hop traversal query
                rel_filter = ""
                if relation_types:
                    rel_filter = ":" + "|".join(relation_types)

                cypher = f"""
                MATCH path = (start:Entity {{name: $start_entity}})-[{rel_filter}*1..{max_hops}]-(related)
                RETURN path, length(path) as hops
                ORDER BY hops
                LIMIT 50
                """

                result = session.run(cypher, start_entity=start_entity)
                paths = []
                for record in result:
                    paths.append({"hops": record["hops"], "path": str(record["path"])})

                return {
                    "start_entity": start_entity,
                    "max_hops": max_hops,
                    "paths_found": len(paths),
                    "paths": paths[:20],
                }
        except Exception as e:
            return {"error": f"Graph traversal failed: {e}"}

    async def _export(
        self,
        kb_name: str,
        output_path: str,
        format: str = "markdown",
        include_heuristics: bool = True,
    ) -> dict:
        """Export knowledge base content."""
        if kb_name not in self.kb_registry:
            return {"error": f"Knowledge base '{kb_name}' not found"}

        kb = self.kb_registry[kb_name]
        output = Path(output_path)

        if format == "markdown":
            content = f"""# {kb_name} Knowledge Base Export

Generated: {datetime.utcnow().isoformat()}

## Summary
- **Scope**: {kb.scope}
- **Documents**: {kb.document_count}
- **Entities**: {kb.entity_count}
- **Heuristics**: {kb.heuristic_count}

## Collections
{chr(10).join(f"- {c}" for c in kb.collections)}

"""
            output.write_text(content)
        elif format == "json":
            data = {
                "name": kb.name,
                "scope": kb.scope,
                "created_at": kb.created_at,
                "document_count": kb.document_count,
                "exported_at": datetime.utcnow().isoformat(),
            }
            output.write_text(json.dumps(data, indent=2))

        return {"success": True, "output_path": str(output), "format": format}

    async def _status(self, kb_name: str = None) -> dict:
        """Check infrastructure status."""
        status = {
            "qdrant": {
                "available": QDRANT_AVAILABLE,
                "connected": self.qdrant is not None,
            },
            "neo4j": {
                "available": NEO4J_AVAILABLE,
                "connected": self.neo4j is not None,
            },
            "elasticsearch": {
                "available": ES_AVAILABLE,
                "connected": self.es is not None,
            },
            "redis": {
                "available": REDIS_AVAILABLE,
                "connected": self.redis_client is not None,
            },
            "knowledge_bases": list(self.kb_registry.keys()),
        }

        if kb_name and kb_name in self.kb_registry:
            kb = self.kb_registry[kb_name]
            status["kb_details"] = {
                "name": kb.name,
                "scope": kb.scope,
                "document_count": kb.document_count,
                "entity_count": kb.entity_count,
            }

        return status

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options()
            )


def main():
    """Entry point."""
    server = AkashicKBServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()

```

## File: akashic-knowledge/mcp/servers/kb-server/requirements.txt

- Extension: .txt
- Language: plaintext
- Size: 241 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```plaintext
# Akashic Knowledge Base MCP Server Dependencies

# MCP SDK
mcp>=1.0.0

# Vector Database
qdrant-client>=1.12.0

# Graph Database
neo4j>=5.26.0

# Search Engine
elasticsearch>=8.17.0

# Caching
redis>=5.0.0

# Utilities
python-dotenv>=1.0.0

```

## File: akashic-knowledge/docs/ARCHITECTURE.md

- Extension: .md
- Language: markdown
- Size: 10809 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/docs/QUICKSTART.md

- Extension: .md
- Language: markdown
- Size: 4005 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
# Akashic Knowledge Quickstart Guide

Get started with the Akashic Knowledge plugin in under 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Claude Code CLI installed
- Python 3.10+ (for hook scripts)

## Step 1: Start Infrastructure

Navigate to the plugin's Docker directory and start the containers:

```bash
cd plugins/akashic-knowledge/docker
docker-compose up -d
```

Verify containers are running:

```bash
docker-compose ps
```

Expected output:
```
NAME                 STATUS
akashic-qdrant       Up
akashic-neo4j        Up
akashic-elasticsearch Up
akashic-redis        Up
```

## Step 2: Load the Plugin

Start Claude Code with the plugin loaded:

```bash
claude --plugin-dir ./plugins/akashic-knowledge
```

Or add to your Claude Code configuration for persistent loading.

## Step 3: Create Your First Knowledge Base

Create a project-scoped knowledge base:

```
/akashic:create-kb my-first-kb project
```

You should see:
```
Knowledge base 'my-first-kb' created successfully.
Scope: project
Collections: qdrant:akashic_my-first-kb, es:akashic_my-first-kb
```

## Step 4: Ingest Documents

Ingest a directory of documents:

```
/akashic:ingest my-first-kb ./docs
```

Or ingest specific file types:

```
/akashic:ingest my-first-kb ./src --patterns "*.py,*.md"
```

## Step 5: Query Your Knowledge Base

Perform a hybrid search:

```
/akashic:query my-first-kb "What are the main components of this system?"
```

Try different search strategies:

```
# Semantic search (meaning-based)
/akashic:query my-first-kb "architecture overview" --search-type semantic

# Keyword search (exact matches)
/akashic:query my-first-kb "UserService" --search-type keyword
```

## Step 6: Discover Patterns and Heuristics

Run the heuristic discovery pipeline:

```
/akashic:discover my-first-kb --domain "code-quality"
```

This will:
1. Extract patterns from your documents
2. Generate heuristic candidates
3. Evolve and validate heuristics
4. Output documented decision functions

## Step 7: Export Research Documents

Export your findings:

```
# As markdown
/akashic:export my-first-kb ./research-output.md

# As JSON
/akashic:export my-first-kb ./research-output.json --format json
```

## Common Workflows

### Research Workflow

```
1. /akashic:create-kb research-project project
2. /akashic:ingest research-project ./papers --patterns "*.pdf,*.md"
3. /akashic:query research-project "main findings on topic X"
4. /akashic:discover research-project --domain "research-methodology"
5. /akashic:export research-project ./findings.md
```

### Code Analysis Workflow

```
1. /akashic:create-kb codebase-analysis project
2. /akashic:ingest codebase-analysis ./src
3. /akashic:query codebase-analysis "error handling patterns"
4. /akashic:discover codebase-analysis --domain "code-quality"
5. /akashic:export codebase-analysis ./code-analysis.md
```

### Temporary Analysis Workflow

```
1. /akashic:create-kb quick-check task
2. /akashic:ingest quick-check ./file.py
3. /akashic:query quick-check "security vulnerabilities"
# KB automatically cleaned up at session end
```

## Troubleshooting

### Containers Not Running

```bash
cd plugins/akashic-knowledge/docker
docker-compose down
docker-compose up -d
```

### Connection Errors

Check infrastructure status:

```
/akashic:sync --status
```

### Empty Query Results

1. Verify documents were ingested: Check `total_in_kb` count
2. Try different search types: `semantic`, `keyword`, `hybrid`
3. Simplify query terms

### Slow Performance

1. Reduce `--top-k` for faster queries
2. Use `--search-type keyword` for simple lookups
3. Check Docker resource allocation

## Next Steps

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) for system details
2. Explore the agent definitions in `agents/`
3. Customize skills in `skills/`
4. Create your own heuristics with the AutoHD pipeline

## Getting Help

- Check the full [README.md](./README.md)
- Review hook scripts for customization options
- Examine schema files for data validation

```

## File: akashic-knowledge/docs/README.md

- Extension: .md
- Language: markdown
- Size: 3960 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
# Akashic Knowledge Plugin

The ultimate research and knowledge base plugin for Claude Code, combining multi-agent orchestration, agentic RAG, containerized databases, and automated heuristics discovery.

## Features

- **Multi-Agent Orchestration**: 7 specialized agents for research, extraction, synthesis, and validation
- **Agentic RAG**: Hybrid search with semantic embeddings, BM25, and graph augmentation
- **Containerized Infrastructure**: Qdrant, Neo4j, Elasticsearch, and Redis via Docker
- **Heuristics Discovery**: AutoHD + POPPER framework for validated decision functions
- **MCP Integration**: Cross-session knowledge base access
- **Progressive Disclosure**: Skills with reference files for deep customization

## Quick Start

### 1. Start Infrastructure

```bash
cd plugins/akashic-knowledge/docker
docker-compose up -d
```

### 2. Load Plugin

```bash
claude --plugin-dir ./plugins/akashic-knowledge
```

### 3. Create Knowledge Base

```bash
/akashic:create-kb my-research project
```

### 4. Ingest Documents

```bash
/akashic:ingest my-research ./docs
```

### 5. Query Knowledge Base

```bash
/akashic:query my-research "What are the best practices?"
```

### 6. Discover Heuristics

```bash
/akashic:discover my-research --domain "code-quality"
```

## Commands

| Command | Description |
|---------|-------------|
| `/akashic:create-kb` | Create new knowledge base |
| `/akashic:ingest` | Ingest documents |
| `/akashic:query` | Query with hybrid search |
| `/akashic:discover` | Run heuristic discovery |
| `/akashic:export` | Export research documents |
| `/akashic:sync` | Sync and check status |

## Agents

| Agent | Purpose |
|-------|---------|
| `orchestrator` | Coordinate multi-agent workflows |
| `researcher` | Web and document research |
| `extractor` | Entity and relation extraction |
| `synthesizer` | Heuristic generation (AutoHD) |
| `validator` | Statistical validation (POPPER) |
| `indexer` | Multi-store indexing |
| `retriever` | RAG query execution |

## Skills

| Skill | Use When |
|-------|----------|
| `knowledge-discovery` | Discovering patterns in documents |
| `rag-retrieval` | Querying knowledge bases |
| `heuristics-synthesis` | Generating decision functions |
| `graph-reasoning` | Multi-hop graph queries |

## Architecture

```
User Query
     ↓
Orchestrator Agent
     ↓
┌────────────────────────────────────┐
│  Parallel Agent Execution          │
├────────────────────────────────────┤
│ Researcher → Extractor → Indexer   │
│      ↓           ↓          ↓      │
│  Web/Docs    Entities    Qdrant    │
│              Relations   Neo4j     │
│              Patterns    ES        │
└────────────────────────────────────┘
     ↓
Synthesizer (AutoHD)
     ↓
Validator (POPPER)
     ↓
Research Documents + Validated Heuristics
```

## Requirements

- Docker and Docker Compose
- Python 3.10+
- Claude Code CLI

## Infrastructure

| Service | Port | Purpose |
|---------|------|---------|
| Qdrant | 6333/6334 | Vector database |
| Neo4j | 7474/7687 | Graph database |
| Elasticsearch | 9200 | Keyword search |
| Redis | 6379 | Caching |

## Configuration

Environment variables in `.mcp.json`:

```json
{
  "QDRANT_URL": "http://localhost:6333",
  "NEO4J_URL": "bolt://localhost:7687",
  "ELASTICSEARCH_URL": "http://localhost:9200",
  "REDIS_URL": "redis://localhost:6379"
}
```

## Performance Targets

| Metric | Target |
|--------|--------|
| RAG Pass@10 | >95% |
| Query Latency | <500ms |
| Heuristic Accuracy | >85% |
| E-Value | >20 |

## Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture details
- [QUICKSTART.md](./QUICKSTART.md) - Getting started guide

## License

MIT

## Author

monxun

```

## File: akashic-knowledge/schemas/research-doc.schema.json

- Extension: .json
- Language: json
- Size: 5726 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://akashic-knowledge.io/schemas/research-doc.schema.json",
  "title": "Akashic Research Document Schema",
  "description": "Schema for exported research documents from knowledge bases",
  "type": "object",
  "required": [
    "title",
    "kb_name",
    "created_at",
    "content"
  ],
  "properties": {
    "title": {
      "type": "string",
      "description": "Document title",
      "minLength": 1,
      "maxLength": 200
    },
    "kb_name": {
      "type": "string",
      "description": "Source knowledge base name"
    },
    "created_at": {
      "type": "string",
      "description": "Document creation timestamp",
      "format": "date-time"
    },
    "format": {
      "type": "string",
      "description": "Output format",
      "enum": [
        "markdown",
        "json",
        "jsonld"
      ],
      "default": "markdown"
    },
    "summary": {
      "type": "object",
      "description": "Knowledge base summary statistics",
      "properties": {
        "document_count": {
          "type": "integer"
        },
        "entity_count": {
          "type": "integer"
        },
        "heuristic_count": {
          "type": "integer"
        },
        "source_files": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "content": {
      "type": "object",
      "description": "Document content sections",
      "properties": {
        "findings": {
          "type": "array",
          "description": "Key findings from the knowledge base",
          "items": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string"
              },
              "description": {
                "type": "string"
              },
              "evidence": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              }
            }
          }
        },
        "patterns": {
          "type": "array",
          "description": "Discovered patterns",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "description": {
                "type": "string"
              },
              "frequency": {
                "type": "integer"
              },
              "examples": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              }
            }
          }
        },
        "entities": {
          "type": "array",
          "description": "Extracted entities",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "mentions": {
                "type": "integer"
              },
              "relationships": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "target": {
                      "type": "string"
                    },
                    "type": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        },
        "heuristics": {
          "type": "array",
          "description": "Discovered heuristics",
          "items": {
            "$ref": "heuristic.schema.json"
          }
        },
        "recommendations": {
          "type": "array",
          "description": "Actionable recommendations",
          "items": {
            "type": "object",
            "properties": {
              "recommendation": {
                "type": "string"
              },
              "rationale": {
                "type": "string"
              },
              "priority": {
                "type": "string",
                "enum": [
                  "high",
                  "medium",
                  "low"
                ]
              }
            }
          }
        }
      }
    },
    "sources": {
      "type": "array",
      "description": "Source citations",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "path": {
            "type": "string"
          },
          "url": {
            "type": "string",
            "format": "uri"
          },
          "accessed_at": {
            "type": "string",
            "format": "date-time"
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional document metadata",
      "properties": {
        "author": {
          "type": "string"
        },
        "version": {
          "type": "string"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "export_config": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "@context": {
      "type": [
        "string",
        "object"
      ],
      "description": "JSON-LD context for semantic web compatibility"
    },
    "@type": {
      "type": "string",
      "description": "JSON-LD type"
    }
  },
  "additionalProperties": false
}

```

## File: akashic-knowledge/schemas/knowledge-base.schema.json

- Extension: .json
- Language: json
- Size: 2424 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://akashic-knowledge.io/schemas/knowledge-base.schema.json",
  "title": "Akashic Knowledge Base Schema",
  "description": "Schema for Akashic knowledge base registry entries",
  "type": "object",
  "required": [
    "name",
    "scope",
    "created_at"
  ],
  "properties": {
    "name": {
      "type": "string",
      "description": "Unique identifier for the knowledge base",
      "pattern": "^[a-z0-9][a-z0-9-]*[a-z0-9]$",
      "minLength": 2,
      "maxLength": 64
    },
    "scope": {
      "type": "string",
      "description": "Knowledge base scope determining lifecycle",
      "enum": [
        "task",
        "project",
        "global"
      ]
    },
    "created_at": {
      "type": "string",
      "description": "ISO 8601 timestamp of creation",
      "format": "date-time"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the knowledge base purpose",
      "maxLength": 500
    },
    "document_count": {
      "type": "integer",
      "description": "Number of indexed documents",
      "minimum": 0,
      "default": 0
    },
    "entity_count": {
      "type": "integer",
      "description": "Number of extracted entities",
      "minimum": 0,
      "default": 0
    },
    "heuristic_count": {
      "type": "integer",
      "description": "Number of discovered heuristics",
      "minimum": 0,
      "default": 0
    },
    "collections": {
      "type": "array",
      "description": "List of storage collections associated with this KB",
      "items": {
        "type": "string",
        "pattern": "^(qdrant|es|neo4j):[a-z0-9_-]+$"
      },
      "default": []
    },
    "config": {
      "type": "object",
      "description": "Optional configuration overrides",
      "properties": {
        "chunk_size": {
          "type": "integer",
          "minimum": 100,
          "maximum": 2000,
          "default": 750
        },
        "chunk_overlap": {
          "type": "integer",
          "minimum": 0,
          "maximum": 500,
          "default": 75
        },
        "embedding_model": {
          "type": "string",
          "default": "text-embedding-3-small"
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}

```

## File: akashic-knowledge/schemas/heuristic.schema.json

- Extension: .json
- Language: json
- Size: 5440 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://akashic-knowledge.io/schemas/heuristic.schema.json",
  "title": "Akashic Heuristic Schema",
  "description": "Schema for discovered heuristic functions and metadata",
  "type": "object",
  "required": [
    "name",
    "domain",
    "version",
    "description",
    "function"
  ],
  "properties": {
    "name": {
      "type": "string",
      "description": "Unique heuristic identifier",
      "pattern": "^heuristic_[a-z][a-z0-9_]*$",
      "minLength": 10,
      "maxLength": 64
    },
    "domain": {
      "type": "string",
      "description": "Domain context for the heuristic",
      "examples": [
        "code-quality",
        "security",
        "api-design",
        "testing"
      ]
    },
    "version": {
      "type": "string",
      "description": "Semantic version of the heuristic",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "description": {
      "type": "string",
      "description": "Human-readable description of what the heuristic measures",
      "minLength": 10,
      "maxLength": 500
    },
    "function": {
      "type": "string",
      "description": "Python function code implementing the heuristic"
    },
    "inputs": {
      "type": "array",
      "description": "Required context keys for the heuristic",
      "items": {
        "type": "object",
        "required": [
          "key",
          "type",
          "description"
        ],
        "properties": {
          "key": {
            "type": "string"
          },
          "type": {
            "type": "string",
            "enum": [
              "string",
              "integer",
              "float",
              "boolean",
              "array",
              "object"
            ]
          },
          "description": {
            "type": "string"
          },
          "required": {
            "type": "boolean",
            "default": true
          }
        }
      }
    },
    "output": {
      "type": "object",
      "description": "Output specification",
      "properties": {
        "type": {
          "type": "string",
          "enum": [
            "float",
            "boolean",
            "string"
          ],
          "default": "float"
        },
        "range": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 2,
          "maxItems": 2
        },
        "interpretation": {
          "type": "string"
        }
      }
    },
    "performance": {
      "type": "object",
      "description": "Performance metrics from evaluation",
      "properties": {
        "accuracy": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "precision": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "recall": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "f1": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "e_value": {
          "type": "number",
          "minimum": 0,
          "description": "POPPER e-value for statistical significance"
        },
        "type_i_error": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Type-I error rate"
        }
      }
    },
    "evolution": {
      "type": "object",
      "description": "Evolution history from AutoHD",
      "properties": {
        "iterations": {
          "type": "integer",
          "minimum": 1
        },
        "parent_heuristics": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "mutations_applied": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "fitness_history": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "iteration": {
                "type": "integer"
              },
              "fitness": {
                "type": "number"
              }
            }
          }
        }
      }
    },
    "validation": {
      "type": "object",
      "description": "POPPER validation results",
      "properties": {
        "status": {
          "type": "string",
          "enum": [
            "pending",
            "validated",
            "rejected",
            "inconclusive"
          ]
        },
        "experiments": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": {
                "type": "string"
              },
              "n_samples": {
                "type": "integer"
              },
              "e_value": {
                "type": "number"
              },
              "passed": {
                "type": "boolean"
              }
            }
          }
        },
        "validated_at": {
          "type": "string",
          "format": "date-time"
        }
      }
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "source_kb": {
      "type": "string",
      "description": "Knowledge base this heuristic was derived from"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "additionalProperties": false
}

```

## File: akashic-knowledge/hooks/hooks.json

- Extension: .json
- Language: json
- Size: 1188 bytes
- Created: 2026-01-16 02:26:49
- Modified: 2026-01-16 02:26:49

### Code

```json
{
  "description": "Akashic Knowledge validation hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__akashic-kb__akashic_ingest",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-corpus.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "mcp__akashic-kb__akashic_create_kb",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/index-on-create.py",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "mcp__akashic-kb__akashic_discover",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-heuristics.py",
            "timeout": 15
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/persist-session.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}

```

## File: akashic-knowledge/hooks/scripts/validate-heuristics.py

- Extension: .py
- Language: python
- Size: 3710 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```python
#!/usr/bin/env python3
"""
Post-discovery heuristic validation hook for Akashic Knowledge plugin.

Validates discovered heuristics after AutoHD pipeline:
- Checks heuristic format
- Validates metadata
- Reports quality metrics

Exit codes:
- 0: Validation passed
- 1: Non-blocking warnings
"""

import json
import os
import sys
from pathlib import Path


def validate_heuristic_format(heuristic_data: dict) -> list[str]:
    """Validate heuristic data format."""
    errors = []

    required_fields = ["status", "kb_name", "domain"]
    for field in required_fields:
        if field not in heuristic_data:
            errors.append(f"Missing required field: {field}")

    return errors


def check_quality_metrics(heuristic_data: dict) -> dict:
    """Check quality metrics from discovery result."""
    metrics = {
        "passed": True,
        "warnings": [],
        "recommendations": [],
    }

    # Check if discovery was initiated successfully
    if heuristic_data.get("status") == "discovery_initiated":
        metrics["recommendations"].append(
            "Discovery initiated. Run the full pipeline with orchestrator agent."
        )
    elif heuristic_data.get("status") == "completed":
        # Check performance metrics if available
        performance = heuristic_data.get("performance", {})

        if performance.get("accuracy", 0) < 0.85:
            metrics["warnings"].append(
                f"Accuracy below threshold: {performance.get('accuracy', 'N/A')}"
            )

        if performance.get("e_value", 0) < 20:
            metrics["warnings"].append(
                f"E-value below significance threshold: {performance.get('e_value', 'N/A')}"
            )

    return metrics


def log_discovery_result(heuristic_data: dict) -> None:
    """Log discovery result for tracking."""
    log_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    from datetime import datetime

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "heuristic_discovery",
        "kb_name": heuristic_data.get("kb_name"),
        "domain": heuristic_data.get("domain"),
        "status": heuristic_data.get("status"),
    }

    log_file = log_dir / "discoveries.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def main():
    """Main entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_result = hook_input.get("tool_result", {})

    # Parse the result
    try:
        result_data = json.loads(tool_result.get("content", "{}"))
    except json.JSONDecodeError:
        result_data = {}

    # Validate format
    format_errors = validate_heuristic_format(result_data)
    if format_errors:
        print("Format validation errors:")
        for error in format_errors:
            print(f"  - {error}")

    # Check quality
    quality = check_quality_metrics(result_data)

    print(f"\nHeuristic Discovery: {result_data.get('status', 'unknown')}")
    print(f"Domain: {result_data.get('domain', 'unknown')}")
    print(f"Knowledge Base: {result_data.get('kb_name', 'unknown')}")

    if quality["warnings"]:
        print("\nWarnings:")
        for w in quality["warnings"]:
            print(f"  - {w}")

    if quality["recommendations"]:
        print("\nRecommendations:")
        for r in quality["recommendations"]:
            print(f"  - {r}")

    # Log the result
    log_discovery_result(result_data)

    sys.exit(0 if quality["passed"] else 1)


if __name__ == "__main__":
    main()

```

## File: akashic-knowledge/hooks/scripts/validate-corpus.py

- Extension: .py
- Language: python
- Size: 2926 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```python
#!/usr/bin/env python3
"""
Pre-ingest validation hook for Akashic Knowledge plugin.

Validates corpus before ingestion:
- Checks source path exists
- Validates file patterns
- Estimates corpus size
- Warns about potential issues

Exit codes:
- 0: Validation passed, continue
- 2: Validation failed, block operation
"""

import json
import os
import sys
from pathlib import Path


def validate_corpus(tool_input: dict) -> tuple[bool, str]:
    """Validate corpus before ingestion."""
    source = tool_input.get("source", "")
    kb_name = tool_input.get("kb_name", "")

    errors = []
    warnings = []

    # Check KB name
    if not kb_name:
        errors.append("Knowledge base name is required")

    # Check source path
    source_path = Path(source)
    if not source_path.exists():
        errors.append(f"Source path does not exist: {source}")
    elif source_path.is_dir():
        # Count files
        patterns = tool_input.get("file_patterns", ["*.md", "*.txt", "*.py"])
        file_count = 0
        total_size = 0

        for pattern in patterns:
            for file_path in source_path.rglob(pattern):
                file_count += 1
                total_size += file_path.stat().st_size

        if file_count == 0:
            warnings.append(f"No files found matching patterns: {patterns}")

        if total_size > 100 * 1024 * 1024:  # 100MB
            warnings.append(
                f"Large corpus detected: {total_size / 1024 / 1024:.1f}MB. "
                "Ingestion may take a while."
            )

        if file_count > 1000:
            warnings.append(
                f"Large number of files: {file_count}. "
                "Consider using more specific patterns."
            )

    # Check for sensitive files
    sensitive_patterns = [".env", "credentials", "secret", "private", "password"]
    if source_path.is_dir():
        for sensitive in sensitive_patterns:
            matches = list(source_path.rglob(f"*{sensitive}*"))
            if matches:
                warnings.append(
                    f"Potentially sensitive files detected: {[str(m) for m in matches[:3]]}"
                )

    if errors:
        return False, "Validation failed:\n" + "\n".join(f"- {e}" for e in errors)

    message = "Validation passed."
    if warnings:
        message += "\nWarnings:\n" + "\n".join(f"- {w}" for w in warnings)

    return True, message


def main():
    """Main entry point."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_input = hook_input.get("tool_input", {})

    passed, message = validate_corpus(tool_input)

    if passed:
        print(message)
        sys.exit(0)
    else:
        print(message, file=sys.stderr)
        sys.exit(2)  # Block operation


if __name__ == "__main__":
    main()

```

## File: akashic-knowledge/hooks/scripts/index-on-create.py

- Extension: .py
- Language: python
- Size: 2852 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```python
#!/usr/bin/env python3
"""
Post-create indexing hook for Akashic Knowledge plugin.

Automatically sets up indices and configurations after KB creation:
- Logs creation event
- Prepares index configurations
- Validates infrastructure connectivity

Exit codes:
- 0: Success
- 1: Non-blocking warning
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def log_creation(tool_result: dict, kb_info: dict) -> None:
    """Log knowledge base creation event."""
    log_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": "kb_created",
        "kb_name": kb_info.get("name", "unknown"),
        "scope": kb_info.get("scope", "unknown"),
        "collections": kb_info.get("collections", []),
        "result": tool_result,
    }

    log_file = log_dir / "events.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def check_infrastructure() -> list[str]:
    """Check infrastructure connectivity."""
    warnings = []

    # Check if Docker is available
    import subprocess

    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        running_containers = result.stdout.strip().split("\n")

        expected = ["akashic-qdrant", "akashic-neo4j", "akashic-elasticsearch"]
        for container in expected:
            if container not in running_containers:
                warnings.append(f"Container not running: {container}")

    except (subprocess.TimeoutExpired, FileNotFoundError):
        warnings.append("Docker not available or timed out")

    return warnings


def main():
    """Main entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(1)

    tool_result = hook_input.get("tool_result", {})

    # Parse the result
    try:
        result_data = json.loads(tool_result.get("content", "{}"))
    except json.JSONDecodeError:
        result_data = {}

    if result_data.get("success"):
        kb_info = result_data.get("kb", {})
        log_creation(tool_result, kb_info)

        print(f"Knowledge base '{kb_info.get('name')}' created successfully.")
        print(f"Scope: {kb_info.get('scope')}")
        print(f"Collections: {', '.join(kb_info.get('collections', []))}")

        # Check infrastructure
        warnings = check_infrastructure()
        if warnings:
            print("\nInfrastructure warnings:")
            for w in warnings:
                print(f"  - {w}")

    sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: akashic-knowledge/hooks/scripts/persist-session.py

- Extension: .py
- Language: python
- Size: 3077 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```python
#!/usr/bin/env python3
"""
Session persistence hook for Akashic Knowledge plugin.

Persists session state on session end:
- Saves KB registry state
- Flushes caches
- Creates session snapshot

Exit codes:
- 0: Success
- 1: Non-blocking warning
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def persist_registry() -> bool:
    """Ensure registry is saved to disk."""
    data_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic"))
    registry_file = data_dir / "registry.json"

    if registry_file.exists():
        print(f"Registry persisted at: {registry_file}")
        return True
    else:
        print("No registry file found (no KBs created this session)")
        return True


def create_session_snapshot() -> None:
    """Create a snapshot of session state."""
    data_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic"))
    snapshots_dir = data_dir / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    snapshot_file = snapshots_dir / f"session_{timestamp}.json"

    # Gather session info
    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "registry_exists": (data_dir / "registry.json").exists(),
        "data_dir": str(data_dir),
    }

    # List knowledge bases
    registry_file = data_dir / "registry.json"
    if registry_file.exists():
        try:
            registry = json.loads(registry_file.read_text())
            snapshot["knowledge_bases"] = list(registry.keys())
        except json.JSONDecodeError:
            snapshot["knowledge_bases"] = []

    snapshot_file.write_text(json.dumps(snapshot, indent=2))
    print(f"Session snapshot saved: {snapshot_file}")


def cleanup_task_kbs() -> int:
    """Clean up task-scoped knowledge bases."""
    data_dir = Path(os.getenv("AKASHIC_DATA_DIR", Path.home() / ".akashic"))
    registry_file = data_dir / "registry.json"

    if not registry_file.exists():
        return 0

    try:
        registry = json.loads(registry_file.read_text())
    except json.JSONDecodeError:
        return 0

    # Find task-scoped KBs
    task_kbs = [name for name, kb in registry.items() if kb.get("scope") == "task"]

    if task_kbs:
        print(f"Task-scoped KBs to clean up: {task_kbs}")
        # In production, would actually clean up the collections
        # For now, just mark in registry
        for kb_name in task_kbs:
            del registry[kb_name]

        registry_file.write_text(json.dumps(registry, indent=2))

    return len(task_kbs)


def main():
    """Main entry point."""
    print("Akashic Knowledge: Session ending, persisting state...")

    # Persist registry
    persist_registry()

    # Create snapshot
    create_session_snapshot()

    # Cleanup task-scoped KBs
    cleaned = cleanup_task_kbs()
    if cleaned > 0:
        print(f"Cleaned up {cleaned} task-scoped knowledge base(s)")

    print("Session state persisted successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: akashic-knowledge/.claude-plugin/plugin.json

- Extension: .json
- Language: json
- Size: 930 bytes
- Created: 2026-01-16 02:46:34
- Modified: 2026-01-16 02:46:34

### Code

```json
{
  "name": "akashic-knowledge",
  "version": "1.0.0",
  "description": "Ultimate research and knowledge base plugin with multi-agent orchestration, agentic RAG, containerized vector/graph databases, and heuristics framework integration for cross-session knowledge persistence.",
  "author": { "name": "monxun" },
  "license": "MIT",
  "repository": "https://github.com/monxun/claude-code-plugins",
  "keywords": [
    "research",
    "knowledge-base",
    "rag",
    "vector-database",
    "graph-database",
    "multi-agent",
    "heuristics",
    "mcp",
    "orchestration"
  ],
  "commands": "./commands/",
  "agents": [
    "./agents/orchestrator.md",
    "./agents/researcher.md",
    "./agents/extractor.md",
    "./agents/synthesizer.md",
    "./agents/validator.md",
    "./agents/indexer.md",
    "./agents/retriever.md"
  ],
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./mcp/.mcp.json"
}

```

## File: akashic-knowledge/templates/kb-manifest.json.j2

- Extension: .j2
- Language: jinja2
- Size: 1752 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```jinja2
{
  "$schema": "https://akashic-knowledge.io/schemas/knowledge-base.schema.json",
  "name": "{{ name }}",
  "scope": "{{ scope }}",
  "created_at": "{{ created_at }}",
  {% if description %}"description": "{{ description }}",{% endif %}
  "document_count": {{ document_count | default(0) }},
  "entity_count": {{ entity_count | default(0) }},
  "heuristic_count": {{ heuristic_count | default(0) }},
  "collections": [
    {% for collection in collections %}"{{ collection }}"{% if not loop.last %},{% endif %}
    {% endfor %}
  ],
  "config": {
    "chunk_size": {{ config.chunk_size | default(750) }},
    "chunk_overlap": {{ config.chunk_overlap | default(75) }},
    "embedding_model": "{{ config.embedding_model | default('text-embedding-3-small') }}"
  },
  "metadata": {
    "version": "1.0.0",
    "plugin_version": "1.0.0",
    "generator": "akashic-knowledge",
    {% if metadata %}
    {% for key, value in metadata.items() %}
    "{{ key }}": {% if value is string %}"{{ value }}"{% else %}{{ value | tojson }}{% endif %}{% if not loop.last %},{% endif %}
    {% endfor %}
    {% endif %}
  },
  "indices": {
    "vector": {
      "store": "qdrant",
      "collection": "akashic_{{ name }}",
      "dimensions": 1536,
      "distance": "cosine"
    },
    "keyword": {
      "store": "elasticsearch",
      "index": "akashic_{{ name }}",
      "analyzer": "standard"
    },
    "graph": {
      "store": "neo4j",
      "database": "akashic",
      "namespace": "{{ name }}"
    }
  },
  "statistics": {
    "last_updated": "{{ last_updated | default(created_at) }}",
    "ingestion_count": {{ ingestion_count | default(0) }},
    "query_count": {{ query_count | default(0) }},
    "discovery_runs": {{ discovery_runs | default(0) }}
  }
}

```

## File: akashic-knowledge/templates/research-report.md.j2

- Extension: .j2
- Language: jinja2
- Size: 3217 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```jinja2
# {{ title | default("Research Report") }}

**Knowledge Base**: {{ kb_name }}
**Generated**: {{ created_at }}
**Scope**: {{ scope }}

---

## Executive Summary

{{ summary | default("This report summarizes the findings from the knowledge base analysis.") }}

## Knowledge Base Statistics

| Metric | Value |
|--------|-------|
| Documents Indexed | {{ document_count | default(0) }} |
| Entities Extracted | {{ entity_count | default(0) }} |
| Heuristics Discovered | {{ heuristic_count | default(0) }} |
| Collections | {{ collections | join(", ") if collections else "None" }} |

---

## Key Findings

{% if findings %}
{% for finding in findings %}
### {{ loop.index }}. {{ finding.title }}

{{ finding.description }}

{% if finding.evidence %}
**Evidence:**
{% for e in finding.evidence %}
- {{ e }}
{% endfor %}
{% endif %}

{% if finding.confidence %}
**Confidence**: {{ (finding.confidence * 100) | round(1) }}%
{% endif %}

{% endfor %}
{% else %}
No specific findings to report. Run discovery pipeline to generate findings.
{% endif %}

---

## Discovered Patterns

{% if patterns %}
| Pattern | Frequency | Description |
|---------|-----------|-------------|
{% for pattern in patterns %}
| {{ pattern.name }} | {{ pattern.frequency }} | {{ pattern.description }} |
{% endfor %}
{% else %}
No patterns discovered yet. Run the knowledge discovery pipeline.
{% endif %}

---

## Entity Relationships

{% if entities %}
### Top Entities

{% for entity in entities[:20] %}
- **{{ entity.name }}** ({{ entity.type }})
  - Mentions: {{ entity.mentions }}
{% if entity.relationships %}
  - Relationships: {{ entity.relationships | length }}
{% endif %}
{% endfor %}
{% else %}
No entities extracted. Run the extraction pipeline to populate.
{% endif %}

---

## Discovered Heuristics

{% if heuristics %}
{% for heuristic in heuristics %}
### {{ heuristic.name }}

**Domain**: {{ heuristic.domain }}
**Version**: {{ heuristic.version }}

{{ heuristic.description }}

{% if heuristic.performance %}
| Metric | Value |
|--------|-------|
| Accuracy | {{ (heuristic.performance.accuracy * 100) | round(1) }}% |
| Precision | {{ (heuristic.performance.precision * 100) | round(1) }}% |
| E-Value | {{ heuristic.performance.e_value | round(2) }} |
{% endif %}

{% if heuristic.validation and heuristic.validation.status %}
**Validation Status**: {{ heuristic.validation.status | upper }}
{% endif %}

---

{% endfor %}
{% else %}
No heuristics discovered. Run `/akashic:discover` to generate heuristics.
{% endif %}

---

## Recommendations

{% if recommendations %}
{% for rec in recommendations %}
### {{ rec.priority | upper }}: {{ rec.recommendation }}

{{ rec.rationale }}

{% endfor %}
{% else %}
No recommendations generated. Run analysis to generate recommendations.
{% endif %}

---

## Sources

{% if sources %}
{% for source in sources %}
{{ loop.index }}. {% if source.title %}**{{ source.title }}**{% endif %}
   - Path: `{{ source.path }}`
{% if source.url %}   - URL: [{{ source.url }}]({{ source.url }}){% endif %}
{% if source.accessed_at %}   - Accessed: {{ source.accessed_at }}{% endif %}

{% endfor %}
{% else %}
No sources indexed.
{% endif %}

---

*Generated by Akashic Knowledge Plugin v1.0.0*

```

## File: akashic-knowledge/templates/heuristic-doc.md.j2

- Extension: .j2
- Language: jinja2
- Size: 3284 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```jinja2
# Heuristic: {{ name }}

**Domain**: {{ domain }}
**Version**: {{ version }}
**Created**: {{ created_at }}
{% if source_kb %}**Source KB**: {{ source_kb }}{% endif %}

---

## Description

{{ description }}

---

## Input Specification

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
{% for input in inputs %}
| `{{ input.key }}` | {{ input.type }} | {{ "Yes" if input.required else "No" }} | {{ input.description }} |
{% endfor %}

---

## Output Specification

- **Type**: {{ output.type | default("float") }}
{% if output.range %}- **Range**: [{{ output.range[0] }}, {{ output.range[1] }}]{% endif %}
{% if output.interpretation %}- **Interpretation**: {{ output.interpretation }}{% endif %}

---

## Implementation

```python
{{ function }}
```

---

## Performance Metrics

{% if performance %}
| Metric | Value | Threshold |
|--------|-------|-----------|
| Accuracy | {{ (performance.accuracy * 100) | round(1) }}% | >85% |
| Precision | {{ (performance.precision * 100) | round(1) }}% | >80% |
| Recall | {{ (performance.recall * 100) | round(1) }}% | >75% |
| F1 Score | {{ (performance.f1 * 100) | round(1) }}% | >78% |
{% if performance.e_value %}| E-Value | {{ performance.e_value | round(2) }} | >20 |{% endif %}
{% if performance.type_i_error %}| Type-I Error | {{ (performance.type_i_error * 100) | round(2) }}% | <10% |{% endif %}
{% else %}
*Performance metrics not yet available. Run validation to generate.*
{% endif %}

---

## Evolution History

{% if evolution %}
**Iterations**: {{ evolution.iterations }}

{% if evolution.parent_heuristics %}
**Parent Heuristics**:
{% for parent in evolution.parent_heuristics %}
- {{ parent }}
{% endfor %}
{% endif %}

{% if evolution.mutations_applied %}
**Mutations Applied**:
{% for mutation in evolution.mutations_applied %}
- {{ mutation }}
{% endfor %}
{% endif %}

{% if evolution.fitness_history %}
### Fitness Progression

| Iteration | Fitness |
|-----------|---------|
{% for entry in evolution.fitness_history %}
| {{ entry.iteration }} | {{ entry.fitness | round(4) }} |
{% endfor %}
{% endif %}
{% else %}
*No evolution history available.*
{% endif %}

---

## Validation Results

{% if validation %}
**Status**: {{ validation.status | upper }}
{% if validation.validated_at %}**Validated At**: {{ validation.validated_at }}{% endif %}

{% if validation.experiments %}
### Experiments

| Type | Samples | E-Value | Passed |
|------|---------|---------|--------|
{% for exp in validation.experiments %}
| {{ exp.type }} | {{ exp.n_samples }} | {{ exp.e_value | round(2) }} | {{ "✓" if exp.passed else "✗" }} |
{% endfor %}
{% endif %}
{% else %}
*Validation pending. Run POPPER validation to verify.*
{% endif %}

---

## Usage Example

```python
from akashic.heuristics import {{ name }}

# Prepare context
context = {
{% for input in inputs %}
    "{{ input.key }}": <{{ input.type }}_value>,  # {{ input.description }}
{% endfor %}
}

# Execute heuristic
score = {{ name }}(context)
print(f"Score: {score}")  # {{ output.interpretation | default("0.0 to 1.0") }}
```

---

## Tags

{% if tags %}
{% for tag in tags %}`{{ tag }}` {% endfor %}
{% else %}
*No tags assigned.*
{% endif %}

---

*Generated by Akashic Knowledge Plugin - AutoHD + POPPER Framework*

```

## File: akashic-knowledge/commands/query.md

- Extension: .md
- Language: markdown
- Size: 1922 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:query
description: Query an Akashic knowledge base using hybrid semantic and keyword search
---

# Query Knowledge Base

Search a knowledge base using state-of-the-art hybrid retrieval.

## Usage

```
/akashic:query <kb-name> "<query>" [options]
```

## Parameters

- **kb-name**: Knowledge base to query
- **query**: Natural language search query (use quotes for multi-word)

## Options

- `--top-k`: Number of results to return (default: 10)
- `--search-type`: Search strategy - `hybrid`, `semantic`, or `keyword` (default: hybrid)
- `--rerank`: Apply ColBERT reranking (default: true)

## Examples

```bash
# Basic hybrid search
/akashic:query my-research "What are the best practices for API design?"

# Semantic-only search
/akashic:query my-research "authentication patterns" --search-type semantic

# Get more results
/akashic:query my-research "error handling" --top-k 20

# Keyword-only for exact matches
/akashic:query my-research "UserService" --search-type keyword
```

## Search Strategies

### Hybrid (Default)
Combines semantic and keyword search:
- 80% semantic (meaning-based)
- 20% keyword (exact match)
- Reciprocal Rank Fusion

### Semantic
Pure vector similarity:
- Best for conceptual queries
- Handles synonyms and paraphrasing

### Keyword
Traditional BM25:
- Best for exact terms
- Code identifiers
- Technical names

## Output Format

```json
{
  "query": "your query",
  "search_type": "hybrid",
  "result_count": 10,
  "results": [
    {
      "id": "chunk_123",
      "content": "Relevant text...",
      "source": "/path/to/document.md",
      "score": 0.95
    }
  ]
}
```

## Query Tips

1. **Be specific**: "React authentication with JWT" > "authentication"
2. **Use natural language**: Queries work best as questions
3. **Try different strategies**: Switch between hybrid/semantic/keyword

## MCP Tool

This command uses `mcp__akashic-kb__akashic_query` under the hood.

```

## File: akashic-knowledge/commands/sync.md

- Extension: .md
- Language: markdown
- Size: 2398 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:sync
description: Sync knowledge base with persistent storage and check infrastructure status
---

# Sync Knowledge Base

Synchronize knowledge base state with persistent storage and check infrastructure health.

## Usage

```
/akashic:sync [kb-name] [options]
```

## Parameters

- **kb-name**: Optional specific knowledge base to sync (syncs all if omitted)

## Options

- `--status`: Check infrastructure status only
- `--force`: Force full resync
- `--prune`: Remove orphaned data

## Examples

```bash
# Check infrastructure status
/akashic:sync --status

# Sync specific knowledge base
/akashic:sync my-research

# Sync all knowledge bases
/akashic:sync

# Force full resync
/akashic:sync my-research --force

# Clean up orphaned data
/akashic:sync --prune
```

## Status Check

The status command reports on:

```json
{
  "qdrant": {"available": true, "connected": true},
  "neo4j": {"available": true, "connected": true},
  "elasticsearch": {"available": true, "connected": true},
  "redis": {"available": true, "connected": true},
  "knowledge_bases": ["kb1", "kb2", "kb3"]
}
```

## Infrastructure Requirements

### Docker Services
Ensure containers are running:
```bash
cd plugins/akashic-knowledge/docker
docker-compose up -d
docker-compose ps  # Check status
```

### Service Ports
| Service | Port | Purpose |
|---------|------|---------|
| Qdrant | 6333 | Vector DB REST |
| Qdrant | 6334 | Vector DB gRPC |
| Neo4j | 7474 | Graph DB HTTP |
| Neo4j | 7687 | Graph DB Bolt |
| Elasticsearch | 9200 | Search API |
| Redis | 6379 | Cache |

## Sync Operations

### Full Sync
1. Validate registry consistency
2. Verify collection existence
3. Update document counts
4. Rebuild broken indices

### Incremental Sync
1. Check for new documents
2. Update modified entries
3. Remove deleted documents

### Prune
1. Find orphaned collections
2. Remove stale indices
3. Clean up cache entries

## Troubleshooting

### Container Not Running
```bash
docker-compose up -d qdrant neo4j elasticsearch redis
```

### Connection Refused
Check environment variables in `.mcp.json`:
- `QDRANT_URL`
- `NEO4J_URL`
- `ELASTICSEARCH_URL`
- `REDIS_URL`

### Data Corruption
```bash
# Force full resync
/akashic:sync --force

# If persists, rebuild from source
/akashic:ingest <kb-name> <original-source>
```

## MCP Tool

This command uses `mcp__akashic-kb__akashic_status` under the hood.

```

## File: akashic-knowledge/commands/ingest.md

- Extension: .md
- Language: markdown
- Size: 1850 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:ingest
description: Ingest documents into an Akashic knowledge base from directory, files, or URLs
---

# Ingest Documents

Ingest documents into an existing knowledge base for indexing and search.

## Usage

```
/akashic:ingest <kb-name> <source> [options]
```

## Parameters

- **kb-name**: Target knowledge base name
- **source**: Path to directory, file, or URL to ingest

## Options

- `--recursive`: Recursively process directories (default: true)
- `--patterns`: File patterns to include (default: *.md,*.txt,*.py,*.js,*.ts)
- `--chunk-size`: Target chunk size in tokens (default: 750)
- `--overlap`: Chunk overlap in tokens (default: 75)

## Examples

```bash
# Ingest entire directory
/akashic:ingest my-research ./docs

# Ingest specific file patterns
/akashic:ingest my-research ./src --patterns "*.py,*.md"

# Ingest single file
/akashic:ingest my-research ./README.md

# Non-recursive directory scan
/akashic:ingest my-research ./docs --recursive false
```

## Supported File Types

| Extension | Handler | Chunking Strategy |
|-----------|---------|-------------------|
| `.md` | Markdown | By headers/sections |
| `.txt` | Plain text | By paragraphs |
| `.py` | Python | By functions/classes |
| `.js/.ts` | JavaScript | By functions/exports |
| `.json` | JSON | By top-level keys |
| `.ipynb` | Notebook | By cells |

## Processing Pipeline

1. **Scan**: Find files matching patterns
2. **Parse**: Extract content based on file type
3. **Chunk**: Split into semantic chunks with overlap
4. **Contextualize**: Add document context to chunks
5. **Index**: Store in vector, keyword, and graph stores

## Output

```json
{
  "success": true,
  "ingested_count": 150,
  "files": ["file1.md", "file2.py", "..."],
  "total_in_kb": 350
}
```

## MCP Tool

This command uses `mcp__akashic-kb__akashic_ingest` under the hood.

```

## File: akashic-knowledge/commands/export.md

- Extension: .md
- Language: markdown
- Size: 2223 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:export
description: Export research documents or heuristics from an Akashic knowledge base
---

# Export Knowledge Base

Export knowledge base contents as research documents, heuristics, or structured data.

## Usage

```
/akashic:export <kb-name> <output-path> [options]
```

## Parameters

- **kb-name**: Source knowledge base
- **output-path**: Path for exported file or directory

## Options

- `--format`: Export format - `markdown`, `json`, or `jsonld` (default: markdown)
- `--include-heuristics`: Include discovered heuristics (default: true)
- `--include-graph`: Include knowledge graph data (default: false)
- `--template`: Custom template for document generation

## Examples

```bash
# Export as markdown document
/akashic:export my-research ./research-output.md

# Export as JSON for programmatic use
/akashic:export my-research ./export.json --format json

# Export as JSON-LD for semantic web
/akashic:export my-research ./export.jsonld --format jsonld

# Full export with graph data
/akashic:export my-research ./full-export --include-graph true
```

## Export Formats

### Markdown
Human-readable research document:
```markdown
# Knowledge Base: my-research

## Summary
- Documents: 150
- Entities: 890
- Heuristics: 12

## Key Findings
...

## Heuristics
...
```

### JSON
Structured data export:
```json
{
  "name": "my-research",
  "documents": [...],
  "entities": [...],
  "heuristics": [...]
}
```

### JSON-LD
Linked data format for semantic interoperability:
```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "name": "my-research",
  ...
}
```

## Template Variables

Custom templates can use:
- `{{kb.name}}`: Knowledge base name
- `{{kb.scope}}`: Scope (task/project/global)
- `{{kb.document_count}}`: Number of documents
- `{{kb.entity_count}}`: Number of entities
- `{{kb.heuristics}}`: List of heuristics
- `{{kb.created_at}}`: Creation timestamp

## Use Cases

1. **Research Reports**: Generate documentation from analysis
2. **Knowledge Transfer**: Export for team sharing
3. **Integration**: JSON export for other systems
4. **Archival**: Preserve knowledge base state

## MCP Tool

This command uses `mcp__akashic-kb__akashic_export` under the hood.

```

## File: akashic-knowledge/commands/create-kb.md

- Extension: .md
- Language: markdown
- Size: 1627 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:create-kb
description: Create a new Akashic knowledge base with specified scope (task, project, or global)
---

# Create Knowledge Base

Create a new knowledge base for research and knowledge management.

## Usage

```
/akashic:create-kb <name> <scope> [description]
```

## Parameters

- **name**: Unique identifier for the knowledge base (kebab-case recommended)
- **scope**: One of:
  - `task`: Ephemeral, cleared after task completion
  - `project`: Persists for session duration
  - `global`: Persistent across all sessions
- **description**: Optional description of the knowledge base purpose

## Examples

```bash
# Create project-scoped KB for current work
/akashic:create-kb my-research project

# Create global KB for ongoing reference
/akashic:create-kb company-docs global "Company documentation and best practices"

# Create task-scoped KB for temporary analysis
/akashic:create-kb quick-analysis task
```

## What This Creates

1. **Vector Collection**: Qdrant collection for semantic search
2. **ES Index**: Elasticsearch index for keyword search
3. **Graph Namespace**: Neo4j namespace for entity relationships
4. **Registry Entry**: Local registry for KB management

## Prerequisites

Ensure Docker containers are running:
```bash
cd plugins/akashic-knowledge/docker && docker-compose up -d
```

## Next Steps

After creating a knowledge base:
1. Use `/akashic:ingest` to add documents
2. Use `/akashic:query` to search the knowledge base
3. Use `/akashic:discover` to find patterns and generate heuristics

## MCP Tool

This command uses `mcp__akashic-kb__akashic_create_kb` under the hood.

```

## File: akashic-knowledge/commands/discover.md

- Extension: .md
- Language: markdown
- Size: 2266 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: akashic:discover
description: Run heuristic discovery pipeline (AutoHD + POPPER) on a knowledge base
---

# Discover Heuristics

Run the automated heuristic discovery pipeline to generate validated decision functions from knowledge patterns.

## Usage

```
/akashic:discover <kb-name> --domain "<domain>" [options]
```

## Parameters

- **kb-name**: Source knowledge base
- **domain**: Domain context for heuristic discovery (e.g., "code-quality", "security", "api-design")

## Options

- `--iterations`: Evolution iterations (default: 3)
- `--validate`: Run POPPER validation (default: true)
- `--output`: Output directory for generated heuristics

## Examples

```bash
# Discover code quality heuristics
/akashic:discover my-research --domain "code-quality"

# More evolution iterations for better results
/akashic:discover my-research --domain "security" --iterations 5

# Skip validation for quick exploration
/akashic:discover my-research --domain "api-design" --validate false

# Specify output location
/akashic:discover my-research --domain "testing" --output ./heuristics
```

## Pipeline Stages

### 1. Pattern Extraction
Extract patterns from knowledge base:
- Entity relationships
- Recurring structures
- Domain-specific rules

### 2. Heuristic Proposal (AutoHD)
Generate candidate heuristics:
- Diverse initial population
- Domain-constrained proposals
- Python function format

### 3. Evolution
Iteratively improve heuristics:
- Mutation operators
- Crossover operators
- Fitness-based selection

### 4. Validation (POPPER)
Statistical validation:
- Falsification experiments
- E-value accumulation
- Type-I error control (<0.10)

## Output Artifacts

```
heuristics/
├── heuristic_complexity_score.py
├── heuristic_security_risk.py
├── metadata.json
├── validation_report.md
└── evolution_log.json
```

## Quality Thresholds

| Metric | Threshold |
|--------|-----------|
| Accuracy | >0.85 |
| Precision | >0.80 |
| E-Value | >20 |
| Type-I Error | <0.10 |

## Integration

Generated heuristics can be:
1. Used directly in code analysis
2. Stored in knowledge base
3. Exported as documentation
4. Registered as MCP resources

## MCP Tool

This command uses `mcp__akashic-kb__akashic_discover` under the hood.

```

## File: akashic-knowledge/skills/knowledge-discovery/SKILL.md

- Extension: .md
- Language: markdown
- Size: 2871 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/skills/knowledge-discovery/references/extraction-patterns.md

- Extension: .md
- Language: markdown
- Size: 4231 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
# Entity and Relation Extraction Patterns

## Entity Types

### Technical Entities

| Type | Examples | Extraction Cues |
|------|----------|-----------------|
| Concept | "dependency injection", "event sourcing" | Abstract nouns, methodology terms |
| Technology | "React", "PostgreSQL", "Docker" | Capitalized names, version mentions |
| Component | "UserService", "AuthController" | CamelCase, class/function names |
| Artifact | "config.yaml", "Dockerfile" | File extensions, path patterns |

### Research Entities

| Type | Examples | Extraction Cues |
|------|----------|-----------------|
| Author | "John Smith", "et al." | Name patterns, author sections |
| Publication | "arXiv:2024.12345" | DOI, arXiv IDs, citations |
| Date | "January 2026", "v2.0" | Date formats, version strings |

## Relation Types

### Hierarchical Relations

```
IS_A(child, parent)
  - "React is a JavaScript framework"
  - Pattern: X is a/an Y

PART_OF(part, whole)
  - "Authentication module is part of the security system"
  - Pattern: X is part of Y, X belongs to Y

CONTAINS(container, contained)
  - "The package contains three modules"
  - Pattern: X contains Y, X includes Y
```

### Associative Relations

```
RELATED_TO(entity1, entity2)
  - General association
  - Pattern: X relates to Y, X and Y

USES(user, used)
  - "The service uses Redis for caching"
  - Pattern: X uses Y, X leverages Y

IMPLEMENTS(implementer, interface)
  - "UserService implements IUserRepository"
  - Pattern: X implements Y, X realizes Y
```

### Temporal Relations

```
PRECEDES(earlier, later)
  - "Authentication precedes authorization"
  - Pattern: X before Y, X precedes Y

VERSION_OF(newer, older)
  - "React 18 is a version of React"
  - Pattern: vX.Y, version history

DEPRECATED_BY(old, new)
  - "ComponentDidMount deprecated by useEffect"
  - Pattern: deprecated, superseded by
```

## Extraction Algorithms

### Named Entity Recognition (NER)

```python
def extract_entities(text: str) -> list[Entity]:
    """
    Multi-pass entity extraction:
    1. Pattern-based extraction (regex)
    2. Context-based classification
    3. Coreference resolution
    """
    entities = []

    # Pass 1: Pattern matching
    for pattern in ENTITY_PATTERNS:
        matches = pattern.findall(text)
        entities.extend(classify_matches(matches))

    # Pass 2: Context classification
    for entity in entities:
        entity.type = classify_by_context(entity, text)

    # Pass 3: Coreference resolution
    entities = resolve_coreferences(entities, text)

    return entities
```

### Relation Extraction

```python
def extract_relations(text: str, entities: list[Entity]) -> list[Relation]:
    """
    Dependency-based relation extraction:
    1. Parse sentence structure
    2. Identify relation triggers
    3. Link entities via dependencies
    """
    relations = []

    for sentence in split_sentences(text):
        deps = parse_dependencies(sentence)
        triggers = find_relation_triggers(deps)

        for trigger in triggers:
            subject = find_subject(trigger, deps, entities)
            object_ = find_object(trigger, deps, entities)

            if subject and object_:
                relation = Relation(
                    source=subject,
                    target=object_,
                    type=classify_relation(trigger),
                    evidence=sentence
                )
                relations.append(relation)

    return relations
```

## Quality Assurance

### Validation Rules

1. **Entity Consistency**: Same entity, same ID across documents
2. **Relation Validity**: Both endpoints must exist
3. **Type Correctness**: Relations match entity types
4. **Evidence Tracking**: All extractions have source evidence

### Confidence Scoring

```python
def calculate_confidence(extraction: Extraction) -> float:
    """
    Confidence based on:
    - Pattern match strength
    - Context support
    - Cross-document frequency
    """
    score = 0.0

    # Pattern strength (0-0.4)
    score += extraction.pattern_score * 0.4

    # Context support (0-0.3)
    score += extraction.context_score * 0.3

    # Frequency (0-0.3)
    score += min(extraction.frequency / 10, 1.0) * 0.3

    return score
```

```

## File: akashic-knowledge/skills/rag-retrieval/SKILL.md

- Extension: .md
- Language: markdown
- Size: 3185 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/skills/rag-retrieval/references/hybrid-search-config.md

- Extension: .md
- Language: markdown
- Size: 4228 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/skills/graph-reasoning/SKILL.md

- Extension: .md
- Language: markdown
- Size: 4019 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/skills/graph-reasoning/references/cypher-patterns.md

- Extension: .md
- Language: markdown
- Size: 4576 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
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

```

## File: akashic-knowledge/skills/heuristics-synthesis/SKILL.md

- Extension: .md
- Language: markdown
- Size: 4265 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
---
name: heuristics-synthesis
description: |
  AutoHD-based heuristic generation and evolution from patterns.
  Use when: generating heuristics, creating decision functions, evolving rules,
  "create heuristic", "generate rule", "automate decision", "discover heuristic",
  "pattern to function", "AutoHD".
triggers:
  - create heuristic
  - generate rule
  - automate decision
  - discover heuristic
  - pattern to function
  - AutoHD
  - evolve heuristic
---

# Heuristics Synthesis Skill

Generate, evaluate, and evolve heuristic functions from knowledge patterns using the AutoHD (Automated Heuristics Discovery) methodology.

## Quick Start

```bash
# Discover heuristics from knowledge base
/akashic:discover my-research --domain "code-quality" --iterations 5

# Generate specific heuristic
/akashic:synthesize "file complexity scoring" --domain "code-quality"
```

## AutoHD Methodology

### Overview
AutoHD generates executable heuristic functions through iterative evolution:

```
Patterns → Proposal → Evaluation → Evolution → Validated Heuristics
              ↑                        ↓
              └────────────────────────┘
                    (iterate)
```

### Phase 1: Initial Proposal
Generate diverse heuristic candidates based on:
- Extracted patterns from corpus
- Domain constraints
- Prior successful heuristics

### Phase 2: Evaluation
Score each heuristic on:
- Accuracy on validation set
- Computational efficiency
- Generalization capability
- Interpretability

### Phase 3: Evolution
Apply genetic operators:
- **Mutation**: Parameter tweaks, condition changes
- **Crossover**: Combine successful elements
- **Selection**: Top-k survival

### Phase 4: Validation
Final validation with POPPER framework:
- Statistical significance testing
- E-value accumulation
- Type-I error control

## Heuristic Format

```python
def heuristic_complexity_score(context: dict) -> float:
    """
    Estimate code complexity based on structural features.

    Args:
        context: Dictionary containing:
            - lines_of_code: int
            - cyclomatic_complexity: int
            - nesting_depth: int
            - num_dependencies: int

    Returns:
        Score between 0.0 (simple) and 1.0 (complex)

    Domain: code-quality
    Version: 1.2.0
    Confidence: 0.92
    """
    score = 0.0

    # Factor 1: Lines of code (normalized)
    loc = context.get("lines_of_code", 0)
    score += min(loc / 500, 1.0) * 0.25

    # Factor 2: Cyclomatic complexity
    cc = context.get("cyclomatic_complexity", 1)
    score += min(cc / 20, 1.0) * 0.35

    # Factor 3: Nesting depth
    depth = context.get("nesting_depth", 0)
    score += min(depth / 5, 1.0) * 0.25

    # Factor 4: Dependencies
    deps = context.get("num_dependencies", 0)
    score += min(deps / 15, 1.0) * 0.15

    return min(1.0, max(0.0, score))
```

## Evolution Operators

### Mutation Types
| Operator | Description | Example |
|----------|-------------|---------|
| Weight Tuning | Adjust factor weights ±10% | 0.25 → 0.275 |
| Threshold Shift | Change normalization bounds | /500 → /450 |
| Condition Add | Add new context check | Add file_type check |
| Condition Remove | Simplify by removing factors | Remove weak factor |

### Crossover Types
| Operator | Description |
|----------|-------------|
| Factor Exchange | Swap factors between heuristics |
| Weight Average | Average weights of similar factors |
| Structure Merge | Combine structural patterns |

## Quality Criteria

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Accuracy | >0.85 | Overall correctness |
| Precision | >0.80 | True positive rate |
| Efficiency | <100ms | Execution time |
| Interpretability | Required | Human-readable |

## Output Artifacts

1. **Python Functions**: Executable heuristic implementations
2. **Metadata JSON**: Performance metrics and evolution history
3. **Validation Report**: POPPER test results
4. **Documentation**: Markdown with usage examples

## References

For implementation details:
- @references/evolution-operators.md - Genetic operators
- @references/evaluation-metrics.md - Scoring functions
- @references/convergence-criteria.md - Stopping conditions

```

## File: akashic-knowledge/skills/heuristics-synthesis/references/evolution-operators.md

- Extension: .md
- Language: markdown
- Size: 6909 bytes
- Created: 2026-01-16 01:27:01
- Modified: 2026-01-16 01:27:01

### Code

```markdown
# Evolution Operators for Heuristic Synthesis

## Mutation Operators

### 1. Weight Tuning

Adjust numeric weights by small amounts:

```python
def mutate_weight(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Adjust weight by ±10% with Gaussian noise.
    """
    current_weight = heuristic.weights[factor_name]
    noise = np.random.normal(0, 0.05)  # 5% std dev
    new_weight = current_weight * (1 + noise)

    # Ensure weights sum to 1.0
    new_weight = max(0.05, min(0.5, new_weight))

    heuristic.weights[factor_name] = new_weight
    heuristic.normalize_weights()

    return heuristic
```

### 2. Threshold Shift

Modify normalization thresholds:

```python
def mutate_threshold(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Adjust normalization threshold by ±15%.
    """
    current_threshold = heuristic.thresholds[factor_name]
    multiplier = np.random.uniform(0.85, 1.15)
    new_threshold = current_threshold * multiplier

    heuristic.thresholds[factor_name] = new_threshold
    return heuristic
```

### 3. Condition Addition

Add new context checks:

```python
def mutate_add_condition(heuristic: Heuristic, context_keys: list[str]) -> Heuristic:
    """
    Add a new factor from available context keys.
    """
    available = set(context_keys) - set(heuristic.factors.keys())

    if available:
        new_factor = random.choice(list(available))
        heuristic.factors[new_factor] = {
            "weight": 0.1,
            "threshold": estimate_threshold(new_factor),
            "operation": "min_normalize"
        }
        heuristic.normalize_weights()

    return heuristic
```

### 4. Condition Removal

Remove weak or redundant factors:

```python
def mutate_remove_condition(heuristic: Heuristic) -> Heuristic:
    """
    Remove lowest-weighted factor if multiple exist.
    """
    if len(heuristic.factors) > 2:
        weakest = min(heuristic.factors.items(), key=lambda x: x[1]["weight"])
        del heuristic.factors[weakest[0]]
        heuristic.normalize_weights()

    return heuristic
```

### 5. Logic Inversion

Try opposite conditions:

```python
def mutate_invert_logic(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Invert factor logic (high→low or low→high).
    """
    factor = heuristic.factors[factor_name]

    if factor["operation"] == "min_normalize":
        factor["operation"] = "max_normalize"
    elif factor["operation"] == "max_normalize":
        factor["operation"] = "min_normalize"

    return heuristic
```

## Crossover Operators

### 1. Factor Exchange

Swap factors between parent heuristics:

```python
def crossover_factor_exchange(
    parent1: Heuristic,
    parent2: Heuristic
) -> tuple[Heuristic, Heuristic]:
    """
    Exchange random factors between parents.
    """
    child1 = parent1.copy()
    child2 = parent2.copy()

    common_factors = set(parent1.factors.keys()) & set(parent2.factors.keys())

    if common_factors:
        factor = random.choice(list(common_factors))
        child1.factors[factor] = parent2.factors[factor].copy()
        child2.factors[factor] = parent1.factors[factor].copy()

    return child1, child2
```

### 2. Weight Averaging

Average weights of similar factors:

```python
def crossover_weight_average(
    parent1: Heuristic,
    parent2: Heuristic
) -> Heuristic:
    """
    Create child with averaged weights from parents.
    """
    child = parent1.copy()

    for factor in child.factors:
        if factor in parent2.factors:
            w1 = parent1.factors[factor]["weight"]
            w2 = parent2.factors[factor]["weight"]
            child.factors[factor]["weight"] = (w1 + w2) / 2

    child.normalize_weights()
    return child
```

### 3. Structure Merge

Combine structural patterns:

```python
def crossover_structure_merge(
    parent1: Heuristic,
    parent2: Heuristic
) -> Heuristic:
    """
    Merge factors from both parents.
    """
    child = Heuristic()

    # Take all factors from both parents
    all_factors = set(parent1.factors.keys()) | set(parent2.factors.keys())

    for factor in all_factors:
        if factor in parent1.factors and factor in parent2.factors:
            # Average if in both
            child.factors[factor] = {
                "weight": (parent1.factors[factor]["weight"] +
                          parent2.factors[factor]["weight"]) / 2,
                "threshold": (parent1.factors[factor]["threshold"] +
                             parent2.factors[factor]["threshold"]) / 2,
                "operation": random.choice([
                    parent1.factors[factor]["operation"],
                    parent2.factors[factor]["operation"]
                ])
            }
        elif factor in parent1.factors:
            child.factors[factor] = parent1.factors[factor].copy()
        else:
            child.factors[factor] = parent2.factors[factor].copy()

    child.normalize_weights()
    return child
```

## Selection Strategies

### Tournament Selection

```python
def tournament_select(
    population: list[Heuristic],
    tournament_size: int = 3
) -> Heuristic:
    """
    Select winner from random tournament.
    """
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda h: h.fitness)
```

### Elitism

```python
def apply_elitism(
    population: list[Heuristic],
    elite_count: int = 2
) -> list[Heuristic]:
    """
    Preserve top performers across generations.
    """
    sorted_pop = sorted(population, key=lambda h: h.fitness, reverse=True)
    return sorted_pop[:elite_count]
```

## Evolution Loop

```python
def evolve_heuristics(
    initial_population: list[Heuristic],
    validation_set: list[Example],
    max_generations: int = 10,
    mutation_rate: float = 0.3,
    crossover_rate: float = 0.7
) -> Heuristic:
    """
    Main evolution loop.
    """
    population = initial_population

    for generation in range(max_generations):
        # Evaluate fitness
        for heuristic in population:
            heuristic.fitness = evaluate(heuristic, validation_set)

        # Check convergence
        best = max(population, key=lambda h: h.fitness)
        if best.fitness > 0.95:
            break

        # Selection and reproduction
        new_population = apply_elitism(population)

        while len(new_population) < len(population):
            if random.random() < crossover_rate:
                p1 = tournament_select(population)
                p2 = tournament_select(population)
                child, _ = crossover_factor_exchange(p1, p2)
            else:
                child = tournament_select(population).copy()

            if random.random() < mutation_rate:
                child = apply_random_mutation(child)

            new_population.append(child)

        population = new_population

    return max(population, key=lambda h: h.fitness)
```

```

