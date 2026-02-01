---
name: autohd-discovery
description: |
  AutoHD (Automated Heuristics Discovery) methodology for LLM-based heuristic generation.
  Use when: generating heuristic functions, evolving candidates, implementing
  inference-time search guidance, creating executable Python heuristics.
  Supports: heuristic proposal, evaluation, evolution, convergence testing.
---

# AutoHD Discovery Skill

## Quick Start

AutoHD enables LLMs to generate explicit heuristic functions H(s, G) as Python code to guide inference-time search without additional model training.

### Core Workflow

```
1. PROPOSE: Generate diverse candidate heuristics
2. EVALUATE: Test against validation sets
3. EVOLVE: Refine top performers
4. CONVERGE: Select best heuristic
```

### Basic Heuristic Template

```python
def heuristic(current_state: Any, goal_state: Any) -> float:
    """
    Evaluate proximity of current state to goal.

    Args:
        current_state: Current problem state
        goal_state: Target state to achieve

    Returns:
        float: Score where lower = closer to goal
    """
    # Domain-specific implementation
    pass
```

## Core Workflow

### Step 1: Heuristic Proposal

Generate diverse candidates using multiple strategies:

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Direct Translation | Convert rules to code | Clear explicit patterns |
| Analogical Reasoning | Adapt from similar domains | Cross-domain transfer |
| Decomposition | Break into sub-heuristics | Complex patterns |
| Relaxation | Start strict, then relax | Constraint-heavy domains |

### Step 2: Evaluation

Test candidates with these metrics:

- **Accuracy**: % of correct orderings
- **Efficiency**: Computation time per call
- **Consistency**: Variance across runs
- **Admissibility**: Never overestimates cost

### Step 3: Evolution

Refine through generations:

```
Parameters:
- Population: 20 candidates
- Selection: Top 5 performers
- Mutation rate: 0.3
- Max generations: 10
- Convergence: <1% improvement
```

### Step 4: Convergence

Stop when:
- Max generations reached
- Improvement below threshold
- Target accuracy achieved

## Quality Criteria

| Metric | Minimum | Target |
|--------|---------|--------|
| Accuracy | 0.75 | 0.85+ |
| Computation | <100ms | <50ms |
| Consistency | σ < 0.1 | σ < 0.05 |

## Additional Resources

- For heuristic function patterns: [function-patterns.md](references/function-patterns.md)
- For evaluation metrics: [evaluation-metrics.md](references/evaluation-metrics.md)
- For evolution parameters: [evolution-params.md](references/evolution-params.md)

## Research Foundation

Based on: "Complex LLM Planning via Automated Heuristics Discovery"
- Authors: Hongyi Ling et al. (Texas A&M)
- Paper: arxiv.org/abs/2502.19295
