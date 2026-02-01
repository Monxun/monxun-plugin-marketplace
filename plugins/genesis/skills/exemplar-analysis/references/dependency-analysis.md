# Dependency Analysis Reference

Patterns for constructing and analyzing dependency graphs from projects.

## Dependency Graph Construction

### Graph Structure
```json
{
  "nodes": [
    {"id": "express", "type": "production", "version": "^4.18.0"},
    {"id": "typescript", "type": "development", "version": "^5.0.0"}
  ],
  "edges": [
    {"source": "express", "target": "body-parser", "type": "depends_on"}
  ]
}
```

### Extraction Methods

#### npm Dependencies
```bash
#!/bin/bash
extract_npm_deps() {
    local pkg="$1"

    echo "=== Production Dependencies ==="
    jq -r '.dependencies | to_entries[] | "\(.key)@\(.value)"' "$pkg" 2>/dev/null

    echo "=== Development Dependencies ==="
    jq -r '.devDependencies | to_entries[] | "\(.key)@\(.value)"' "$pkg" 2>/dev/null

    echo "=== Peer Dependencies ==="
    jq -r '.peerDependencies | to_entries[] | "\(.key)@\(.value)"' "$pkg" 2>/dev/null
}
```

#### Python Dependencies
```python
import tomllib
import re

def extract_python_deps(pyproject_path=None, requirements_path=None):
    deps = {'production': [], 'development': []}

    if pyproject_path:
        with open(pyproject_path, 'rb') as f:
            data = tomllib.load(f)
            deps['production'] = data.get('project', {}).get('dependencies', [])
            optional = data.get('project', {}).get('optional-dependencies', {})
            deps['development'] = optional.get('dev', [])

    if requirements_path:
        with open(requirements_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    deps['production'].append(line)

    return deps
```

#### Go Dependencies
```bash
#!/bin/bash
extract_go_deps() {
    local gomod="$1"

    echo "=== Direct Dependencies ==="
    grep -E "^\t[^/]" "$gomod" | awk '{print $1 "@" $2}'

    echo "=== Indirect Dependencies ==="
    grep -E "// indirect$" "$gomod" | awk '{print $1 "@" $2}'
}
```

## Dependency Classification

### By Type
| Type | Description | Example |
|------|-------------|---------|
| `production` | Required at runtime | `express`, `react` |
| `development` | Build/test only | `typescript`, `jest` |
| `peer` | Provided by consumer | `react` (for components) |
| `optional` | Feature-specific | `pg` (for PostgreSQL) |

### By Category
```javascript
const categories = {
    framework: ['react', 'vue', 'angular', 'next', 'nuxt'],
    database: ['prisma', 'typeorm', 'sequelize', 'mongoose', 'pg', 'mysql2'],
    testing: ['jest', 'vitest', 'mocha', 'pytest', 'testing-library'],
    build: ['typescript', 'esbuild', 'vite', 'webpack', 'rollup'],
    utility: ['lodash', 'date-fns', 'axios', 'zod'],
    monitoring: ['sentry', 'datadog', 'newrelic']
};

function categorize(dependency) {
    for (const [category, packages] of Object.entries(categories)) {
        if (packages.some(p => dependency.includes(p))) {
            return category;
        }
    }
    return 'other';
}
```

## Version Analysis

### Constraint Types
| Pattern | Meaning | Example |
|---------|---------|---------|
| `^1.2.3` | Compatible with 1.x.x | `^1.2.3` → `1.2.3` to `<2.0.0` |
| `~1.2.3` | Patch updates only | `~1.2.3` → `1.2.3` to `<1.3.0` |
| `1.2.3` | Exact version | Only `1.2.3` |
| `>=1.2.3` | Minimum version | `1.2.3` or higher |
| `*` | Any version | Latest available |

### Version Recommendation
```javascript
function recommendVersion(current, available) {
    // Prefer caret for production deps
    const latest = available.filter(v => !v.includes('-'))[0];
    return `^${latest}`;
}
```

## Security Analysis

### Vulnerability Check
```bash
#!/bin/bash
check_vulnerabilities() {
    local dir="$1"

    if [ -f "$dir/package.json" ]; then
        npm audit --json 2>/dev/null | jq '.vulnerabilities'
    fi

    if [ -f "$dir/requirements.txt" ]; then
        pip-audit -r "$dir/requirements.txt" --format json 2>/dev/null
    fi
}
```

### Outdated Check
```bash
#!/bin/bash
check_outdated() {
    local dir="$1"

    if [ -f "$dir/package.json" ]; then
        npm outdated --json 2>/dev/null
    fi

    if [ -f "$dir/requirements.txt" ]; then
        pip list --outdated --format json 2>/dev/null
    fi
}
```

## Output Format

```json
{
  "dependency_analysis": {
    "total_count": 45,
    "production_count": 12,
    "development_count": 33,

    "by_category": {
      "framework": ["fastify"],
      "database": ["prisma", "pg"],
      "testing": ["vitest", "@testing-library/react"],
      "build": ["typescript", "esbuild"]
    },

    "graph": {
      "nodes": [...],
      "edges": [...]
    },

    "security": {
      "vulnerabilities": 0,
      "outdated": 3,
      "deprecated": 0
    },

    "recommendations": [
      {"package": "lodash", "action": "update", "from": "4.17.20", "to": "4.17.21"}
    ]
  }
}
```
