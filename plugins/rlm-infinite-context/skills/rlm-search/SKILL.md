---
name: rlm-search
description: |
  Recursive Language Model search strategies for infinite context processing.
  Use when: processing large documents, searching long contexts, "unlimited context",
  "10 million tokens", "recursive search", "context window limit", "long document",
  "massive codebase", needle in haystack, deep search, context rot.
  Supports: keyword search, regex search, semantic sections, recursive sub-queries.
triggers:
  - large document
  - long context
  - unlimited context
  - recursive search
  - massive file
  - 10 million tokens
  - context window
  - needle in haystack
allowed-tools: Read, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# RLM Search Skill

Master the Recursive Language Model technique for processing arbitrarily long contexts.

## Quick Start

```bash
# Load a massive document
/rlm:load ./huge-codebase.txt

# View structure
/rlm:outline

# Search for content
/rlm:search "authentication"

# Go deeper into results
/rlm:search-deep "OAuth tokens" --chunks 5,6,7

# Ask questions
/rlm:query "How does the system handle session management?"
```

## Core Concept

**The Key Insight**: Long prompts should NOT be fed directly into the model's context window. Instead, they should be stored externally and accessed through search tools.

```
Traditional Approach:
┌─────────────────────────────────┐
│     Model Context Window        │
│  ┌───────────────────────────┐  │
│  │ Entire 10M token document │  │  ← Context rot!
│  └───────────────────────────┘  │
└─────────────────────────────────┘

RLM Approach:
┌─────────────────────────────────┐
│     Model Context Window        │
│  ┌───────────────────────────┐  │
│  │ Query + Relevant chunks   │  │  ← Only what's needed
│  │ (~20K tokens)             │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
           ↕ Search Tools
┌─────────────────────────────────┐
│   External Storage (10M+)       │
│   Chunked, indexed, searchable  │
└─────────────────────────────────┘
```

## Search Strategies

### 1. Keyword Search
Best for: Finding mentions of specific terms
```bash
/rlm:search "error handling exceptions" --type keyword
```

### 2. Regex Search
Best for: Pattern matching, code structures
```bash
/rlm:search "def\s+test_\w+\(" --type regex
```

### 3. Section Search
Best for: Finding document structure
```bash
/rlm:search "Chapter 5" --type section
```

### 4. Recursive Search
Best for: Deep information retrieval
```bash
# Step 1: Find relevant areas
/rlm:search "payment processing"
# Returns chunks: 45, 46, 47

# Step 2: Search deeper
/rlm:search-deep "refund logic" --chunks 45,46,47
```

## Recursive Workflow

```
Query: "What error codes does the payment module return?"

Depth 0: Search "payment error codes"
  → Chunks 45, 67, 89 (high relevance)
  
Depth 1: Search within chunks 45, 67
  → Sub-chunks with error definitions
  
Depth 2: Search for "HTTP status" in sub-chunks  
  → Exact error code mappings found!
  
Result: Synthesize findings from all depths
```

## Optimization Tips

### Query Formulation
- Start broad, then narrow
- Use specific terminology from the document
- Reference section names if known

### Chunk Selection
- Don't search too many chunks at once (increases cost)
- Focus on high-relevance results from initial search
- Use outline to target specific areas

### Depth Management
- Most queries resolve at depth 0-2
- Depth 3+ indicates complex queries
- Max depth 10 prevents runaway searches

## Performance Characteristics

| Document Size | Load Time | Search Time | Memory |
|--------------|-----------|-------------|--------|
| 1 MB | <1s | <100ms | ~10 MB |
| 10 MB | ~2s | ~200ms | ~100 MB |
| 100 MB | ~20s | ~500ms | ~1 GB |
| 1 GB | ~3min | ~1s | ~10 GB |

## Comparison with Alternatives

| Method | Max Tokens | Quality | Cost |
|--------|------------|---------|------|
| Native context | ~200K | Degrades | High |
| Summarization | Unlimited | Lossy | Medium |
| RAG | Unlimited | Good | Medium |
| **RLM** | **Unlimited** | **Excellent** | **Low** |

## References

For detailed documentation:
- @references/search-patterns.md - Search pattern reference
- @references/optimization.md - Performance optimization
- @references/troubleshooting.md - Common issues and solutions
