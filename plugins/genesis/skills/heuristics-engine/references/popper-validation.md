# POPPER Validation Reference

Statistical validation through sequential falsification testing.

## Overview

POPPER (Principled Observation-based Pattern Proving through Experimental Refutation) validates heuristics by attempting to falsify them through controlled experiments.

## Core Principles

1. **Falsifiability**: Hypotheses must be testable and refutable
2. **Sequential Testing**: Test one hypothesis at a time
3. **E-Value Accumulation**: Evidence accumulates across experiments
4. **Type-I Error Control**: Maintain statistical validity

## Process

```
┌─────────────────────────────────────────────────────────────┐
│  1. DECOMPOSE                                                │
│     Break heuristic into testable hypotheses                 │
├─────────────────────────────────────────────────────────────┤
│  2. DESIGN                                                   │
│     Create falsification experiments                         │
├─────────────────────────────────────────────────────────────┤
│  3. EXECUTE                                                  │
│     Run experiments, collect results                         │
├─────────────────────────────────────────────────────────────┤
│  4. ANALYZE                                                  │
│     Calculate e-values, make decisions                       │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Decompose

### Hypothesis Extraction
```python
def decompose_heuristic(heuristic_code: str) -> list[dict]:
    """
    Extract testable hypotheses from heuristic.

    Example heuristic:
    "If package.json contains 'express', detect as Express.js"

    Hypotheses:
    - H1: Package with 'express' dependency is Express.js project
    - H2: Package without 'express' is NOT Express.js project
    - H3: Related packages indicate Express.js with lower confidence
    """
    prompt = f"""
    Extract testable hypotheses from this heuristic:

    {heuristic_code}

    For each hypothesis:
    1. State the claim clearly
    2. Define what would falsify it
    3. Specify the null hypothesis
    """
    return llm_extract_hypotheses(prompt)
```

### Hypothesis Format
```json
{
  "hypotheses": [
    {
      "id": "H1",
      "claim": "Package.json with 'express' dependency indicates Express.js",
      "null": "Package.json with 'express' does NOT indicate Express.js",
      "falsifier": "Find express dependency in non-Express.js project",
      "prior_probability": 0.95
    },
    {
      "id": "H2",
      "claim": "Package without 'express' is not Express.js project",
      "null": "Package without 'express' CAN be Express.js project",
      "falsifier": "Find Express.js project without direct express dependency",
      "prior_probability": 0.80
    }
  ]
}
```

## Step 2: Design Experiments

### Experiment Types
```python
def design_experiments(hypothesis: dict) -> list[dict]:
    """
    Design falsification experiments for hypothesis.
    """
    experiments = []

    # Positive case experiments
    experiments.append({
        "type": "positive",
        "description": f"Verify {hypothesis['claim']}",
        "sample_source": "known_positive_examples",
        "expected_result": True
    })

    # Negative case experiments
    experiments.append({
        "type": "negative",
        "description": f"Test null: {hypothesis['null']}",
        "sample_source": "known_negative_examples",
        "expected_result": False
    })

    # Edge case experiments
    experiments.append({
        "type": "edge",
        "description": "Test boundary conditions",
        "sample_source": "generated_edge_cases",
        "expected_result": "varies"
    })

    return experiments
```

### Sample Generation
```python
def generate_test_samples(experiment: dict, n_samples: int = 100):
    """
    Generate test samples for experiment.
    """
    if experiment['sample_source'] == 'known_positive_examples':
        return fetch_positive_examples(n_samples)

    elif experiment['sample_source'] == 'known_negative_examples':
        return fetch_negative_examples(n_samples)

    elif experiment['sample_source'] == 'generated_edge_cases':
        return generate_edge_cases(n_samples)
```

## Step 3: Execute

### Sequential Testing
```python
def execute_experiment(heuristic, samples, alpha=0.05):
    """
    Execute experiment with sequential testing.

    Uses e-values for anytime-valid inference.
    """
    results = []
    e_value = 1.0  # Initial e-value

    for sample in samples:
        # Run heuristic
        predicted, confidence = heuristic(sample['input'])
        expected = sample['expected']

        # Calculate likelihood ratio
        if predicted == expected:
            likelihood_ratio = (1 - alpha) / 0.5  # Correct prediction
        else:
            likelihood_ratio = alpha / 0.5  # Incorrect prediction

        # Update e-value
        e_value *= likelihood_ratio

        results.append({
            'sample_id': sample['id'],
            'predicted': predicted,
            'expected': expected,
            'correct': predicted == expected,
            'e_value': e_value
        })

        # Early stopping: strong evidence for/against
        if e_value > 1/alpha:  # Strong evidence FOR hypothesis
            break
        if e_value < alpha:  # Strong evidence AGAINST hypothesis
            break

    return results, e_value
```

## Step 4: Analyze

### E-Value Interpretation
```
E-value > 20:     Strong evidence FOR hypothesis
E-value > 10:     Moderate evidence FOR hypothesis
E-value 1-10:     Weak evidence
E-value 0.1-1:    Weak evidence AGAINST
E-value < 0.1:    Moderate evidence AGAINST
E-value < 0.05:   Strong evidence AGAINST (reject at α=0.05)
```

### Decision Function
```python
def make_decision(e_value: float, alpha: float = 0.05) -> dict:
    """
    Make validation decision based on e-value.
    """
    if e_value > 1/alpha:
        return {
            "decision": "VALIDATED",
            "confidence": "high",
            "e_value": e_value,
            "interpretation": "Strong evidence supports hypothesis"
        }
    elif e_value < alpha:
        return {
            "decision": "FALSIFIED",
            "confidence": "high",
            "e_value": e_value,
            "interpretation": "Strong evidence against hypothesis"
        }
    else:
        return {
            "decision": "INCONCLUSIVE",
            "confidence": "low",
            "e_value": e_value,
            "interpretation": "Insufficient evidence",
            "recommendation": "Collect more samples"
        }
```

## Full Validation Pipeline

```python
def popper_validate(heuristic, alpha=0.05):
    """
    Full POPPER validation of heuristic.
    """
    # Decompose
    hypotheses = decompose_heuristic(heuristic)

    results = []
    for h in hypotheses:
        # Design experiments
        experiments = design_experiments(h)

        h_results = []
        for exp in experiments:
            # Generate samples
            samples = generate_test_samples(exp)

            # Execute
            exp_results, e_value = execute_experiment(heuristic, samples, alpha)

            # Analyze
            decision = make_decision(e_value, alpha)
            h_results.append({
                "experiment": exp,
                "results": exp_results,
                "decision": decision
            })

        results.append({
            "hypothesis": h,
            "experiments": h_results,
            "overall_valid": all(r['decision']['decision'] == 'VALIDATED' for r in h_results)
        })

    return {
        "heuristic_valid": all(r['overall_valid'] for r in results),
        "hypotheses": results
    }
```

## Output Format

```json
{
  "validation_result": {
    "heuristic_id": "h_framework_detection_v3",
    "valid": true,
    "overall_e_value": 156.7,
    "hypotheses": [
      {
        "id": "H1",
        "valid": true,
        "e_value": 234.5,
        "experiments_run": 3,
        "samples_tested": 150
      }
    ],
    "falsification_attempts": {
      "total": 5,
      "successful": 0
    }
  }
}
```
