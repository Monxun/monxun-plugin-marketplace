---
name: research-stack
description: Web research for technology stack recommendations and best practices
allowed-tools: Read, WebSearch, WebFetch
argument-validation: required
---

# Research Stack Command

Search the web for latest documentation, best practices, and patterns for a technology stack.

## Usage

```
/genesis:research-stack <query> [options]
```

## Arguments

- `$1` - Research query (required)
- `$ARGUMENTS` - Full argument string

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--depth <level>` | Research depth (quick, standard, deep) | standard |
| `--sources <list>` | Limit to sources | all |
| `--include-security` | Include security advisories | true |
| `--output <format>` | Output format (json, markdown) | markdown |

## Research Sources

- **Official Documentation** - Framework/library docs
- **GitHub** - Trending repos, templates, patterns
- **Security Advisories** - CVE databases, npm audit
- **Package Registries** - npm, PyPI, crates.io
- **Community** - Best practices, anti-patterns

## Examples

```bash
# Research FastAPI patterns
/genesis:research-stack "FastAPI production best practices 2026"

# Research with specific focus
/genesis:research-stack "Next.js 15 App Router" --depth deep

# Security-focused research
/genesis:research-stack "Express.js security" --include-security
```

## Output

```json
{
  "query": "FastAPI production best practices",
  "documentation": {
    "officialDocs": "https://fastapi.tiangolo.com",
    "latestVersion": "0.110.0"
  },
  "patterns": [
    {"source": "GitHub", "pattern": "...", "stars": 15000}
  ],
  "securityAdvisories": [],
  "versionRecommendations": {
    "fastapi": "^0.110.0",
    "pydantic": "^2.5.0"
  },
  "bestPractices": [...]
}
```

## Injected Skills

- `template-patterns` - Pattern recognition
- `github-actions` - Workflow patterns

## Delegates To

- `web-researcher` agent for comprehensive research
