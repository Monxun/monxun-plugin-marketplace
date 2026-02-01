---
name: heuristics-synthesis
description: |
  AutoHD-based heuristic generation and evolution from patterns.
  Use when: generating heuristics, creating decision functions, evolving rules,
  "create heuristic", "generate rule", "automate decision", "discover heuristic",
  "pattern to function", "AutoHD".
triggers:
  - create heuristic
  - generate rule
  - automate decision
  - discover heuristic
  - pattern to function
  - AutoHD
  - evolve heuristic
---

# Heuristics Synthesis Skill

Generate, evaluate, and evolve heuristic functions from knowledge patterns using the AutoHD (Automated Heuristics Discovery) methodology.

## Quick Start

```bash
# Discover heuristics from knowledge base
/akashic:discover my-research --domain "code-quality" --iterations 5

# Generate specific heuristic
/akashic:synthesize "file complexity scoring" --domain "code-quality"
```

## AutoHD Methodology

### Overview
AutoHD generates executable heuristic functions through iterative evolution:

```
Patterns → Proposal → Evaluation → Evolution → Validated Heuristics
              ↑                        ↓
              └────────────────────────┘
                    (iterate)
```

### Phase 1: Initial Proposal
Generate diverse heuristic candidates based on:
- Extracted patterns from corpus
- Domain constraints
- Prior successful heuristics

### Phase 2: Evaluation
Score each heuristic on:
- Accuracy on validation set
- Computational efficiency
- Generalization capability
- Interpretability

### Phase 3: Evolution
Apply genetic operators:
- **Mutation**: Parameter tweaks, condition changes
- **Crossover**: Combine successful elements
- **Selection**: Top-k survival

### Phase 4: Validation
Final validation with POPPER framework:
- Statistical significance testing
- E-value accumulation
- Type-I error control

## Heuristic Format

```python
def heuristic_complexity_score(context: dict) -> float:
    """
    Estimate code complexity based on structural features.

    Args:
        context: Dictionary containing:
            - lines_of_code: int
            - cyclomatic_complexity: int
            - nesting_depth: int
            - num_dependencies: int

    Returns:
        Score between 0.0 (simple) and 1.0 (complex)

    Domain: code-quality
    Version: 1.2.0
    Confidence: 0.92
    """
    score = 0.0

    # Factor 1: Lines of code (normalized)
    loc = context.get("lines_of_code", 0)
    score += min(loc / 500, 1.0) * 0.25

    # Factor 2: Cyclomatic complexity
    cc = context.get("cyclomatic_complexity", 1)
    score += min(cc / 20, 1.0) * 0.35

    # Factor 3: Nesting depth
    depth = context.get("nesting_depth", 0)
    score += min(depth / 5, 1.0) * 0.25

    # Factor 4: Dependencies
    deps = context.get("num_dependencies", 0)
    score += min(deps / 15, 1.0) * 0.15

    return min(1.0, max(0.0, score))
```

## Evolution Operators

### Mutation Types
| Operator | Description | Example |
|----------|-------------|---------|
| Weight Tuning | Adjust factor weights ±10% | 0.25 → 0.275 |
| Threshold Shift | Change normalization bounds | /500 → /450 |
| Condition Add | Add new context check | Add file_type check |
| Condition Remove | Simplify by removing factors | Remove weak factor |

### Crossover Types
| Operator | Description |
|----------|-------------|
| Factor Exchange | Swap factors between heuristics |
| Weight Average | Average weights of similar factors |
| Structure Merge | Combine structural patterns |

## Quality Criteria

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Accuracy | >0.85 | Overall correctness |
| Precision | >0.80 | True positive rate |
| Efficiency | <100ms | Execution time |
| Interpretability | Required | Human-readable |

## Output Artifacts

1. **Python Functions**: Executable heuristic implementations
2. **Metadata JSON**: Performance metrics and evolution history
3. **Validation Report**: POPPER test results
4. **Documentation**: Markdown with usage examples

## References

For implementation details:
- @references/evolution-operators.md - Genetic operators
- @references/evaluation-metrics.md - Scoring functions
- @references/convergence-criteria.md - Stopping conditions
