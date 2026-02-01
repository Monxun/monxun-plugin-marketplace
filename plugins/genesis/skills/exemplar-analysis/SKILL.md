---
name: exemplar-analysis
description: |
  Project analysis patterns for extracting structure and conventions from source code.
  Use when: analyzing source code, detecting frameworks, extracting patterns,
  "analyze project", "learn from example", project inspection, framework detection,
  dependency analysis, architecture recognition.
  Supports: AST parsing, config detection, dependency analysis.
allowed-tools: Read, Grep, Glob, Bash
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Exemplar Analysis Skill

Extract patterns, structure, and conventions from existing projects for template generation.

## Language Detection

### By File Extension
```bash
# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
```

### By Config Files
| Config File | Language |
|-------------|----------|
| `package.json` | JavaScript/TypeScript |
| `tsconfig.json` | TypeScript |
| `pyproject.toml` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pom.xml` | Java |
| `build.gradle` | Java/Kotlin |
| `Gemfile` | Ruby |

## Framework Detection

### Node.js Frameworks
```bash
jq -r '.dependencies | keys[]' package.json 2>/dev/null | grep -E "^(next|react|vue|express|fastify|nest|hono)"
```

### Python Frameworks
```bash
grep -E "^(fastapi|django|flask|starlette|litestar)" requirements.txt pyproject.toml 2>/dev/null
```

### Go Frameworks
```bash
grep -E "(gin-gonic|echo|fiber|chi|gorilla)" go.mod 2>/dev/null
```

## Architecture Patterns

| Pattern | Indicators |
|---------|------------|
| **Layered** | `/routes`, `/services`, `/repositories` |
| **Hexagonal** | `/domain`, `/ports`, `/adapters` |
| **Clean** | `/entities`, `/usecases`, `/interfaces` |
| **Feature-based** | `/features/{feature}/` |
| **Microservice** | Multiple `go.mod` or `package.json` |

### Detection Script
```bash
# Check for layered architecture
[ -d "src/routes" ] && [ -d "src/services" ] && echo "Layered architecture"

# Check for hexagonal
[ -d "src/domain" ] && [ -d "src/ports" ] && echo "Hexagonal architecture"

# Check for monorepo
[ -d "packages" ] || [ -d "apps" ] && echo "Monorepo structure"
```

## Convention Extraction

### Naming Conventions
```bash
# File naming
ls src/*.ts 2>/dev/null | head -5  # kebab-case, camelCase, snake_case?

# Function naming
grep -h "export function" src/**/*.ts 2>/dev/null | head -5

# Class naming
grep -h "export class" src/**/*.ts 2>/dev/null | head -5
```

### File Organization
- **Co-located tests**: `*.test.ts` next to `*.ts`
- **Separate tests**: `__tests__/` or `tests/` directory
- **Co-located styles**: `*.module.css` next to component

## Quick Analysis

```bash
# Full project scan
echo "=== Language ==="
find . -type f -name "*.ts" | wc -l && echo "TypeScript files"
find . -type f -name "*.py" | wc -l && echo "Python files"

echo "=== Framework ==="
[ -f package.json ] && jq -r '.dependencies | keys[]' package.json | head -10
[ -f requirements.txt ] && head -10 requirements.txt

echo "=== Structure ==="
ls -la src/ 2>/dev/null | head -10

echo "=== Config ==="
ls -la *.json *.yaml *.toml 2>/dev/null
```

## Output Format

```json
{
  "languages": {"primary": "typescript", "secondary": ["yaml"]},
  "frameworks": [{"name": "fastify", "confidence": 0.95}],
  "architecture": {"pattern": "layered", "layers": ["routes", "services"]},
  "conventions": {"naming": "kebab-case", "testPattern": "co-located"}
}
```

## Detailed References

- [AST Patterns](references/ast-patterns.md) - Tree-sitter parsing patterns
- [Config Detection](references/config-detection.md) - Configuration file analysis
- [Dependency Analysis](references/dependency-analysis.md) - Dependency graph construction
