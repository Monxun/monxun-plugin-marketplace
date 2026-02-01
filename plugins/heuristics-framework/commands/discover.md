# Discover Heuristics Command

Discover and document heuristics from a corpus using the full AutoHD + POPPER pipeline.

## Usage

```
/heuristics-framework:discover <corpus-path> [options]
```

## Arguments

- `$1` - Path to corpus directory (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--domain <domain>` - Filter to specific domain
- `--confidence <0-1>` - Minimum confidence threshold (default: 0.85)
- `--output <path>` - Output directory (default: ./heuristics-output)
- `--format <json|md|html|all>` - Output format (default: all)

## Workflow

This command delegates to the `heuristics-orchestrator` agent which coordinates:

1. **Ingestion Phase**
   - Corpus parsing via `heuristics-extractor`
   - Knowledge graph construction via `heuristics-kg-builder`

2. **Discovery Phase (AutoHD)**
   - Heuristic synthesis via `heuristics-synthesizer`
   - Evolutionary refinement

3. **Validation Phase (POPPER)**
   - Sequential falsification via `heuristics-validator`
   - Statistical significance testing

4. **Documentation Phase**
   - Multi-format output via `heuristics-documenter`

## Injected Skills

- `autohd-discovery` - Heuristic generation methodology
- `popper-validation` - Hypothesis validation framework

## Example

```bash
# Discover heuristics from a codebase
/heuristics-framework:discover ./src --domain software-engineering

# With custom confidence threshold
/heuristics-framework:discover ./docs --confidence 0.90 --format json
```

## Output

```
heuristics-output/
├── json-ld/
│   └── *.jsonld
├── markdown/
│   ├── index.md
│   └── *.md
├── html/
│   ├── index.html
│   └── *.html
├── knowledge-graph.json
└── validation-report.json
```
