# Quality Metrics

Measuring and scoring plugin quality.

## Quality Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Structure | 25% | Correct directory layout |
| Schema | 25% | Valid JSON/YAML |
| Documentation | 20% | Description quality |
| Efficiency | 15% | Progressive disclosure |
| Testing | 15% | Validation coverage |

## Scoring System

### Overall Score
```
Score = (Structure × 0.25) + (Schema × 0.25) +
        (Documentation × 0.20) + (Efficiency × 0.15) +
        (Testing × 0.15)
```

### Grade Scale
| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | Excellent |
| 80-89 | B | Good |
| 70-79 | C | Acceptable |
| 60-69 | D | Needs Work |
| <60 | F | Failing |

## Structure Metrics

### Checklist (25 points)
| Check | Points |
|-------|--------|
| plugin.json exists | 5 |
| Only plugin.json in .claude-plugin/ | 5 |
| Components at root | 5 |
| All paths valid | 5 |
| Proper organization | 5 |

### Calculation
```python
def score_structure(plugin_path):
    score = 0

    # plugin.json exists
    if os.path.exists(f"{plugin_path}/.claude-plugin/plugin.json"):
        score += 5

    # Only plugin.json in .claude-plugin/
    contents = os.listdir(f"{plugin_path}/.claude-plugin")
    if contents == ["plugin.json"]:
        score += 5

    # Components at root
    for component in ["commands", "agents", "skills"]:
        if os.path.isdir(f"{plugin_path}/{component}"):
            score += 1.67  # 5 total for all three

    # All paths valid
    paths_valid = check_all_paths(plugin_path)
    if paths_valid:
        score += 5

    # Proper organization
    if check_organization(plugin_path):
        score += 5

    return score
```

## Schema Metrics

### Checklist (25 points)
| Check | Points |
|-------|--------|
| Valid JSON files | 5 |
| Valid YAML frontmatter | 5 |
| Required fields present | 5 |
| Name format correct | 5 |
| Version format correct | 5 |

### Calculation
```python
def score_schema(plugin_path):
    score = 0

    # Valid JSON
    json_files = glob.glob(f"{plugin_path}/**/*.json", recursive=True)
    valid_json = all(validate_json(f) for f in json_files)
    if valid_json:
        score += 5

    # Valid YAML frontmatter
    md_files = glob.glob(f"{plugin_path}/**/*.md", recursive=True)
    valid_yaml = all(validate_frontmatter(f) for f in md_files)
    if valid_yaml:
        score += 5

    # Required fields
    if check_required_fields(plugin_path):
        score += 5

    # Name format
    if check_name_format(plugin_path):
        score += 5

    # Version format
    if check_version_format(plugin_path):
        score += 5

    return score
```

## Documentation Metrics

### Checklist (20 points)
| Check | Points |
|-------|--------|
| README exists | 4 |
| Description quality | 4 |
| Trigger keywords | 4 |
| Usage examples | 4 |
| API documented | 4 |

### Description Quality Score
```python
def score_description(description):
    score = 0

    # Length check (not too short, not too long)
    if 100 <= len(description) <= 1024:
        score += 1

    # Has "Use when:" pattern
    if "use when:" in description.lower():
        score += 1

    # Has trigger keywords (count >= 5)
    keywords = extract_keywords(description)
    if len(keywords) >= 5:
        score += 1

    # Has capabilities list
    if "supports:" in description.lower():
        score += 1

    return score  # Max 4
```

## Efficiency Metrics

### Checklist (15 points)
| Check | Points |
|-------|--------|
| SKILL.md < 500 lines | 5 |
| Has reference files | 5 |
| Scripts for automation | 5 |

### Calculation
```python
def score_efficiency(plugin_path):
    score = 0

    # SKILL.md line count
    skill_files = glob.glob(f"{plugin_path}/skills/*/SKILL.md")
    all_under_500 = all(count_lines(f) < 500 for f in skill_files)
    if all_under_500:
        score += 5

    # Has reference files
    ref_dirs = glob.glob(f"{plugin_path}/skills/*/references")
    if ref_dirs:
        score += 5

    # Has scripts
    script_files = glob.glob(f"{plugin_path}/**/scripts/*", recursive=True)
    if script_files:
        score += 5

    return score
```

## Testing Metrics

### Checklist (15 points)
| Check | Points |
|-------|--------|
| Has validation hooks | 5 |
| Integration test passes | 5 |
| Components load | 5 |

### Calculation
```python
def score_testing(plugin_path):
    score = 0

    # Has validation hooks
    hooks_file = f"{plugin_path}/hooks/hooks.json"
    if os.path.exists(hooks_file):
        with open(hooks_file) as f:
            hooks = json.load(f)
        if "PreToolUse" in hooks.get("hooks", {}):
            score += 5

    # Integration test
    result = run_integration_test(plugin_path)
    if result.returncode == 0:
        score += 5

    # Components load
    components_loaded = check_components_load(plugin_path)
    if components_loaded:
        score += 5

    return score
```

## Quality Report

### Format
```json
{
  "plugin": "plugin-name",
  "timestamp": "2026-01-15T12:00:00Z",
  "scores": {
    "structure": 25,
    "schema": 20,
    "documentation": 16,
    "efficiency": 15,
    "testing": 10
  },
  "total": 86,
  "grade": "B",
  "details": {
    "structure": {
      "checks": [
        {"name": "plugin.json exists", "passed": true},
        {"name": "only plugin.json in .claude-plugin", "passed": true}
      ]
    },
    "issues": [
      {"category": "schema", "message": "Version not semver format"}
    ],
    "recommendations": [
      {"priority": "medium", "suggestion": "Add reference files for large skills"}
    ]
  }
}
```

### Generating Report
```python
def generate_quality_report(plugin_path):
    return {
        "plugin": get_plugin_name(plugin_path),
        "timestamp": datetime.now().isoformat(),
        "scores": {
            "structure": score_structure(plugin_path),
            "schema": score_schema(plugin_path),
            "documentation": score_documentation(plugin_path),
            "efficiency": score_efficiency(plugin_path),
            "testing": score_testing(plugin_path)
        },
        "total": calculate_total(scores),
        "grade": get_grade(total),
        "details": collect_details(plugin_path)
    }
```
