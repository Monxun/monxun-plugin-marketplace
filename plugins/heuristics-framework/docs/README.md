# Heuristics Framework Plugin

LLM-based framework for automated heuristic discovery, validation, and documentation using AutoHD, POPPER, and knowledge graph construction methodologies.

## Overview

This plugin provides a complete pipeline for:

1. **Pattern Extraction** - Extract implicit patterns from code, documents, and research
2. **Heuristic Discovery (AutoHD)** - Generate executable heuristic functions
3. **Validation (POPPER)** - Validate heuristics through sequential falsification
4. **Knowledge Graph Construction** - Build structured relationships
5. **Documentation Generation** - Multi-format output (JSON-LD, Markdown, HTML)

## Installation

```bash
claude plugin install heuristics-framework@monxun-marketplace --scope local
```

## Commands

| Command | Description |
|---------|-------------|
| `/heuristics-framework:discover <path>` | Full discovery pipeline |
| `/heuristics-framework:extract <path>` | Extract patterns only |
| `/heuristics-framework:validate <path>` | Validate heuristics |
| `/heuristics-framework:build-kg <path>` | Build knowledge graph |

## Quick Start

```bash
# Discover heuristics from a codebase
/heuristics-framework:discover ./src --domain software-engineering

# Extract patterns without full synthesis
/heuristics-framework:extract ./docs --min-confidence 0.7

# Validate existing heuristics
/heuristics-framework:validate ./heuristics/

# Build knowledge graph
/heuristics-framework:build-kg ./patterns.json --format neo4j
```

## Agents

| Agent | Purpose |
|-------|---------|
| `heuristics-orchestrator` | Coordinates the full pipeline |
| `heuristics-extractor` | Parses corpus and extracts patterns |
| `heuristics-synthesizer` | Generates heuristic functions (AutoHD) |
| `heuristics-validator` | Validates through falsification (POPPER) |
| `heuristics-documenter` | Generates multi-format documentation |
| `heuristics-kg-builder` | Constructs knowledge graphs |

## Skills

| Skill | Description |
|-------|-------------|
| `autohd-discovery` | AutoHD methodology for heuristic generation |
| `popper-validation` | POPPER framework for hypothesis validation |
| `kg-construction` | Knowledge graph construction pipeline |
| `deterministic-inference` | Reproducible LLM inference configuration |

## Research Foundation

Based on cutting-edge research:

- **AutoHD**: "Complex LLM Planning via Automated Heuristics Discovery" (Texas A&M, Feb 2025)
- **POPPER**: "Agentic AI Framework for Hypothesis Validation" (Stanford/Harvard, Feb 2025)
- **KG Construction**: "LLM-empowered Knowledge Graph Construction Survey" (Oct 2025)
- **Deterministic Inference**: SGLang batch-invariant kernels (Sep 2025)

## Output Formats

### JSON-LD Schema

```json
{
  "@type": "heuristic:Heuristic",
  "@id": "heuristic:early-return-001",
  "name": "Early Return Pattern",
  "heuristic:confidence": 0.87,
  "popper:validation": {
    "method": "POPPER",
    "typeIError": 0.08
  }
}
```

### Heuristic Function

```python
def heuristic_early_return(current_state: dict, goal_state: dict) -> float:
    """Evaluate code against early return pattern."""
    # Implementation
    pass
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Heuristic confidence | >0.85 |
| Type-I error rate | <0.10 |
| Statistical power | >0.80 |
| KG entity precision | >0.85 |

## License

MIT
