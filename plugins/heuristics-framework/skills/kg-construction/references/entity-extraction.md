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
