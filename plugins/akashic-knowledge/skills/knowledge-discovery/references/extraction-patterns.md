# Entity and Relation Extraction Patterns

## Entity Types

### Technical Entities

| Type | Examples | Extraction Cues |
|------|----------|-----------------|
| Concept | "dependency injection", "event sourcing" | Abstract nouns, methodology terms |
| Technology | "React", "PostgreSQL", "Docker" | Capitalized names, version mentions |
| Component | "UserService", "AuthController" | CamelCase, class/function names |
| Artifact | "config.yaml", "Dockerfile" | File extensions, path patterns |

### Research Entities

| Type | Examples | Extraction Cues |
|------|----------|-----------------|
| Author | "John Smith", "et al." | Name patterns, author sections |
| Publication | "arXiv:2024.12345" | DOI, arXiv IDs, citations |
| Date | "January 2026", "v2.0" | Date formats, version strings |

## Relation Types

### Hierarchical Relations

```
IS_A(child, parent)
  - "React is a JavaScript framework"
  - Pattern: X is a/an Y

PART_OF(part, whole)
  - "Authentication module is part of the security system"
  - Pattern: X is part of Y, X belongs to Y

CONTAINS(container, contained)
  - "The package contains three modules"
  - Pattern: X contains Y, X includes Y
```

### Associative Relations

```
RELATED_TO(entity1, entity2)
  - General association
  - Pattern: X relates to Y, X and Y

USES(user, used)
  - "The service uses Redis for caching"
  - Pattern: X uses Y, X leverages Y

IMPLEMENTS(implementer, interface)
  - "UserService implements IUserRepository"
  - Pattern: X implements Y, X realizes Y
```

### Temporal Relations

```
PRECEDES(earlier, later)
  - "Authentication precedes authorization"
  - Pattern: X before Y, X precedes Y

VERSION_OF(newer, older)
  - "React 18 is a version of React"
  - Pattern: vX.Y, version history

DEPRECATED_BY(old, new)
  - "ComponentDidMount deprecated by useEffect"
  - Pattern: deprecated, superseded by
```

## Extraction Algorithms

### Named Entity Recognition (NER)

```python
def extract_entities(text: str) -> list[Entity]:
    """
    Multi-pass entity extraction:
    1. Pattern-based extraction (regex)
    2. Context-based classification
    3. Coreference resolution
    """
    entities = []

    # Pass 1: Pattern matching
    for pattern in ENTITY_PATTERNS:
        matches = pattern.findall(text)
        entities.extend(classify_matches(matches))

    # Pass 2: Context classification
    for entity in entities:
        entity.type = classify_by_context(entity, text)

    # Pass 3: Coreference resolution
    entities = resolve_coreferences(entities, text)

    return entities
```

### Relation Extraction

```python
def extract_relations(text: str, entities: list[Entity]) -> list[Relation]:
    """
    Dependency-based relation extraction:
    1. Parse sentence structure
    2. Identify relation triggers
    3. Link entities via dependencies
    """
    relations = []

    for sentence in split_sentences(text):
        deps = parse_dependencies(sentence)
        triggers = find_relation_triggers(deps)

        for trigger in triggers:
            subject = find_subject(trigger, deps, entities)
            object_ = find_object(trigger, deps, entities)

            if subject and object_:
                relation = Relation(
                    source=subject,
                    target=object_,
                    type=classify_relation(trigger),
                    evidence=sentence
                )
                relations.append(relation)

    return relations
```

## Quality Assurance

### Validation Rules

1. **Entity Consistency**: Same entity, same ID across documents
2. **Relation Validity**: Both endpoints must exist
3. **Type Correctness**: Relations match entity types
4. **Evidence Tracking**: All extractions have source evidence

### Confidence Scoring

```python
def calculate_confidence(extraction: Extraction) -> float:
    """
    Confidence based on:
    - Pattern match strength
    - Context support
    - Cross-document frequency
    """
    score = 0.0

    # Pattern strength (0-0.4)
    score += extraction.pattern_score * 0.4

    # Context support (0-0.3)
    score += extraction.context_score * 0.3

    # Frequency (0-0.3)
    score += min(extraction.frequency / 10, 1.0) * 0.3

    return score
```
