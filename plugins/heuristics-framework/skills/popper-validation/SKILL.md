---
name: popper-validation
description: |
  POPPER framework for hypothesis validation through sequential falsification.
  Use when: validating heuristics, designing experiments, calculating e-values,
  controlling Type-I errors, statistical hypothesis testing.
  Supports: experiment design, e-value accumulation, falsification testing.
---

# POPPER Validation Skill

## Quick Start

POPPER implements Karl Popper's falsification principle for automated hypothesis validation with rigorous statistical control.

### Core Principle

> A hypothesis is validated not by confirming it, but by failing to falsify it.

### Basic Workflow

```
1. DECOMPOSE: Break into testable sub-hypotheses
2. DESIGN: Create falsification experiments
3. EXECUTE: Run with statistical rigor
4. ACCUMULATE: Calculate e-values
5. DECIDE: Accept/reject at threshold
```

## Core Workflow

### Step 1: Hypothesis Decomposition

Break complex heuristics into testable claims:

```
Main: "Early return reduces complexity"

Sub-H1: "Guard clauses reduce nesting depth"
Sub-H2: "Early returns decrease cyclomatic complexity"
Sub-H3: "Pattern improves readability scores"
```

### Step 2: Experiment Design

For each sub-hypothesis:

| Component | Description |
|-----------|-------------|
| Null Hypothesis | What we try to falsify |
| Test Procedure | How to measure outcome |
| Sample Size | Statistical power requirement |
| Alpha Level | Type-I error threshold |

### Step 3: E-Value Calculation

```python
# E-value properties:
# - E[e] ≤ 1 under null hypothesis
# - Can multiply across experiments
# - Provides anytime-valid inference

e_value = likelihood_alternative / likelihood_null
accumulated = e_value_1 * e_value_2 * ... * e_value_n
```

### Step 4: Decision Rules

| Condition | Decision |
|-----------|----------|
| accumulated_e < α | REJECT (falsified) |
| accumulated_e > 1/α | ACCEPT (validated) |
| Otherwise | CONTINUE testing |

## Statistical Requirements

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Type-I Error | < 0.10 | Balance sensitivity/specificity |
| Statistical Power | > 0.80 | Adequate detection |
| Minimum Sample | 50 | Statistical stability |
| Confidence | 95% | Scientific standard |

## Output Format

```json
{
  "decision": "VALIDATED",
  "confidence": 0.92,
  "accumulatedEValue": 247.3,
  "typeIErrorRate": 0.08,
  "experimentsRun": 5
}
```

## Additional Resources

- For experiment design: [experiment-design.md](references/experiment-design.md)
- For e-value theory: [e-value-theory.md](references/e-value-theory.md)
- For statistical tests: [statistical-tests.md](references/statistical-tests.md)

## Research Foundation

Based on: "POPPER: Agentic AI Framework for Hypothesis Validation"
- Authors: Stanford & Harvard researchers
- GitHub: github.com/snap-stanford/POPPER
- Paper: arxiv.org/abs/2502.09858
