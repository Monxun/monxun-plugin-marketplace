# Validate Heuristic Command

Run POPPER validation on a specific heuristic or set of heuristics.

## Usage

```
/heuristics-framework:validate <heuristic-path> [options]
```

## Arguments

- `$1` - Path to heuristic file or directory (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--alpha <0-1>` - Type-I error threshold (default: 0.10)
- `--power <0-1>` - Statistical power target (default: 0.80)
- `--samples <n>` - Minimum samples per test (default: 50)
- `--output <path>` - Validation report output path

## Workflow

This command delegates to the `heuristics-validator` agent to:

1. **Decompose** heuristic into testable sub-hypotheses
2. **Design** falsification experiments
3. **Execute** experiments with statistical rigor
4. **Calculate** e-values for evidence accumulation
5. **Report** validation results with confidence scores

## Injected Skills

- `popper-validation` - POPPER framework implementation

## Example

```bash
# Validate a single heuristic
/heuristics-framework:validate ./heuristics/early-return.py

# Validate all heuristics in directory
/heuristics-framework:validate ./heuristics/ --alpha 0.05

# With custom sample size
/heuristics-framework:validate ./heuristics/guard-clause.py --samples 100
```

## Output Format

```json
{
  "heuristicId": "...",
  "validationMethod": "POPPER",
  "decision": "VALIDATED|REJECTED|INCONCLUSIVE",
  "confidence": 0.92,
  "accumulatedEValue": 247.3,
  "typeIErrorRate": 0.08,
  "subHypotheses": [...],
  "counterExamples": [...]
}
```

## Decision Criteria

| Accumulated E-Value | Decision |
|---------------------|----------|
| < α (0.10) | REJECTED |
| > 1/α (10) | VALIDATED |
| Otherwise | INCONCLUSIVE |
