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
