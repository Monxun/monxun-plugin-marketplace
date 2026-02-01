# Evolution Operators for Heuristic Synthesis

## Mutation Operators

### 1. Weight Tuning

Adjust numeric weights by small amounts:

```python
def mutate_weight(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Adjust weight by ±10% with Gaussian noise.
    """
    current_weight = heuristic.weights[factor_name]
    noise = np.random.normal(0, 0.05)  # 5% std dev
    new_weight = current_weight * (1 + noise)

    # Ensure weights sum to 1.0
    new_weight = max(0.05, min(0.5, new_weight))

    heuristic.weights[factor_name] = new_weight
    heuristic.normalize_weights()

    return heuristic
```

### 2. Threshold Shift

Modify normalization thresholds:

```python
def mutate_threshold(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Adjust normalization threshold by ±15%.
    """
    current_threshold = heuristic.thresholds[factor_name]
    multiplier = np.random.uniform(0.85, 1.15)
    new_threshold = current_threshold * multiplier

    heuristic.thresholds[factor_name] = new_threshold
    return heuristic
```

### 3. Condition Addition

Add new context checks:

```python
def mutate_add_condition(heuristic: Heuristic, context_keys: list[str]) -> Heuristic:
    """
    Add a new factor from available context keys.
    """
    available = set(context_keys) - set(heuristic.factors.keys())

    if available:
        new_factor = random.choice(list(available))
        heuristic.factors[new_factor] = {
            "weight": 0.1,
            "threshold": estimate_threshold(new_factor),
            "operation": "min_normalize"
        }
        heuristic.normalize_weights()

    return heuristic
```

### 4. Condition Removal

Remove weak or redundant factors:

```python
def mutate_remove_condition(heuristic: Heuristic) -> Heuristic:
    """
    Remove lowest-weighted factor if multiple exist.
    """
    if len(heuristic.factors) > 2:
        weakest = min(heuristic.factors.items(), key=lambda x: x[1]["weight"])
        del heuristic.factors[weakest[0]]
        heuristic.normalize_weights()

    return heuristic
```

### 5. Logic Inversion

Try opposite conditions:

```python
def mutate_invert_logic(heuristic: Heuristic, factor_name: str) -> Heuristic:
    """
    Invert factor logic (high→low or low→high).
    """
    factor = heuristic.factors[factor_name]

    if factor["operation"] == "min_normalize":
        factor["operation"] = "max_normalize"
    elif factor["operation"] == "max_normalize":
        factor["operation"] = "min_normalize"

    return heuristic
```

## Crossover Operators

### 1. Factor Exchange

Swap factors between parent heuristics:

```python
def crossover_factor_exchange(
    parent1: Heuristic,
    parent2: Heuristic
) -> tuple[Heuristic, Heuristic]:
    """
    Exchange random factors between parents.
    """
    child1 = parent1.copy()
    child2 = parent2.copy()

    common_factors = set(parent1.factors.keys()) & set(parent2.factors.keys())

    if common_factors:
        factor = random.choice(list(common_factors))
        child1.factors[factor] = parent2.factors[factor].copy()
        child2.factors[factor] = parent1.factors[factor].copy()

    return child1, child2
```

### 2. Weight Averaging

Average weights of similar factors:

```python
def crossover_weight_average(
    parent1: Heuristic,
    parent2: Heuristic
) -> Heuristic:
    """
    Create child with averaged weights from parents.
    """
    child = parent1.copy()

    for factor in child.factors:
        if factor in parent2.factors:
            w1 = parent1.factors[factor]["weight"]
            w2 = parent2.factors[factor]["weight"]
            child.factors[factor]["weight"] = (w1 + w2) / 2

    child.normalize_weights()
    return child
```

### 3. Structure Merge

Combine structural patterns:

```python
def crossover_structure_merge(
    parent1: Heuristic,
    parent2: Heuristic
) -> Heuristic:
    """
    Merge factors from both parents.
    """
    child = Heuristic()

    # Take all factors from both parents
    all_factors = set(parent1.factors.keys()) | set(parent2.factors.keys())

    for factor in all_factors:
        if factor in parent1.factors and factor in parent2.factors:
            # Average if in both
            child.factors[factor] = {
                "weight": (parent1.factors[factor]["weight"] +
                          parent2.factors[factor]["weight"]) / 2,
                "threshold": (parent1.factors[factor]["threshold"] +
                             parent2.factors[factor]["threshold"]) / 2,
                "operation": random.choice([
                    parent1.factors[factor]["operation"],
                    parent2.factors[factor]["operation"]
                ])
            }
        elif factor in parent1.factors:
            child.factors[factor] = parent1.factors[factor].copy()
        else:
            child.factors[factor] = parent2.factors[factor].copy()

    child.normalize_weights()
    return child
```

## Selection Strategies

### Tournament Selection

```python
def tournament_select(
    population: list[Heuristic],
    tournament_size: int = 3
) -> Heuristic:
    """
    Select winner from random tournament.
    """
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda h: h.fitness)
```

### Elitism

```python
def apply_elitism(
    population: list[Heuristic],
    elite_count: int = 2
) -> list[Heuristic]:
    """
    Preserve top performers across generations.
    """
    sorted_pop = sorted(population, key=lambda h: h.fitness, reverse=True)
    return sorted_pop[:elite_count]
```

## Evolution Loop

```python
def evolve_heuristics(
    initial_population: list[Heuristic],
    validation_set: list[Example],
    max_generations: int = 10,
    mutation_rate: float = 0.3,
    crossover_rate: float = 0.7
) -> Heuristic:
    """
    Main evolution loop.
    """
    population = initial_population

    for generation in range(max_generations):
        # Evaluate fitness
        for heuristic in population:
            heuristic.fitness = evaluate(heuristic, validation_set)

        # Check convergence
        best = max(population, key=lambda h: h.fitness)
        if best.fitness > 0.95:
            break

        # Selection and reproduction
        new_population = apply_elitism(population)

        while len(new_population) < len(population):
            if random.random() < crossover_rate:
                p1 = tournament_select(population)
                p2 = tournament_select(population)
                child, _ = crossover_factor_exchange(p1, p2)
            else:
                child = tournament_select(population).copy()

            if random.random() < mutation_rate:
                child = apply_random_mutation(child)

            new_population.append(child)

        population = new_population

    return max(population, key=lambda h: h.fitness)
```
