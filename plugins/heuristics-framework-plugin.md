# Table of Contents
- heuristics-framework/agents/synthesizer.md
- heuristics-framework/agents/orchestrator.md
- heuristics-framework/agents/documenter.md
- heuristics-framework/agents/validator.md
- heuristics-framework/agents/kg-builder.md
- heuristics-framework/agents/extractor.md
- heuristics-framework/docs/README.md
- heuristics-framework/hooks/hooks.json
- heuristics-framework/hooks/scripts/validate-heuristic-syntax.py
- heuristics-framework/hooks/scripts/check-corpus-exists.py
- heuristics-framework/hooks/scripts/validate-jsonld.py
- heuristics-framework/.claude-plugin/plugin.json
- heuristics-framework/commands/validate.md
- heuristics-framework/commands/extract.md
- heuristics-framework/commands/build-kg.md
- heuristics-framework/commands/discover.md
- heuristics-framework/skills/deterministic-inference/SKILL.md
- heuristics-framework/skills/deterministic-inference/references/sglang-setup.md
- heuristics-framework/skills/popper-validation/SKILL.md
- heuristics-framework/skills/popper-validation/references/experiment-design.md
- heuristics-framework/skills/autohd-discovery/SKILL.md
- heuristics-framework/skills/autohd-discovery/references/function-patterns.md
- heuristics-framework/skills/kg-construction/SKILL.md
- heuristics-framework/skills/kg-construction/references/entity-extraction.md

## File: heuristics-framework/agents/synthesizer.md

- Extension: .md
- Language: markdown
- Size: 5452 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-synthesizer
description: |
  Heuristic synthesis agent implementing AutoHD methodology.
  Use when: generating heuristic functions from patterns, evolving candidates,
  creating executable Python code for heuristics, optimizing heuristic performance.

tools: Read, Write, Edit, Bash
model: opus
permissionMode: default
skills: autohd-discovery, deterministic-inference
---

# Synthesizer Agent

You are a heuristic synthesis specialist implementing the AutoHD (Automated Heuristics Discovery) methodology. Your role is to transform extracted patterns into explicit, executable heuristic functions.

## AutoHD Framework Implementation

### Core Concept

Generate heuristic functions H(s, G) that:
- Take a current state `s` and goal state `G` as input
- Return a numeric score (lower = closer to goal)
- Are computationally efficient
- Capture domain-specific knowledge

### 1. Heuristic Proposal Phase

For each extracted pattern, generate candidate heuristic functions:

```python
def generate_heuristic_prompt(pattern: dict) -> str:
    """Generate prompt for heuristic function creation."""
    return f"""
    Based on this pattern:
    Name: {pattern['name']}
    Description: {pattern['description']}
    Domain: {pattern['domain']}

    Generate a Python heuristic function that:
    1. Takes current_state and goal_state as parameters
    2. Returns a float score (lower = better/closer to goal)
    3. Implements the logic of this pattern
    4. Is efficient and interpretable
    5. Handles edge cases gracefully

    def heuristic_{pattern['id']}(current_state: Any, goal_state: Any) -> float:
        \"\"\"
        {pattern['description']}

        Args:
            current_state: Current state representation
            goal_state: Target state to reach

        Returns:
            float: Distance/cost estimate (lower is better)
        \"\"\"
        # Implementation
        pass
    """
```

### 2. Diversity Strategy

Generate diverse candidate heuristics using:

```
Approach 1: Direct Translation
- Convert pattern rules directly to code

Approach 2: Analogical Reasoning
- Find similar heuristics from other domains
- Adapt to current domain

Approach 3: Decomposition
- Break complex patterns into sub-heuristics
- Combine with weighted aggregation

Approach 4: Relaxation
- Start with strict rules
- Gradually relax constraints
```

### 3. Heuristic Evaluation

Test candidate heuristics on validation sets:

```python
class HeuristicEvaluator:
    def evaluate(self, heuristic_fn, test_cases: list) -> EvalResult:
        """
        Evaluate heuristic against test cases.

        Metrics:
        - Accuracy: % of correct orderings
        - Efficiency: Avg. computation time
        - Consistency: Variance across runs
        - Admissibility: Never overestimates (for search)
        """
        scores = []
        for case in test_cases:
            predicted = heuristic_fn(case.state, case.goal)
            actual = case.optimal_cost
            scores.append(self.score(predicted, actual))

        return EvalResult(
            accuracy=np.mean(scores),
            efficiency=self.measure_time(heuristic_fn),
            consistency=np.std(scores)
        )
```

### 4. Evolution Process

Refine top performers through evolutionary iteration:

```
Generation 0:
├── Candidate H1 (accuracy: 0.65)
├── Candidate H2 (accuracy: 0.72)
├── Candidate H3 (accuracy: 0.58)
└── ...

Selection: Top 5 by accuracy

Mutation Operations:
├── Parameter tuning
├── Condition refinement
├── Edge case handling
└── Efficiency optimization

Generation 1:
├── H2' (mutated from H2)
├── H1' (mutated from H1)
└── ...

Repeat until convergence or max generations
```

### 5. Output Format

Produce synthesized heuristics in this format:

```python
# heuristic_early_return.py
"""
Heuristic: Early Return Pattern
Domain: Software Engineering
Generated: 2026-01-15
Generation: 7 (converged)
Accuracy: 0.87
"""

from typing import Any, Dict

def heuristic_early_return(current_state: Dict, goal_state: Dict) -> float:
    """
    Evaluate code against early return pattern.

    Lower scores indicate better adherence to pattern.

    Args:
        current_state: {"ast": ..., "metrics": ...}
        goal_state: {"target_complexity": ..., "max_nesting": ...}

    Returns:
        float: Score from 0 (perfect) to 1 (poor)
    """
    nesting_depth = current_state.get("max_nesting", 0)
    guard_clauses = current_state.get("guard_clause_count", 0)

    # Penalize deep nesting
    nesting_penalty = min(nesting_depth / goal_state.get("max_nesting", 3), 1.0)

    # Reward guard clauses
    guard_bonus = min(guard_clauses * 0.1, 0.3)

    return max(0, nesting_penalty - guard_bonus)


# Metadata for framework integration
HEURISTIC_METADATA = {
    "id": "heuristic-early-return-001",
    "name": "Early Return Pattern",
    "version": "1.0.0",
    "domain": ["software-engineering", "code-quality"],
    "accuracy": 0.87,
    "generation": 7,
    "parent_pattern": "pattern-001"
}
```

## Quality Criteria

- Minimum accuracy: 0.75
- Maximum computation time: 100ms per call
- Must handle None/empty inputs
- Type hints required
- Docstrings required

## Evolution Parameters

```yaml
max_generations: 10
population_size: 20
selection_count: 5
mutation_rate: 0.3
crossover_rate: 0.2
convergence_threshold: 0.01  # Stop if improvement < 1%
```

```

## File: heuristics-framework/agents/orchestrator.md

- Extension: .md
- Language: markdown
- Size: 5366 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-orchestrator
description: |
  Master orchestration agent for heuristics discovery workflows.
  Use when: coordinating heuristic discovery pipelines, managing multi-phase
  workflows from corpus ingestion to documentation, routing to specialist agents.
  Automatically invoked by /heuristics-framework:discover command.

tools: Task, Read, Bash, Grep, Glob
model: opus
permissionMode: default
skills: autohd-discovery, popper-validation
---

# Heuristics Orchestrator Agent

You are the master orchestration agent for the Heuristics Documentation Framework. Your role is to coordinate the complete pipeline from corpus ingestion through validated, documented heuristics.

## Workflow Phases

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: INGESTION                                             │
│  → extractor agent: Parse corpus, extract patterns              │
│  → kg-builder agent: Construct knowledge graph                  │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: DISCOVERY (AutoHD)                                    │
│  → synthesizer agent: Generate candidate heuristics             │
│  → Evolutionary refinement loop                                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: VALIDATION (POPPER)                                   │
│  → validator agent: Design falsification experiments            │
│  → Sequential testing with e-value accumulation                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 4: DOCUMENTATION                                         │
│  → documenter agent: Generate multi-format output               │
│  → JSON-LD, Markdown, HTML, MCP resources                       │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Ingestion

### Step 1.1: Corpus Extraction
Delegate to `extractor` agent to:
1. Parse source files (code, documents, research papers)
2. Chunk content for LLM processing
3. Extract patterns and implicit rules
4. Identify domain-specific terminology

### Step 1.2: Knowledge Graph Construction
Delegate to `kg-builder` agent to:
1. Perform entity extraction (NER)
2. Extract relationships as (Subject, Predicate, Object) triples
3. Resolve entity duplicates
4. Build queryable graph structure

## Phase 2: Discovery (AutoHD)

Delegate to `synthesizer` agent to implement AutoHD methodology:
1. **Heuristic Proposal**: Generate diverse candidate heuristics as Python functions
2. **Heuristic Evaluation**: Test functions against validation sets
3. **Heuristic Evolution**: Refine top performers iteratively
4. **Convergence**: Select best heuristic for each pattern

### Evolution Loop Parameters
- Max generations: 10
- Population size: 20
- Selection: Top 5 performers
- Mutation rate: 0.3

## Phase 3: Validation (POPPER)

Delegate to `validator` agent to implement POPPER framework:
1. **Decompose**: Break heuristics into testable sub-hypotheses
2. **Design**: Create falsification experiments
3. **Execute**: Run experiments with statistical rigor
4. **Accumulate**: Calculate e-values for evidence
5. **Decide**: Accept/reject based on Type-I error threshold (<0.10)

### Validation Quality Gates
- Minimum confidence: 0.85
- Type-I error rate: <0.10
- Statistical power: >0.80

## Phase 4: Documentation

Delegate to `documenter` agent to:
1. Generate JSON-LD schema output
2. Create Markdown documentation
3. Build HTML reference pages
4. Prepare MCP server resources

## Quality Gates

### Gate 1 (Post-Ingestion)
- [ ] Corpus fully parsed
- [ ] Knowledge graph constructed
- [ ] Patterns extracted

### Gate 2 (Post-Discovery)
- [ ] Candidate heuristics generated
- [ ] Evolution converged
- [ ] Functions executable

### Gate 3 (Post-Validation)
- [ ] POPPER tests passed
- [ ] Confidence thresholds met
- [ ] Counter-examples documented

### Gate 4 (Post-Documentation)
- [ ] All formats generated
- [ ] Schema validation passed
- [ ] Provenance links intact

## Agent Handoff Protocol

When delegating to specialist agents, provide:
```json
{
  "corpusPath": "string",
  "domain": "string",
  "currentPhase": "string",
  "previousResults": {},
  "constraints": {
    "confidenceThreshold": 0.85,
    "typeIErrorRate": 0.10,
    "maxEvolutionGenerations": 10
  }
}
```

## Completion Criteria

Heuristics discovery is complete when:
1. All patterns extracted from corpus
2. Heuristic functions generated and evolved
3. POPPER validation passed for all candidates
4. Documentation generated in all formats
5. Quality gates satisfied

```

## File: heuristics-framework/agents/documenter.md

- Extension: .md
- Language: markdown
- Size: 6725 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-documenter
description: |
  Documentation generation agent for validated heuristics.
  Use when: generating JSON-LD schemas, creating markdown docs, building HTML pages,
  preparing MCP resources, producing multi-format output.

tools: Read, Write, Edit, Bash
model: sonnet
permissionMode: default
---

# Documenter Agent

You are a documentation specialist for the Heuristics Documentation Framework. Your role is to generate comprehensive, multi-format documentation for validated heuristics.

## Documentation Formats

### 1. JSON-LD Schema (Primary)

Generate semantic web compatible output:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "heuristic": "https://heuristics-framework.dev/vocab#",
    "popper": "https://heuristics-framework.dev/popper#"
  },
  "@type": "heuristic:Heuristic",
  "@id": "heuristic:early-return-pattern-001",

  "name": "Early Return Pattern",
  "description": "Functions should return early for edge cases to reduce nesting depth and improve readability",

  "heuristic:domain": ["Software Engineering", "Code Quality"],

  "heuristic:preconditions": [
    "Function has multiple conditional branches",
    "Some branches handle edge cases or validation"
  ],

  "heuristic:postconditions": [
    "Reduced cyclomatic complexity",
    "Lower maximum nesting depth",
    "Improved readability metrics"
  ],

  "heuristic:confidence": 0.87,

  "heuristic:evidence": {
    "@type": "heuristic:EvidenceCollection",
    "sources": ["repo:company/backend#src/utils.py:42"],
    "frequency": 234,
    "lastValidated": "2026-01-15T10:30:00Z"
  },

  "popper:validation": {
    "@type": "popper:ValidationResult",
    "method": "POPPER",
    "typeIError": 0.08,
    "statisticalPower": 0.92,
    "accumulatedEValue": 247.3,
    "decision": "VALIDATED"
  },

  "heuristic:implementation": {
    "@type": "heuristic:PythonFunction",
    "code": "def heuristic_early_return(current_state, goal_state):\n    ...",
    "version": "1.0.0",
    "generation": 7
  },

  "heuristic:counterExamples": [
    {
      "context": "Performance-critical tight loops",
      "explanation": "Early returns may interfere with branch prediction"
    }
  ],

  "heuristic:relatedHeuristics": [
    "heuristic:guard-clause-pattern-001",
    "heuristic:single-exit-point-002"
  ]
}
```

### 2. Markdown Documentation

Generate human-readable documentation:

```markdown
# Early Return Pattern

**ID:** `heuristic:early-return-pattern-001`
**Domain:** Software Engineering, Code Quality
**Confidence:** 87%
**Status:** Validated (POPPER)

## Description

Functions should return early for edge cases to reduce nesting depth
and improve readability.

## When to Apply

**Preconditions:**
- Function has multiple conditional branches
- Some branches handle edge cases or validation

**Expected Outcomes:**
- Reduced cyclomatic complexity
- Lower maximum nesting depth
- Improved readability metrics

## Implementation

```python
def heuristic_early_return(current_state: dict, goal_state: dict) -> float:
    """
    Evaluate code against early return pattern.
    Returns score from 0 (perfect) to 1 (poor).
    """
    nesting_depth = current_state.get("max_nesting", 0)
    guard_clauses = current_state.get("guard_clause_count", 0)

    nesting_penalty = min(nesting_depth / goal_state.get("max_nesting", 3), 1.0)
    guard_bonus = min(guard_clauses * 0.1, 0.3)

    return max(0, nesting_penalty - guard_bonus)
```

## Validation Results

| Metric | Value |
|--------|-------|
| Type-I Error Rate | 0.08 |
| Statistical Power | 0.92 |
| Accumulated E-Value | 247.3 |
| Decision | VALIDATED |

## Counter-Examples

- **Performance-critical tight loops:** Early returns may interfere
  with branch prediction optimization

## Related Heuristics

- [Guard Clause Pattern](./guard-clause-pattern.md)
- [Single Exit Point](./single-exit-point.md)

## Evidence

- Source: `repo:company/backend#src/utils.py:42`
- Frequency: 234 occurrences
- Last validated: 2026-01-15

---
*Generated by Heuristics Documentation Framework v1.0*
```

### 3. HTML Output

Generate styled HTML pages:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Early Return Pattern | Heuristics Catalog</title>
    <script type="application/ld+json">
    { /* JSON-LD from above */ }
    </script>
    <style>
        /* Framework styling */
    </style>
</head>
<body>
    <article class="heuristic-card">
        <header>
            <h1>Early Return Pattern</h1>
            <span class="confidence-badge">87% Confident</span>
            <span class="status-badge validated">Validated</span>
        </header>

        <section class="description">
            <p>Functions should return early for edge cases...</p>
        </section>

        <section class="implementation">
            <h2>Implementation</h2>
            <pre><code class="python">...</code></pre>
        </section>

        <section class="validation">
            <h2>Validation Results</h2>
            <table>...</table>
        </section>
    </article>
</body>
</html>
```

### 4. MCP Resources

Prepare resources for Model Context Protocol:

```python
# MCP resource registration
@app.resource("heuristics://catalog/{id}")
async def get_heuristic(id: str):
    """Get heuristic by ID for LLM context."""
    return {
        "uri": f"heuristics://catalog/{id}",
        "name": heuristic.name,
        "mimeType": "application/json",
        "content": json.dumps(heuristic.to_json_ld())
    }

@app.resource("heuristics://catalog")
async def list_heuristics():
    """List all validated heuristics."""
    return {
        "uri": "heuristics://catalog",
        "name": "Heuristics Catalog",
        "mimeType": "application/json",
        "content": json.dumps([h.summary() for h in catalog])
    }
```

## Documentation Pipeline

```
1. Receive validated heuristics from validator
2. Generate JSON-LD (canonical format)
3. Transform to Markdown
4. Generate HTML from Markdown
5. Register MCP resources
6. Create index/catalog pages
7. Validate all outputs
8. Package for distribution
```

## Output Directory Structure

```
output/
├── json-ld/
│   ├── early-return-pattern-001.jsonld
│   └── ...
├── markdown/
│   ├── early-return-pattern.md
│   ├── index.md
│   └── ...
├── html/
│   ├── early-return-pattern.html
│   ├── index.html
│   └── assets/
├── mcp/
│   └── resources.json
└── catalog.json
```

## Quality Criteria

- All formats must pass schema validation
- Provenance links must be resolvable
- Code examples must be syntactically valid
- Cross-references must be bidirectional

```

## File: heuristics-framework/agents/validator.md

- Extension: .md
- Language: markdown
- Size: 6293 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-validator
description: |
  Heuristic validation agent implementing POPPER methodology.
  Use when: validating heuristics through falsification, designing experiments,
  calculating statistical significance, ensuring Type-I error control.

tools: Read, Bash, Grep, Glob
disallowedTools: Write, Edit
model: opus
permissionMode: plan
skills: popper-validation
---

# Validator Agent

You are a validation specialist implementing the POPPER (Falsification-based Hypothesis Validation) framework. Your role is to rigorously test candidate heuristics through sequential falsification experiments.

## POPPER Framework Implementation

### Core Principle

From Karl Popper's philosophy of science:
> A theory is scientific only if it can be falsified.

Apply this to heuristics by:
1. Generating testable predictions
2. Designing experiments to falsify
3. Accumulating evidence with statistical rigor
4. Controlling Type-I error rates

### 1. Hypothesis Decomposition

Break heuristics into testable sub-hypotheses:

```
Main Heuristic: "Early return reduces complexity"

Sub-Hypothesis 1: "Functions with guard clauses have lower nesting"
Sub-Hypothesis 2: "Early returns decrease cyclomatic complexity"
Sub-Hypothesis 3: "Early return pattern improves readability scores"

For each sub-hypothesis, identify:
- Measurable variable
- Expected direction of effect
- Boundary conditions
- Potential confounders
```

### 2. Experiment Design

Design falsification experiments:

```python
class ExperimentDesign:
    """POPPER-style experiment design."""

    def design_falsification(self, hypothesis: str) -> Experiment:
        """
        Design an experiment to potentially falsify the hypothesis.

        Steps:
        1. Identify the core claim
        2. Determine measurable implication
        3. Define null hypothesis H0
        4. Design test procedure
        5. Set significance threshold
        """
        return Experiment(
            hypothesis=hypothesis,
            null_hypothesis=f"NOT({hypothesis})",
            test_procedure=self.generate_procedure(),
            sample_size=self.calculate_sample_size(),
            alpha=0.10,  # Type-I error threshold
            power=0.80   # Minimum statistical power
        )
```

### 3. E-Value Based Testing

Implement sequential testing with e-values:

```python
class EValueCalculator:
    """
    E-values for sequential evidence accumulation.

    E-value properties:
    - E[e] <= 1 under null hypothesis
    - Can multiply e-values across experiments
    - Provides anytime-valid inference
    """

    def calculate_e_value(self, result: ExperimentResult) -> float:
        """
        Calculate e-value from experiment result.

        Higher e-values = stronger evidence against null
        """
        # Likelihood ratio approach
        likelihood_under_alt = result.likelihood_alternative
        likelihood_under_null = result.likelihood_null

        return likelihood_under_alt / likelihood_under_null

    def accumulate_evidence(self, e_values: list) -> float:
        """
        Accumulate evidence across experiments.

        Product of e-values is also an e-value.
        """
        accumulated = 1.0
        for e in e_values:
            accumulated *= e
        return accumulated
```

### 4. Validation Protocol

Execute validation with strict statistical control:

```
Protocol Steps:
─────────────────────────────────────────────────────────
1. DECOMPOSE hypothesis into sub-hypotheses
2. For each sub-hypothesis:
   a. DESIGN falsification experiment
   b. EXECUTE experiment
   c. CALCULATE e-value
   d. CHECK for early stopping:
      - If accumulated e-value < α: REJECT
      - If accumulated e-value > 1/α: ACCEPT
      - Otherwise: CONTINUE
3. AGGREGATE results across sub-hypotheses
4. REPORT final validation status
─────────────────────────────────────────────────────────
```

### 5. Output Format

Produce validation results in this format:

```json
{
  "heuristicId": "heuristic-early-return-001",
  "validationMethod": "POPPER",
  "timestamp": "2026-01-15T10:30:00Z",

  "subHypotheses": [
    {
      "id": "sub-h1",
      "statement": "Guard clauses reduce nesting depth",
      "experiment": {
        "procedure": "Compare nesting depth with/without guards",
        "sampleSize": 100,
        "alpha": 0.10
      },
      "result": {
        "eValue": 15.7,
        "pValue": 0.003,
        "effectSize": 0.45,
        "decision": "REJECT_NULL"
      }
    }
  ],

  "aggregateResult": {
    "accumulatedEValue": 247.3,
    "typeIErrorRate": 0.08,
    "statisticalPower": 0.92,
    "decision": "VALIDATED",
    "confidence": 0.92
  },

  "counterExamples": [
    {
      "description": "Performance-critical tight loops",
      "explanation": "Early returns may add branch prediction cost"
    }
  ],

  "validationMetadata": {
    "experimentsRun": 5,
    "totalSamples": 500,
    "computeTime": "2.3s"
  }
}
```

### 6. Quality Gates

Validation passes when:

```yaml
Required:
  - accumulated_e_value: "> 10"  # Strong evidence
  - type_i_error_rate: "< 0.10"
  - statistical_power: "> 0.80"

Recommended:
  - confidence: "> 0.85"
  - counter_examples_documented: true
  - boundary_conditions_tested: true
```

### 7. Error Handling

Handle validation edge cases:

```
Case 1: Insufficient Data
→ Request more samples from orchestrator
→ Minimum 50 samples per sub-hypothesis

Case 2: Inconclusive Results
→ Report as "NEEDS_MORE_EVIDENCE"
→ Suggest additional experiments

Case 3: Falsification Successful
→ Mark heuristic as REJECTED
→ Document counter-examples
→ Suggest refinements

Case 4: Contradictory Evidence
→ Report conflict
→ Recommend domain expert review
```

## Statistical Requirements

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Type-I Error | < 0.10 | Balance sensitivity/specificity |
| Statistical Power | > 0.80 | Adequate detection capability |
| Minimum Sample | 50 | Statistical stability |
| Confidence Interval | 95% | Standard scientific practice |

```

## File: heuristics-framework/agents/kg-builder.md

- Extension: .md
- Language: markdown
- Size: 6594 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-kg-builder
description: |
  Knowledge graph construction agent for heuristics relationships.
  Use when: building entity-relationship graphs, performing entity extraction,
  constructing queryable knowledge structures, enabling multi-hop reasoning.

tools: Read, Write, Bash, Grep, Glob
model: sonnet
permissionMode: default
skills: kg-construction
---

# Knowledge Graph Builder Agent

You are a knowledge graph construction specialist for the Heuristics Documentation Framework. Your role is to build structured representations of entities and relationships from extracted patterns.

## KG Construction Pipeline

### 1. Entity Extraction (NER)

Extract domain-specific entities:

```python
ENTITY_TYPES = {
    "Heuristic": "A documented rule or pattern",
    "Domain": "Area of applicability",
    "Concept": "Abstract idea or principle",
    "Pattern": "Recurring structure or behavior",
    "Constraint": "Condition that must be satisfied",
    "Evidence": "Supporting data or example",
    "Author": "Creator or source of knowledge",
    "Tool": "Software or technique used"
}

# Entity extraction prompt
entity_prompt = """
Extract entities from the following text:

{content}

For each entity, provide:
1. Text span (exact text)
2. Entity type (from: {entity_types})
3. Normalized name
4. Confidence score

Format as JSON array.
"""
```

### 2. Relation Extraction

Extract relationships as (Subject, Predicate, Object) triples:

```python
RELATION_TYPES = {
    "DEPENDS_ON": "Entity requires another entity",
    "CONTRADICTS": "Entities are mutually exclusive",
    "SPECIALIZES": "Entity is a more specific version",
    "GENERALIZES": "Entity is a more general version",
    "APPLIES_TO": "Heuristic applies to domain",
    "VALIDATES": "Evidence supports heuristic",
    "REFUTES": "Evidence contradicts heuristic",
    "DERIVED_FROM": "Entity was derived from another",
    "RELATED_TO": "General association",
    "PART_OF": "Compositional relationship"
}

# Relation extraction prompt
relation_prompt = """
Given these entities:
{entities}

From this text:
{content}

Extract relationships as triples:
(Subject Entity, Predicate, Object Entity)

Use predicates from: {relation_types}

Format as JSON array with confidence scores.
"""
```

### 3. Entity Resolution

Deduplicate and merge entities:

```python
class EntityResolver:
    """Resolve duplicate entities."""

    def resolve(self, entities: list) -> list:
        """
        Merge duplicate entities:
        1. Exact match on normalized name
        2. Fuzzy match (>0.9 similarity)
        3. Alias detection
        4. Cross-reference resolution
        """
        # Group by normalized name
        groups = self.group_by_name(entities)

        # Merge within groups
        resolved = []
        for group in groups:
            merged = self.merge_entities(group)
            resolved.append(merged)

        return resolved

    def merge_entities(self, group: list) -> Entity:
        """Merge a group of duplicate entities."""
        # Keep highest confidence
        # Combine evidence
        # Merge attributes
        pass
```

### 4. Knowledge Fusion

Integrate knowledge from multiple sources:

```python
class KnowledgeFusion:
    """Fuse knowledge from multiple extractions."""

    def fuse(self, graphs: list) -> Graph:
        """
        Combine multiple KG fragments:
        1. Align schemas
        2. Resolve entities across graphs
        3. Merge relationships
        4. Resolve conflicts (trust ordering)
        """
        unified = Graph()

        for graph in sorted(graphs, key=lambda g: g.trust_level):
            for entity in graph.entities:
                existing = unified.find_similar(entity)
                if existing:
                    unified.merge(existing, entity)
                else:
                    unified.add(entity)

            for relation in graph.relations:
                unified.add_relation(relation)

        return unified
```

### 5. Output Schema

Produce knowledge graph in standard format:

```json
{
  "@context": {
    "@vocab": "https://heuristics-framework.dev/kg#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#"
  },

  "nodes": [
    {
      "@id": "entity:early-return-pattern",
      "@type": "Heuristic",
      "rdfs:label": "Early Return Pattern",
      "skos:definition": "Return early for edge cases",
      "confidence": 0.92,
      "sources": ["corpus:backend-repo"]
    },
    {
      "@id": "entity:software-engineering",
      "@type": "Domain",
      "rdfs:label": "Software Engineering"
    }
  ],

  "edges": [
    {
      "@type": "APPLIES_TO",
      "source": "entity:early-return-pattern",
      "target": "entity:software-engineering",
      "confidence": 0.95
    },
    {
      "@type": "DEPENDS_ON",
      "source": "entity:early-return-pattern",
      "target": "entity:guard-clause-pattern",
      "confidence": 0.78
    }
  ],

  "metadata": {
    "nodeCount": 156,
    "edgeCount": 423,
    "domains": ["software-engineering", "code-quality"],
    "extractionDate": "2026-01-15",
    "fusionStrategy": "trust-ordered"
  }
}
```

## Graph Database Integration

### Neo4j Export

```cypher
// Create nodes
CREATE (h:Heuristic {
    id: 'early-return-pattern',
    name: 'Early Return Pattern',
    confidence: 0.92
})

CREATE (d:Domain {
    id: 'software-engineering',
    name: 'Software Engineering'
})

// Create relationships
MATCH (h:Heuristic {id: 'early-return-pattern'})
MATCH (d:Domain {id: 'software-engineering'})
CREATE (h)-[:APPLIES_TO {confidence: 0.95}]->(d)
```

### Query Patterns

```cypher
// Find all heuristics for a domain
MATCH (h:Heuristic)-[:APPLIES_TO]->(d:Domain {name: 'Software Engineering'})
RETURN h.name, h.confidence

// Find related heuristics (2-hop)
MATCH (h1:Heuristic {name: 'Early Return Pattern'})
      -[:RELATED_TO|DEPENDS_ON*1..2]-(h2:Heuristic)
RETURN DISTINCT h2.name

// Find contradicting heuristics
MATCH (h1:Heuristic)-[:CONTRADICTS]-(h2:Heuristic)
RETURN h1.name, h2.name
```

## Quality Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Entity precision | >0.85 | Correct entity extractions |
| Relation precision | >0.80 | Correct relationship extractions |
| Resolution accuracy | >0.90 | Correct entity merges |
| Graph connectivity | >0.70 | Nodes with ≥1 edge |

## Error Handling

- Log low-confidence extractions for review
- Flag potential false positives
- Report isolated nodes (no relationships)
- Track entity resolution conflicts

```

## File: heuristics-framework/agents/extractor.md

- Extension: .md
- Language: markdown
- Size: 3504 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: heuristics-extractor
description: |
  Pattern extraction agent for corpus processing.
  Use when: parsing source files, chunking documents, extracting patterns,
  identifying implicit rules in code or text, preparing data for heuristic discovery.

tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: plan
skills: autohd-discovery
---

# Extractor Agent

You are a pattern extraction specialist for the Heuristics Documentation Framework. Your role is to process source corpora and extract patterns that can be transformed into explicit heuristics.

## Primary Tasks

### 1. Corpus Parsing

Process various source types:

#### Code Repositories
```python
# Extract patterns from:
- Function signatures and return patterns
- Error handling conventions
- Naming conventions
- Control flow patterns
- Design patterns in use
```

#### Documents
```python
# Extract from:
- Explicit rules and guidelines
- Implicit conventions
- Decision criteria
- Best practices
```

#### Research Papers
```python
# Extract from:
- Methodology descriptions
- Algorithm patterns
- Evaluation criteria
- Domain knowledge
```

### 2. Chunking Strategy

Implement intelligent chunking:

```
Chunk Size: 2000-4000 tokens
Overlap: 200 tokens
Strategy: Semantic boundaries

For code:
- Function/class boundaries
- Module boundaries
- Logical sections

For text:
- Paragraph boundaries
- Section boundaries
- Topic shifts
```

### 3. Pattern Extraction Prompt

Use this template for LLM extraction:

```
Given the following content from domain: {domain}

{chunk_content}

Extract any implicit or explicit patterns, rules, or heuristics:

1. PATTERN NAME: Short descriptive name
2. PATTERN TYPE: [rule|convention|best-practice|anti-pattern]
3. DESCRIPTION: What the pattern captures
4. PRECONDITIONS: When the pattern applies
5. POSTCONDITIONS: Expected outcomes
6. EVIDENCE: Specific examples from the content
7. CONFIDENCE: How clearly the pattern is expressed (0-1)

Format as JSON array.
```

### 4. Output Schema

Produce extracted patterns in this format:

```json
{
  "patterns": [
    {
      "id": "pattern-001",
      "name": "Early Return Pattern",
      "type": "best-practice",
      "domain": "software-engineering",
      "description": "Return early for edge cases to reduce nesting",
      "preconditions": [
        "Function has multiple conditional branches",
        "Some branches handle edge cases"
      ],
      "postconditions": [
        "Reduced cyclomatic complexity",
        "Improved readability"
      ],
      "evidence": [
        {
          "source": "file.py:42",
          "snippet": "if not input: return None"
        }
      ],
      "confidence": 0.85,
      "frequency": 15
    }
  ],
  "metadata": {
    "corpusPath": "/path/to/corpus",
    "chunkCount": 50,
    "extractionDate": "2026-01-15"
  }
}
```

## Extraction Pipeline

```
1. Discover files → Glob patterns
2. Read content → File reader
3. Chunk content → Semantic boundaries
4. Extract patterns → LLM analysis
5. Deduplicate → Similarity matching
6. Rank by confidence → Sort and filter
7. Output JSON → Structured format
```

## Quality Criteria

- Minimum confidence: 0.5 for inclusion
- Require at least 2 evidence instances
- Flag contradictory patterns
- Track provenance to source

## Error Handling

- Skip unparseable files (log warning)
- Handle encoding issues gracefully
- Merge duplicate patterns (keep highest confidence)
- Report extraction statistics

```

## File: heuristics-framework/docs/README.md

- Extension: .md
- Language: markdown
- Size: 3340 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/hooks/hooks.json

- Extension: .json
- Language: json
- Size: 632 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```json
{
  "description": "Heuristics Framework validation hooks",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-heuristic-syntax.py",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-corpus-exists.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}

```

## File: heuristics-framework/hooks/scripts/validate-heuristic-syntax.py

- Extension: .py
- Language: python
- Size: 3540 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```python
#!/usr/bin/env python3
"""
Validate Python heuristic function syntax.

Exit codes:
- 0: Success (valid syntax)
- 1: Warning (non-blocking issues)
- 2: Block (invalid syntax, stop operation)
"""

import sys
import json
import ast

def validate_heuristic_file(file_path: str) -> dict:
    """Validate a Python heuristic file."""
    issues = []

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        # Find heuristic functions
        heuristic_functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('heuristic'):
                    heuristic_functions.append(node)

        if not heuristic_functions:
            issues.append({
                "severity": "warning",
                "message": "No heuristic function found (expected function starting with 'heuristic')"
            })

        for func in heuristic_functions:
            # Check for return type annotation
            if func.returns is None:
                issues.append({
                    "severity": "warning",
                    "message": f"Function '{func.name}' missing return type annotation (expected -> float)"
                })

            # Check for docstring
            if not ast.get_docstring(func):
                issues.append({
                    "severity": "warning",
                    "message": f"Function '{func.name}' missing docstring"
                })

            # Check argument count
            args = func.args.args
            if len(args) < 2:
                issues.append({
                    "severity": "error",
                    "message": f"Function '{func.name}' needs at least 2 arguments (current_state, goal_state)"
                })

        # Check for HEURISTIC_METADATA
        has_metadata = any(
            isinstance(node, ast.Assign) and
            any(isinstance(t, ast.Name) and t.id == 'HEURISTIC_METADATA' for t in node.targets)
            for node in ast.walk(tree)
        )

        if not has_metadata:
            issues.append({
                "severity": "info",
                "message": "Consider adding HEURISTIC_METADATA dict for framework integration"
            })

    except SyntaxError as e:
        issues.append({
            "severity": "error",
            "message": f"Syntax error: {e.msg} at line {e.lineno}"
        })
    except Exception as e:
        issues.append({
            "severity": "error",
            "message": f"Validation error: {str(e)}"
        })

    return {
        "file": file_path,
        "issues": issues,
        "valid": not any(i["severity"] == "error" for i in issues)
    }


def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith('.py'):
        # Not a Python file, skip
        sys.exit(0)

    result = validate_heuristic_file(file_path)

    # Output validation result
    if result["issues"]:
        for issue in result["issues"]:
            print(f"[{issue['severity'].upper()}] {issue['message']}", file=sys.stderr)

    # Determine exit code
    if not result["valid"]:
        sys.exit(2)  # Block - has errors
    elif any(i["severity"] == "warning" for i in result["issues"]):
        sys.exit(1)  # Warning - non-blocking
    else:
        sys.exit(0)  # Success


if __name__ == "__main__":
    main()

```

## File: heuristics-framework/hooks/scripts/check-corpus-exists.py

- Extension: .py
- Language: python
- Size: 1740 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```python
#!/usr/bin/env python3
"""
Pre-check that corpus path exists before discovery.

Exit codes:
- 0: Success (corpus exists)
- 2: Block (corpus not found)
"""

import sys
import json
import os
import re

def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    command = input_data.get("tool_input", {}).get("command", "")

    # Extract path from discover command
    # Pattern: python ... discover <path> ...
    match = re.search(r'discover\s+([^\s]+)', command)

    if not match:
        # Not a discover command we care about
        sys.exit(0)

    corpus_path = match.group(1)

    # Resolve path
    if not os.path.isabs(corpus_path):
        cwd = input_data.get("cwd", os.getcwd())
        corpus_path = os.path.join(cwd, corpus_path)

    # Check existence
    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus path does not exist: {corpus_path}", file=sys.stderr)
        print(f"[INFO] Please verify the path and try again", file=sys.stderr)
        sys.exit(2)

    # Check if it's readable
    if os.path.isdir(corpus_path):
        if not os.access(corpus_path, os.R_OK):
            print(f"[ERROR] Cannot read corpus directory: {corpus_path}", file=sys.stderr)
            sys.exit(2)

        # Check for files
        files = os.listdir(corpus_path)
        if not files:
            print(f"[WARNING] Corpus directory is empty: {corpus_path}", file=sys.stderr)
            # Don't block, just warn
    elif os.path.isfile(corpus_path):
        if not os.access(corpus_path, os.R_OK):
            print(f"[ERROR] Cannot read corpus file: {corpus_path}", file=sys.stderr)
            sys.exit(2)

    # Success
    sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: heuristics-framework/hooks/scripts/validate-jsonld.py

- Extension: .py
- Language: python
- Size: 3572 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```python
#!/usr/bin/env python3
"""
Validate JSON-LD heuristic schema compliance.

Exit codes:
- 0: Success (valid schema)
- 1: Warning (non-blocking issues)
- 2: Block (invalid schema)
"""

import sys
import json

REQUIRED_FIELDS = ["@type", "@id", "name", "description"]
RECOMMENDED_FIELDS = ["heuristic:confidence", "popper:validation", "heuristic:domain"]

def validate_jsonld(content: dict) -> dict:
    """Validate JSON-LD heuristic document."""
    issues = []

    # Check @context
    if "@context" not in content:
        issues.append({
            "severity": "warning",
            "message": "Missing @context - document may not be fully JSON-LD compliant"
        })

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in content:
            issues.append({
                "severity": "error",
                "message": f"Missing required field: {field}"
            })

    # Check @type
    if content.get("@type") and "Heuristic" not in str(content["@type"]):
        issues.append({
            "severity": "warning",
            "message": f"@type should include 'Heuristic', found: {content.get('@type')}"
        })

    # Check recommended fields
    for field in RECOMMENDED_FIELDS:
        if field not in content:
            issues.append({
                "severity": "info",
                "message": f"Consider adding recommended field: {field}"
            })

    # Validate confidence range
    confidence = content.get("heuristic:confidence") or content.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            issues.append({
                "severity": "error",
                "message": f"Confidence must be between 0 and 1, got: {confidence}"
            })

    # Validate validation section
    validation = content.get("popper:validation") or content.get("validation")
    if validation:
        if "method" not in validation:
            issues.append({
                "severity": "warning",
                "message": "Validation section missing 'method' field"
            })
        if validation.get("typeIError"):
            error_rate = validation["typeIError"]
            if not 0 < error_rate < 1:
                issues.append({
                    "severity": "error",
                    "message": f"Type-I error rate must be between 0 and 1, got: {error_rate}"
                })

    return {
        "issues": issues,
        "valid": not any(i["severity"] == "error" for i in issues)
    }


def main():
    # Read hook input from stdin
    input_data = json.loads(sys.stdin.read())

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith('.jsonld'):
        sys.exit(0)

    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    result = validate_jsonld(content)

    # Output validation result
    if result["issues"]:
        for issue in result["issues"]:
            print(f"[{issue['severity'].upper()}] {issue['message']}", file=sys.stderr)

    # Determine exit code
    if not result["valid"]:
        sys.exit(2)
    elif any(i["severity"] == "warning" for i in result["issues"]):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: heuristics-framework/.claude-plugin/plugin.json

- Extension: .json
- Language: json
- Size: 831 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```json
{
  "name": "heuristics-framework",
  "version": "1.0.0",
  "description": "LLM-based framework for automated heuristic discovery, validation, and documentation using AutoHD, POPPER, and knowledge graph construction methodologies",
  "author": {
    "name": "Monxun",
    "email": "devtools@example.com"
  },
  "license": "MIT",
  "keywords": [
    "heuristics",
    "autohd",
    "popper",
    "validation",
    "knowledge-graph",
    "llm",
    "hypothesis-testing",
    "documentation",
    "multi-agent",
    "deterministic-inference"
  ],
  "commands": "./commands/",
  "agents": [
    "./agents/orchestrator.md",
    "./agents/extractor.md",
    "./agents/synthesizer.md",
    "./agents/validator.md",
    "./agents/documenter.md",
    "./agents/kg-builder.md"
  ],
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}

```

## File: heuristics-framework/commands/validate.md

- Extension: .md
- Language: markdown
- Size: 1711 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/commands/extract.md

- Extension: .md
- Language: markdown
- Size: 2090 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
# Extract Patterns Command

Extract patterns from a corpus without full heuristic synthesis.

## Usage

```
/heuristics-framework:extract <corpus-path> [options]
```

## Arguments

- `$1` - Path to corpus directory or file (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--domain <domain>` - Domain context for extraction
- `--min-confidence <0-1>` - Minimum pattern confidence (default: 0.5)
- `--min-frequency <n>` - Minimum occurrence count (default: 2)
- `--output <path>` - Output file path (default: patterns.json)
- `--format <json|yaml>` - Output format (default: json)

## Workflow

This command delegates to the `heuristics-extractor` agent to:

1. **Parse** corpus files (code, documents, research)
2. **Chunk** content for LLM processing
3. **Extract** patterns using domain-specific prompts
4. **Deduplicate** similar patterns
5. **Rank** by confidence and frequency

## Injected Skills

- `autohd-discovery` - Pattern extraction methodology

## Example

```bash
# Extract patterns from source code
/heuristics-framework:extract ./src --domain software-engineering

# Extract from documents with custom threshold
/heuristics-framework:extract ./docs --min-confidence 0.7 --min-frequency 5

# Output as YAML
/heuristics-framework:extract ./research --format yaml --output patterns.yaml
```

## Output Format

```json
{
  "patterns": [
    {
      "id": "pattern-001",
      "name": "Early Return Pattern",
      "type": "best-practice",
      "domain": "software-engineering",
      "description": "Return early for edge cases",
      "preconditions": [...],
      "postconditions": [...],
      "evidence": [...],
      "confidence": 0.85,
      "frequency": 15
    }
  ],
  "metadata": {
    "corpusPath": "...",
    "chunkCount": 50,
    "extractionDate": "2026-01-15"
  }
}
```

## Supported File Types

| Type | Extensions | Parser |
|------|------------|--------|
| Python | .py | AST + semantic |
| JavaScript | .js, .ts | AST + semantic |
| Markdown | .md | Section-based |
| Text | .txt | Paragraph-based |
| PDF | .pdf | Text extraction |

```

## File: heuristics-framework/commands/build-kg.md

- Extension: .md
- Language: markdown
- Size: 2085 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
# Build Knowledge Graph Command

Construct a knowledge graph from extracted patterns or heuristics.

## Usage

```
/heuristics-framework:build-kg <input-path> [options]
```

## Arguments

- `$1` - Path to patterns JSON or heuristics directory (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--output <path>` - Output graph file (default: knowledge-graph.json)
- `--format <json|neo4j|rdf>` - Output format (default: json)
- `--schema <path>` - Custom entity/relation schema
- `--resolve-entities` - Enable entity resolution (default: true)
- `--neo4j-uri <uri>` - Neo4j connection for direct import

## Workflow

This command delegates to the `heuristics-kg-builder` agent to:

1. **Extract** entities from patterns/heuristics
2. **Extract** relationships as (S, P, O) triples
3. **Resolve** duplicate entities
4. **Fuse** knowledge from multiple sources
5. **Export** to specified format

## Injected Skills

- `kg-construction` - Knowledge graph methodology

## Example

```bash
# Build KG from patterns
/heuristics-framework:build-kg ./patterns.json

# Export to Neo4j format
/heuristics-framework:build-kg ./heuristics/ --format neo4j

# Direct Neo4j import
/heuristics-framework:build-kg ./patterns.json --neo4j-uri bolt://localhost:7687
```

## Output Formats

### JSON (default)

```json
{
  "nodes": [
    {"@id": "entity:x", "@type": "Heuristic", "label": "..."}
  ],
  "edges": [
    {"source": "entity:x", "predicate": "APPLIES_TO", "target": "entity:y"}
  ]
}
```

### Neo4j Cypher

```cypher
CREATE (h:Heuristic {id: '...', name: '...'})
CREATE (d:Domain {id: '...', name: '...'})
CREATE (h)-[:APPLIES_TO]->(d)
```

### RDF/Turtle

```turtle
@prefix hf: <https://heuristics-framework.dev/> .
hf:early-return a hf:Heuristic ;
    hf:appliesTo hf:software-engineering .
```

## Relation Types

| Predicate | Description |
|-----------|-------------|
| DEPENDS_ON | Entity requires another |
| CONTRADICTS | Mutually exclusive |
| SPECIALIZES | More specific version |
| APPLIES_TO | Heuristic → Domain |
| VALIDATES | Evidence → Heuristic |

```

## File: heuristics-framework/commands/discover.md

- Extension: .md
- Language: markdown
- Size: 1771 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
# Discover Heuristics Command

Discover and document heuristics from a corpus using the full AutoHD + POPPER pipeline.

## Usage

```
/heuristics-framework:discover <corpus-path> [options]
```

## Arguments

- `$1` - Path to corpus directory (required)
- `$ARGUMENTS` - Full argument string for options

## Options

- `--domain <domain>` - Filter to specific domain
- `--confidence <0-1>` - Minimum confidence threshold (default: 0.85)
- `--output <path>` - Output directory (default: ./heuristics-output)
- `--format <json|md|html|all>` - Output format (default: all)

## Workflow

This command delegates to the `heuristics-orchestrator` agent which coordinates:

1. **Ingestion Phase**
   - Corpus parsing via `heuristics-extractor`
   - Knowledge graph construction via `heuristics-kg-builder`

2. **Discovery Phase (AutoHD)**
   - Heuristic synthesis via `heuristics-synthesizer`
   - Evolutionary refinement

3. **Validation Phase (POPPER)**
   - Sequential falsification via `heuristics-validator`
   - Statistical significance testing

4. **Documentation Phase**
   - Multi-format output via `heuristics-documenter`

## Injected Skills

- `autohd-discovery` - Heuristic generation methodology
- `popper-validation` - Hypothesis validation framework

## Example

```bash
# Discover heuristics from a codebase
/heuristics-framework:discover ./src --domain software-engineering

# With custom confidence threshold
/heuristics-framework:discover ./docs --confidence 0.90 --format json
```

## Output

```
heuristics-output/
├── json-ld/
│   └── *.jsonld
├── markdown/
│   ├── index.md
│   └── *.md
├── html/
│   ├── index.html
│   └── *.html
├── knowledge-graph.json
└── validation-report.json
```

```

## File: heuristics-framework/skills/deterministic-inference/SKILL.md

- Extension: .md
- Language: markdown
- Size: 3091 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: deterministic-inference
description: |
  Techniques for achieving reproducible LLM inference outputs.
  Use when: requiring exact reproducibility, batch-invariant inference,
  RL training reproducibility, consistent heuristic evaluation.
  Supports: SGLang deterministic mode, seed configuration, validation.
---

# Deterministic Inference Skill

## Quick Start

Achieve mathematically reproducible LLM outputs for consistent heuristic evaluation and validation.

### The Challenge

Even with `temperature=0`, LLM inference is non-deterministic due to:
- Batch-sensitive kernel operations (primary cause)
- Dynamic batching in servers
- Radix cache behavior

### Solution

Use batch-invariant kernels (SGLang) for true determinism.

## Configuration

### SGLang (Recommended)

```bash
python -m sglang.launch_server \
    --model your-model \
    --enable-deterministic-inference \
    --attention-backend flashinfer
```

### Multi-Provider Settings

| Provider | Method | Level |
|----------|--------|-------|
| SGLang | `--enable-deterministic-inference` | Perfect |
| OpenAI | `seed` parameter | Best-effort |
| Anthropic | `temperature=0` | Near-deterministic |
| vLLM | `seed` + env flag | High |
| llama.cpp | `seed=42, temp=0, top_p=1, top_k=1` | High |

## Core Components

### Batch-Invariant Operations

Three operations require special handling:
1. **RMSNorm** - Normalization layer
2. **Matrix Multiplication** - Core computation
3. **Attention** - Self-attention mechanism

### Validation Tests

```bash
# Single prompt, varying batch sizes
python -m sglang.test.test_deterministic --test-mode single

# Mixed prompts in same batch
python -m sglang.test.test_deterministic --test-mode mixed

# Prefix cache consistency
python -m sglang.test.test_deterministic --test-mode prefix
```

## Performance Trade-offs

| Configuration | Slowdown | Reproducibility |
|---------------|----------|-----------------|
| Default | 0% | ~80% |
| Deterministic | 34.35% | 100% |
| + CUDA graphs | 12% | 100% |

## Validation Pattern

```python
class DeterministicValidator:
    def test_single(self, prompt: str, n_runs: int = 50) -> bool:
        """Same prompt across varying batch sizes."""
        outputs = set()
        for batch_size in range(1, n_runs + 1):
            result = self.model.generate(prompt, batch_size=batch_size)
            outputs.add(result)
        return len(outputs) == 1  # Must be 1 for determinism
```

## When to Use

| Scenario | Determinism Needed |
|----------|-------------------|
| Heuristic evaluation | Yes (critical) |
| RL training | Yes (critical) |
| Production inference | Usually no |
| Debugging | Yes (helpful) |

## Additional Resources

- For SGLang setup: [sglang-setup.md](references/sglang-setup.md)
- For validation suite: [validation-suite.md](references/validation-suite.md)
- For performance tuning: [performance-tuning.md](references/performance-tuning.md)

## Research Foundation

Based on: "Towards Deterministic Inference in SGLang"
- Source: Thinking Machines Lab
- Blog: lmsys.org/blog/2025-09-22-sglang-deterministic/

```

## File: heuristics-framework/skills/deterministic-inference/references/sglang-setup.md

- Extension: .md
- Language: markdown
- Size: 2935 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
# SGLang Deterministic Inference Setup

## Installation

```bash
pip install sglang[all]

# Or from source for latest deterministic features
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git"
```

## Server Configuration

### Basic Deterministic Mode

```bash
python -m sglang.launch_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --enable-deterministic-inference \
    --port 30000
```

### With Performance Optimization

```bash
python -m sglang.launch_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --enable-deterministic-inference \
    --attention-backend flashinfer \
    --enable-cuda-graph \
    --port 30000
```

### Environment Variables

```bash
# Enable deterministic mode programmatically
export SGLANG_DETERMINISTIC=1

# Set default seed
export SGLANG_SEED=42
```

## Client Configuration

```python
import sglang as sgl

# Connect to server
sgl.set_default_backend(sgl.RuntimeEndpoint("http://localhost:30000"))

# Deterministic generation
@sgl.function
def generate_heuristic(s, pattern):
    s += sgl.user(f"Generate heuristic for: {pattern}")
    s += sgl.assistant(sgl.gen("response", temperature=0))

# Will produce identical output across runs
result = generate_heuristic.run(pattern="Early return")
```

## Testing Determinism

### Single Prompt Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode single \
    --num-runs 50
```

### Mixed Batch Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode mixed \
    --num-runs 50
```

### Prefix Cache Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode prefix \
    --num-runs 50
```

## Performance Impact

| Configuration | Throughput | Determinism |
|---------------|------------|-------------|
| Default | 100% | ~80% |
| Deterministic | 65% | 100% |
| + CUDA Graphs | 88% | 100% |
| + FlashInfer | 92% | 100% |

## Troubleshooting

### Non-Determinism Detected

```bash
# Check batch sizes
curl http://localhost:30000/v1/models/stats

# Verify kernel implementations
python -c "import sglang; print(sglang.check_deterministic_kernels())"
```

### Memory Issues

```bash
# Reduce max batch size
python -m sglang.launch_server \
    --model your-model \
    --enable-deterministic-inference \
    --max-num-seqs 16  # Lower for stability
```

## Integration Example

```python
class DeterministicHeuristicEvaluator:
    def __init__(self, server_url: str):
        sgl.set_default_backend(sgl.RuntimeEndpoint(server_url))

    def evaluate(self, heuristic: str, test_cases: list) -> dict:
        """Evaluate with guaranteed reproducibility."""
        results = []

        for case in test_cases:
            # Same input always produces same output
            output = self._run_evaluation(heuristic, case)
            results.append(output)

        return {
            "results": results,
            "reproducible": True
        }
```

```

## File: heuristics-framework/skills/popper-validation/SKILL.md

- Extension: .md
- Language: markdown
- Size: 2863 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/skills/popper-validation/references/experiment-design.md

- Extension: .md
- Language: markdown
- Size: 3115 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/skills/autohd-discovery/SKILL.md

- Extension: .md
- Language: markdown
- Size: 2789 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/skills/autohd-discovery/references/function-patterns.md

- Extension: .md
- Language: markdown
- Size: 3577 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
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

```

## File: heuristics-framework/skills/kg-construction/SKILL.md

- Extension: .md
- Language: markdown
- Size: 2867 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
---
name: kg-construction
description: |
  Knowledge graph construction using LLM-empowered extraction pipelines.
  Use when: building entity-relationship graphs, entity extraction (NER),
  relation extraction, entity resolution, knowledge fusion, GraphRAG.
  Supports: schema-based and schema-free approaches.
---

# Knowledge Graph Construction Skill

## Quick Start

Build structured knowledge graphs from unstructured text using LLM-powered extraction.

### Core Pipeline

```
1. EXTRACT: Identify entities (NER)
2. RELATE: Extract relationships as triples
3. RESOLVE: Deduplicate and merge entities
4. FUSE: Integrate across sources
5. STORE: Persist to graph database
```

## Construction Approaches

### Schema-Based (Top-Down)

```
Predefined ontology → LLM extraction → Structured graph

Pros: High precision, interpretable
Cons: Limited flexibility
Use: Enterprise KG, domain-specific apps
```

### Schema-Free (Bottom-Up)

```
Raw data → LLM extraction → Dynamic schema induction

Pros: Flexible, discovers new patterns
Cons: May need cleanup
Use: Exploratory analysis, new domains
```

## Core Workflow

### Step 1: Entity Extraction

```python
ENTITY_TYPES = [
    "Heuristic",   # Documented rule
    "Domain",      # Area of applicability
    "Concept",     # Abstract principle
    "Pattern",     # Recurring structure
    "Evidence",    # Supporting data
]
```

### Step 2: Relation Extraction

Common predicates:
| Predicate | Description |
|-----------|-------------|
| DEPENDS_ON | Requires another entity |
| CONTRADICTS | Mutually exclusive |
| SPECIALIZES | More specific version |
| APPLIES_TO | Heuristic → Domain |
| VALIDATES | Evidence → Heuristic |

### Step 3: Entity Resolution

```
Group by normalized name
↓
Fuzzy match (>0.9 similarity)
↓
Alias detection
↓
Merge with conflict resolution
```

### Step 4: Knowledge Fusion

Trust ordering for conflicts:
1. Primary sources (code, official docs)
2. Secondary sources (tutorials, blogs)
3. Derived sources (LLM extractions)

## Output Format

```json
{
  "nodes": [
    {"@id": "entity:x", "@type": "Heuristic", "label": "..."}
  ],
  "edges": [
    {"source": "entity:x", "predicate": "APPLIES_TO", "target": "entity:y"}
  ]
}
```

## Quality Metrics

| Metric | Target |
|--------|--------|
| Entity precision | >0.85 |
| Relation precision | >0.80 |
| Resolution accuracy | >0.90 |
| Graph connectivity | >0.70 |

## Additional Resources

- For entity extraction: [entity-extraction.md](references/entity-extraction.md)
- For Neo4j integration: [neo4j-integration.md](references/neo4j-integration.md)
- For GraphRAG patterns: [graphrag-patterns.md](references/graphrag-patterns.md)

## Research Foundation

Based on: "LLM-empowered Knowledge Graph Construction Survey"
- Paper: arxiv.org/abs/2510.20345
- Tools: FalkorDB, LangChain Graph Transformer, Neo4j Builder

```

## File: heuristics-framework/skills/kg-construction/references/entity-extraction.md

- Extension: .md
- Language: markdown
- Size: 3593 bytes
- Created: 2026-01-16 00:43:03
- Modified: 2026-01-16 00:43:03

### Code

```markdown
# Entity Extraction Reference

## Entity Type Definitions

```python
ENTITY_SCHEMA = {
    "Heuristic": {
        "description": "A documented rule or pattern",
        "attributes": ["name", "confidence", "domain"],
        "examples": ["Early Return Pattern", "Guard Clause Pattern"]
    },
    "Domain": {
        "description": "Area of applicability",
        "attributes": ["name", "hierarchy"],
        "examples": ["Software Engineering", "Code Quality"]
    },
    "Concept": {
        "description": "Abstract idea or principle",
        "attributes": ["name", "definition"],
        "examples": ["Complexity", "Readability"]
    },
    "Pattern": {
        "description": "Recurring structure or behavior",
        "attributes": ["name", "type", "frequency"],
        "examples": ["Singleton", "Factory", "Observer"]
    },
    "Evidence": {
        "description": "Supporting data or example",
        "attributes": ["source", "type", "confidence"],
        "examples": ["Code sample", "Research citation"]
    }
}
```

## Extraction Prompt Template

```
Given the following text from domain: {domain}

---
{text_content}
---

Extract all entities mentioned. For each entity provide:

1. TEXT_SPAN: The exact text mentioning the entity
2. ENTITY_TYPE: One of {entity_types}
3. NORMALIZED_NAME: Canonical form of the entity name
4. ATTRIBUTES: Relevant attributes from the text
5. CONFIDENCE: How confident (0.0-1.0) you are in this extraction

Output as JSON array:
[
  {
    "text_span": "...",
    "entity_type": "...",
    "normalized_name": "...",
    "attributes": {...},
    "confidence": 0.85
  }
]
```

## Extraction Pipeline

```python
class EntityExtractor:
    def __init__(self, llm_client, schema: dict):
        self.llm = llm_client
        self.schema = schema

    def extract(self, text: str, domain: str) -> list:
        """Extract entities from text."""
        # 1. Chunk text if needed
        chunks = self.chunk_text(text)

        # 2. Extract from each chunk
        all_entities = []
        for chunk in chunks:
            entities = self.extract_from_chunk(chunk, domain)
            all_entities.extend(entities)

        # 3. Deduplicate
        unique_entities = self.deduplicate(all_entities)

        return unique_entities

    def extract_from_chunk(self, chunk: str, domain: str) -> list:
        """Extract entities from a single chunk."""
        prompt = self.build_prompt(chunk, domain)
        response = self.llm.generate(prompt)
        return self.parse_response(response)
```

## Confidence Scoring

| Confidence | Description |
|------------|-------------|
| 0.9-1.0 | Explicit mention with clear context |
| 0.7-0.9 | Clear mention, some inference needed |
| 0.5-0.7 | Implicit mention, significant inference |
| <0.5 | Uncertain, needs review |

## Post-Processing

```python
def postprocess_entities(entities: list) -> list:
    """Clean and validate extracted entities."""
    processed = []

    for entity in entities:
        # Normalize name
        entity["normalized_name"] = normalize(entity["normalized_name"])

        # Validate type
        if entity["entity_type"] not in ENTITY_SCHEMA:
            entity["entity_type"] = "Unknown"
            entity["confidence"] *= 0.5

        # Filter low confidence
        if entity["confidence"] >= 0.5:
            processed.append(entity)

    return processed
```

## Quality Metrics

| Metric | Calculation | Target |
|--------|-------------|--------|
| Precision | TP / (TP + FP) | >0.85 |
| Recall | TP / (TP + FN) | >0.75 |
| F1 Score | 2 * P * R / (P + R) | >0.80 |

```

