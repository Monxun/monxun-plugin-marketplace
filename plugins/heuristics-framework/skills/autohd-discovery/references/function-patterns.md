# Heuristic Function Patterns

## Standard Function Signature

```python
def heuristic_name(current_state: Any, goal_state: Any) -> float:
    """
    Brief description of what this heuristic measures.

    Args:
        current_state: Current problem state representation
        goal_state: Target state to achieve

    Returns:
        float: Score where lower values indicate closer to goal
    """
    pass
```

## Common Pattern Types

### 1. Distance-Based Heuristic

```python
def heuristic_distance(current_state: dict, goal_state: dict) -> float:
    """Measure distance between current and goal states."""
    diff = 0.0
    for key in goal_state:
        if key in current_state:
            diff += abs(current_state[key] - goal_state[key])
    return diff
```

### 2. Feature-Based Heuristic

```python
def heuristic_features(current_state: dict, goal_state: dict) -> float:
    """Score based on feature presence/absence."""
    score = 0.0
    required_features = goal_state.get("required", [])

    for feature in required_features:
        if feature not in current_state.get("features", []):
            score += 1.0

    return score
```

### 3. Constraint-Based Heuristic

```python
def heuristic_constraints(current_state: dict, goal_state: dict) -> float:
    """Measure constraint violations."""
    violations = 0
    constraints = goal_state.get("constraints", [])

    for constraint in constraints:
        if not constraint.is_satisfied(current_state):
            violations += constraint.weight

    return float(violations)
```

### 4. Composite Heuristic

```python
def heuristic_composite(current_state: dict, goal_state: dict) -> float:
    """Combine multiple sub-heuristics with weights."""
    weights = {"distance": 0.4, "features": 0.3, "constraints": 0.3}

    score = 0.0
    score += weights["distance"] * heuristic_distance(current_state, goal_state)
    score += weights["features"] * heuristic_features(current_state, goal_state)
    score += weights["constraints"] * heuristic_constraints(current_state, goal_state)

    return score
```

## Domain-Specific Patterns

### Code Quality Heuristic

```python
def heuristic_code_quality(code_state: dict, quality_goal: dict) -> float:
    """Evaluate code against quality metrics."""
    score = 0.0

    # Complexity penalty
    max_complexity = quality_goal.get("max_complexity", 10)
    actual_complexity = code_state.get("cyclomatic_complexity", 0)
    if actual_complexity > max_complexity:
        score += (actual_complexity - max_complexity) * 0.1

    # Nesting penalty
    max_nesting = quality_goal.get("max_nesting", 3)
    actual_nesting = code_state.get("max_nesting_depth", 0)
    if actual_nesting > max_nesting:
        score += (actual_nesting - max_nesting) * 0.2

    # Test coverage bonus (negative penalty)
    min_coverage = quality_goal.get("min_coverage", 80)
    actual_coverage = code_state.get("test_coverage", 0)
    if actual_coverage < min_coverage:
        score += (min_coverage - actual_coverage) * 0.01

    return max(0.0, score)
```

### Search Problem Heuristic

```python
def heuristic_search(state: tuple, goal: tuple) -> float:
    """Manhattan distance for grid-based search."""
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
```

## Best Practices

1. **Admissibility**: Never overestimate actual cost
2. **Consistency**: h(n) ≤ c(n, n') + h(n')
3. **Efficiency**: O(1) or O(n) complexity preferred
4. **Handling Edge Cases**: Return 0 for goal state
5. **Type Safety**: Use type hints
6. **Documentation**: Clear docstrings
