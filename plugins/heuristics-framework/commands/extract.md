# Extract Patterns Command

Extract patterns from a corpus without full heuristic synthesis.

## Usage

```
/heuristics-framework:extract <corpus-path> [options]
```

## Arguments

- `$1` - Path to corpus directory or file (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--domain <domain>` - Domain context for extraction
- `--min-confidence <0-1>` - Minimum pattern confidence (default: 0.5)
- `--min-frequency <n>` - Minimum occurrence count (default: 2)
- `--output <path>` - Output file path (default: patterns.json)
- `--format <json|yaml>` - Output format (default: json)

## Workflow

This command delegates to the `heuristics-extractor` agent to:

1. **Parse** corpus files (code, documents, research)
2. **Chunk** content for LLM processing
3. **Extract** patterns using domain-specific prompts
4. **Deduplicate** similar patterns
5. **Rank** by confidence and frequency

## Injected Skills

- `autohd-discovery` - Pattern extraction methodology

## Example

```bash
# Extract patterns from source code
/heuristics-framework:extract ./src --domain software-engineering

# Extract from documents with custom threshold
/heuristics-framework:extract ./docs --min-confidence 0.7 --min-frequency 5

# Output as YAML
/heuristics-framework:extract ./research --format yaml --output patterns.yaml
```

## Output Format

```json
{
  "patterns": [
    {
      "id": "pattern-001",
      "name": "Early Return Pattern",
      "type": "best-practice",
      "domain": "software-engineering",
      "description": "Return early for edge cases",
      "preconditions": [...],
      "postconditions": [...],
      "evidence": [...],
      "confidence": 0.85,
      "frequency": 15
    }
  ],
  "metadata": {
    "corpusPath": "...",
    "chunkCount": 50,
    "extractionDate": "2026-01-15"
  }
}
```

## Supported File Types

| Type | Extensions | Parser |
|------|------------|--------|
| Python | .py | AST + semantic |
| JavaScript | .js, .ts | AST + semantic |
| Markdown | .md | Section-based |
| Text | .txt | Paragraph-based |
| PDF | .pdf | Text extraction |
