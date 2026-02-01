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
