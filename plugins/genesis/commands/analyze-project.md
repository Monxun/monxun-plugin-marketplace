---
name: analyze-project
description: Deep analysis of an existing project to extract patterns, frameworks, and conventions
allowed-tools: Read, Grep, Glob, Bash
argument-validation: required
---

# Analyze Project Command

Perform deep analysis of an existing project to understand its structure, frameworks, and patterns.

## Usage

```
/genesis:analyze-project <project-path> [options]
```

## Arguments

- `$1` - Path to project directory (required)
- `$ARGUMENTS` - Full argument string

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output <format>` | Output format (json, markdown) | json |
| `--depth <level>` | Analysis depth (quick, standard, deep) | standard |
| `--include-deps` | Include dependency analysis | true |
| `--include-ast` | Include AST analysis | false |

## Analysis Components

### Language Detection
- File extension analysis
- Configuration file detection
- Import statement parsing

### Framework Detection
- Manifest file parsing (package.json, pyproject.toml, etc.)
- Framework-specific file detection
- Confidence scoring

### Architecture Recognition
- Directory structure analysis
- Layer identification (routes, services, repositories)
- Pattern matching (MVC, hexagonal, microservice)

### Convention Extraction
- Naming conventions (files, functions, classes)
- File organization patterns
- Test patterns (co-located, separate)

### Dependency Analysis
- Production vs development dependencies
- Dependency categorization
- Version constraint analysis

## Examples

```bash
# Quick analysis
/genesis:analyze-project ./my-project --depth quick

# Deep analysis with AST
/genesis:analyze-project ./my-project --depth deep --include-ast

# Output as markdown
/genesis:analyze-project ./my-project --output markdown
```

## Output

```json
{
  "projectName": "my-project",
  "languages": {"primary": "typescript", "secondary": ["yaml"]},
  "frameworks": [{"name": "fastify", "confidence": 0.95}],
  "architecture": {"pattern": "layered", "layers": ["routes", "services"]},
  "conventions": {"naming": "kebab-case", "testPattern": "co-located"},
  "dependencies": {"production": [...], "development": [...]}
}
```

## Injected Skills

- `exemplar-analysis` - Pattern extraction techniques

## Delegates To

- `exemplar-analyzer` agent for detailed analysis
