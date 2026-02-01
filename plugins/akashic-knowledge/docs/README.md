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
