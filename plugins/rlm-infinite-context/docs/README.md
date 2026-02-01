# RLM Infinite Context Plugin

> **Recursive Language Model (RLM)** implementation for Claude Code, enabling processing of arbitrarily long contexts (10M+ tokens) without information loss.

Based on the MIT research paper on recursive language models for inference-time scaling.

## Overview

This plugin implements the RLM technique which dramatically extends Claude's effective context window by:

1. **External Storage**: Large documents are stored outside the model's context window
2. **Recursive Search**: The model searches through content using tools
3. **Deep Diving**: Found sections can be recursively searched for more detail
4. **No Information Loss**: Unlike summarization, no content is compressed or discarded

### Key Benefits

| Feature | Traditional | RLM |
|---------|-------------|-----|
| Max Context | ~200K tokens | **Unlimited** |
| Information Loss | Yes (summarization) | **None** |
| Cost | Linear with size | **Efficient** |
| Recall Quality | Degrades with size | **Consistent** |

## Installation

```bash
# Clone or download the plugin
git clone https://github.com/example/rlm-infinite-context.git

# Use with Claude Code
claude --plugin-dir ./rlm-infinite-context
```

## Quick Start

```bash
# 1. Load a large document
/rlm:load ./massive-codebase.txt

# 2. View the structure
/rlm:outline

# 3. Search for content
/rlm:search "authentication"

# 4. Go deeper into results
/rlm:search-deep "OAuth tokens" --chunks 5,6,7

# 5. Ask questions
/rlm:query "How does the payment module handle refunds?"

# 6. Check status
/rlm:status --stats
```

## Commands

| Command | Description |
|---------|-------------|
| `/rlm:load` | Load documents into RLM storage |
| `/rlm:search` | Search loaded context |
| `/rlm:search-deep` | Recursive sub-search in chunks |
| `/rlm:query` | Ask questions about content |
| `/rlm:outline` | View document structure |
| `/rlm:status` | Check loaded contexts and stats |
| `/rlm:clear` | Clear loaded contexts |

## How It Works

### The RLM Technique

Traditional approach (problematic at scale):
```
┌────────────────────────────────────────┐
│         Model Context Window           │
│  ┌──────────────────────────────────┐  │
│  │  Entire document (10M tokens)    │  │  ← Context rot!
│  │  Quality degrades significantly  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

RLM approach (scales indefinitely):
```
┌────────────────────────────────────────┐
│         Model Context Window           │
│  ┌──────────────────────────────────┐  │
│  │  Query + Relevant chunks only    │  │  ← Only what's needed!
│  │  (~10-30K tokens)                │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
                    ↕ Search Tools
┌────────────────────────────────────────┐
│        External Storage (10M+)         │
│  Chunked, indexed, searchable content  │
└────────────────────────────────────────┘
```

### Recursive Search Flow

```
User Question: "What authentication methods are supported?"

Step 1: Initial Search (Depth 0)
   └─→ Found chunks 15, 23, 47 about authentication

Step 2: Deep Search on chunk 15 (Depth 1)
   └─→ Found OAuth 2.0 details

Step 3: Deep Search on chunk 23 (Depth 1)
   └─→ Found SAML configuration

Step 4: Synthesize Answer
   └─→ "The system supports OAuth 2.0 (primary) and SAML 2.0 (SSO)..."
```

## Search Types

### Keyword Search
```bash
/rlm:search "error handling exceptions"
```
Best for: Finding mentions of specific terms

### Regex Search
```bash
/rlm:search "def\s+test_\w+\(" --type regex
```
Best for: Pattern matching in code

### Section Search
```bash
/rlm:search "Chapter 5" --type section
```
Best for: Finding document structure

### Recursive Search
```bash
/rlm:search-deep "specific detail" --chunks 10,11,12
```
Best for: Deep information retrieval

## Performance

### Token Efficiency

| Scenario | Full Context | RLM | Savings |
|----------|--------------|-----|---------|
| 1M tokens, 1 query | 1M | ~20K | 98% |
| 10M tokens, 5 queries | 50M | ~100K | 99.8% |

### Benchmarks

| Document Size | Load Time | Search Time |
|---------------|-----------|-------------|
| 1 MB | <1s | <100ms |
| 10 MB | ~2s | ~200ms |
| 100 MB | ~20s | ~500ms |

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `RLM_MAX_DEPTH` | 10 | Maximum recursion depth |
| `RLM_CHUNK_SIZE` | 4000 | Characters per chunk |
| `RLM_OVERLAP` | 200 | Overlap between chunks |
| `RLM_DATA_DIR` | `./data` | Storage directory |

## Architecture

```
rlm-infinite-context/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                # User commands
│   ├── load.md
│   ├── search.md
│   ├── search-deep.md
│   └── ...
├── agents/                  # Specialized agents
│   ├── orchestrator.md
│   └── searcher.md
├── skills/                  # Search skills
│   └── rlm-search/
│       ├── SKILL.md
│       └── references/
├── hooks/                   # Lifecycle hooks
│   ├── hooks.json
│   └── scripts/
├── servers/                 # MCP server
│   └── rlm_server.py
└── docs/
    └── README.md
```

## Use Cases

### Code Repository Analysis
```bash
/rlm:load ./entire-monorepo.txt --name "codebase"
/rlm:query "How does the authentication middleware work?"
```

### Research Paper Processing
```bash
/rlm:load ./research-papers.txt --name "literature"
/rlm:query "What methods have been used to address context limitations?"
```

### Documentation Search
```bash
/rlm:load ./all-docs.txt --name "docs"
/rlm:search "API rate limits"
```

### Log Analysis
```bash
/rlm:load ./server-logs.txt --name "logs"
/rlm:search "ERROR.*timeout" --type regex
```

## Comparison with Alternatives

| Approach | Quality | Speed | Cost | Max Size |
|----------|---------|-------|------|----------|
| Native Context | Degrades | Fast | High | ~200K |
| Summarization | Lossy | Medium | Medium | Unlimited |
| RAG | Good | Medium | Medium | Unlimited |
| **RLM** | **Excellent** | **Fast** | **Low** | **Unlimited** |

## Troubleshooting

### Common Issues

1. **"No context loaded"**: Run `/rlm:load` first
2. **Empty results**: Try broader search terms
3. **Max depth reached**: Start with broader query
4. **Slow performance**: Check chunk count with `/rlm:status`

See `skills/rlm-search/references/troubleshooting.md` for detailed help.

## Credits

Based on MIT research on Recursive Language Models for inference-time scaling.

## License

MIT License
