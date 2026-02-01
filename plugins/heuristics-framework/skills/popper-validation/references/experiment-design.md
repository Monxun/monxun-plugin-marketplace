# POPPER Experiment Design Reference

## Experiment Structure

```python
@dataclass
class Experiment:
    hypothesis: str           # What we're testing
    null_hypothesis: str      # What we try to falsify
    test_procedure: str       # How to run the test
    sample_size: int          # Number of samples
    alpha: float              # Type-I error threshold
    power: float              # Statistical power target
    expected_effect: float    # Expected effect size
```

## Design Process

### Step 1: Identify Measurable Implications

From abstract hypothesis to concrete measurements:

```
Hypothesis: "Early return reduces complexity"

Measurable implications:
1. Cyclomatic complexity metric
2. Nesting depth measurement
3. Cognitive complexity score
4. Readability index
```

### Step 2: Formulate Null Hypothesis

```
H0: Early return has no effect on complexity
H1: Early return reduces complexity

Test: Compare complexity metrics with/without early returns
```

### Step 3: Design Test Procedure

```python
def design_test_procedure(hypothesis: str) -> TestProcedure:
    """
    Generate test procedure for hypothesis.

    Components:
    1. Sample selection criteria
    2. Measurement methodology
    3. Control variables
    4. Statistical test selection
    """
    return TestProcedure(
        sampling="Stratified by project size",
        measurement="Automated AST analysis",
        controls=["Language", "Project type", "Team size"],
        test="Paired t-test or Wilcoxon"
    )
```

### Step 4: Calculate Sample Size

```python
def calculate_sample_size(
    effect_size: float,      # Expected effect (Cohen's d)
    alpha: float = 0.10,     # Type-I error rate
    power: float = 0.80      # Statistical power
) -> int:
    """
    Calculate required sample size.

    Using power analysis formula for two-sample test.
    """
    from scipy import stats

    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    return int(np.ceil(n))
```

## Experiment Types

### Type 1: A/B Comparison

```
Group A: With pattern applied
Group B: Without pattern

Measure: Metric difference
Test: Independent samples t-test
```

### Type 2: Before/After

```
Before: Baseline measurement
After: Post-intervention measurement

Measure: Change in metric
Test: Paired samples t-test
```

### Type 3: Natural Experiment

```
Observational: Code with pattern naturally occurring
Control: Code without pattern

Measure: Metric comparison
Test: Propensity score matching
```

## Boundary Condition Testing

Always test edge cases:

```python
boundary_tests = [
    "Empty input",
    "Single element",
    "Maximum size",
    "Null values",
    "Type edge cases"
]
```

## Reporting Template

```json
{
  "experimentId": "exp-001",
  "hypothesis": "...",
  "procedure": {
    "type": "A/B",
    "sampleSize": 100,
    "duration": "2 weeks"
  },
  "results": {
    "testStatistic": 3.45,
    "pValue": 0.002,
    "effectSize": 0.48,
    "confidenceInterval": [0.23, 0.73]
  },
  "conclusion": "Reject null hypothesis"
}
```
