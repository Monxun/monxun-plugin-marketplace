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
