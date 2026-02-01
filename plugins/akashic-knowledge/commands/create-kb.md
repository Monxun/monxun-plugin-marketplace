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
