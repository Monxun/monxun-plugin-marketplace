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
