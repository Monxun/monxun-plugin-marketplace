# AutoHD Discovery Reference

Automated Heuristics Discovery methodology for pattern generation.

## Overview

AutoHD (Automated Heuristics Discovery) is a methodology for generating reusable heuristics from observed patterns using LLM-based generation and evolutionary refinement.

## Core Process

```
┌─────────────────────────────────────────────────────────────┐
│  1. PROPOSAL                                                 │
│     LLM generates candidate heuristics from examples        │
├─────────────────────────────────────────────────────────────┤
│  2. EVALUATION                                               │
│     Score candidates against validation set                  │
├─────────────────────────────────────────────────────────────┤
│  3. EVOLUTION                                                │
│     Combine and mutate top performers                        │
├─────────────────────────────────────────────────────────────┤
│  4. CONVERGENCE                                              │
│     Iterate until stable or max iterations                   │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Heuristic Proposal

### Input Format
```json
{
  "examples": [
    {
      "input": "package.json with express dependency",
      "output": "Detected Express.js framework",
      "context": "Node.js project"
    }
  ],
  "domain": "framework_detection",
  "constraints": ["Must be fast", "Must handle edge cases"]
}
```

### Proposal Prompt
```
Given these examples of {domain}:

{examples}

Generate a heuristic function that:
1. Takes similar inputs
2. Produces similar outputs
3. Generalizes to unseen cases

Output as executable Python:
```

### Example Generated Heuristic
```python
def detect_express_framework(package_json: dict) -> tuple[bool, float]:
    """
    Detect if project uses Express.js framework.

    Returns: (detected, confidence)
    """
    dependencies = package_json.get('dependencies', {})
    dev_dependencies = package_json.get('devDependencies', {})

    # Direct detection
    if 'express' in dependencies:
        return True, 0.95

    # Indirect detection via common Express packages
    express_related = ['body-parser', 'cors', 'helmet', 'morgan']
    related_count = sum(1 for pkg in express_related if pkg in dependencies)

    if related_count >= 2:
        return True, 0.7 + (related_count * 0.05)

    return False, 0.0
```

## Step 2: Evaluation

### Scoring Function
```python
def evaluate_heuristic(heuristic, validation_set):
    """
    Evaluate heuristic against validation examples.

    Returns: score between 0 and 1
    """
    correct = 0
    total = len(validation_set)

    for example in validation_set:
        predicted, confidence = heuristic(example['input'])
        expected = example['expected_output']

        if predicted == expected:
            correct += 1
            # Bonus for high confidence correct predictions
            if confidence > 0.8:
                correct += 0.1

    return min(correct / total, 1.0)
```

### Validation Set Structure
```json
{
  "validation_set": [
    {
      "input": {"dependencies": {"express": "^4.18.0"}},
      "expected_output": true,
      "category": "direct_detection"
    },
    {
      "input": {"dependencies": {"fastify": "^4.0.0"}},
      "expected_output": false,
      "category": "negative_case"
    }
  ]
}
```

## Step 3: Evolution

### Selection
```python
def select_top_performers(candidates, scores, top_k=5):
    """Select top K heuristics by score."""
    sorted_pairs = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [c for c, s in sorted_pairs[:top_k]]
```

### Crossover
```python
def crossover_heuristics(h1, h2):
    """
    Combine two heuristics via LLM.

    Prompt: "Combine the strengths of these two heuristics..."
    """
    prompt = f"""
    Combine these two heuristics into a better one:

    Heuristic 1:
    {h1}

    Heuristic 2:
    {h2}

    Create a new heuristic that:
    - Combines the best aspects of both
    - Handles edge cases from both
    - Maintains readability
    """
    return llm_generate(prompt)
```

### Mutation
```python
def mutate_heuristic(heuristic, mutation_prompt):
    """
    Apply random mutation to heuristic.

    mutation_prompt examples:
    - "Add handling for edge case: empty dependencies"
    - "Improve performance by short-circuiting"
    - "Add more confidence granularity"
    """
    prompt = f"""
    Modify this heuristic:
    {heuristic}

    Modification: {mutation_prompt}
    """
    return llm_generate(prompt)
```

## Step 4: Convergence

### Stopping Criteria
```python
def check_convergence(history, threshold=0.01, window=3):
    """
    Check if evolution has converged.

    Converged if:
    - Best score hasn't improved by threshold in window iterations
    - OR max iterations reached
    """
    if len(history) < window:
        return False

    recent_scores = history[-window:]
    improvement = max(recent_scores) - min(recent_scores)

    return improvement < threshold
```

### Full Loop
```python
def autohd_discovery(examples, validation_set, max_iterations=10):
    """
    Full AutoHD discovery loop.
    """
    # Initial proposal
    candidates = [propose_heuristic(examples) for _ in range(5)]
    history = []

    for iteration in range(max_iterations):
        # Evaluate
        scores = [evaluate_heuristic(c, validation_set) for c in candidates]
        history.append(max(scores))

        # Check convergence
        if check_convergence(history):
            break

        # Select top performers
        top = select_top_performers(candidates, scores)

        # Evolution
        new_candidates = []
        for h in top:
            new_candidates.append(h)  # Keep original
            new_candidates.append(mutate_heuristic(h, random_mutation()))

        # Crossover pairs
        for i in range(0, len(top) - 1, 2):
            new_candidates.append(crossover_heuristics(top[i], top[i+1]))

        candidates = new_candidates

    # Return best
    final_scores = [evaluate_heuristic(c, validation_set) for c in candidates]
    best_idx = final_scores.index(max(final_scores))
    return candidates[best_idx], final_scores[best_idx]
```

## Output Format

```json
{
  "heuristic": {
    "id": "h_framework_detection_v3",
    "domain": "framework_detection",
    "code": "def detect_framework(config)...",
    "score": 0.94,
    "iterations": 7,
    "evolution_history": [0.75, 0.82, 0.88, 0.91, 0.93, 0.94, 0.94],
    "validation_results": {
      "true_positives": 45,
      "false_positives": 2,
      "true_negatives": 48,
      "false_negatives": 5
    }
  }
}
```
