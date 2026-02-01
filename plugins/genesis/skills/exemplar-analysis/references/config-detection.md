# Config Detection Reference

Patterns for detecting and analyzing configuration files across different ecosystems.

## Configuration File Mapping

### Node.js/TypeScript
| File | Purpose | Key Fields |
|------|---------|------------|
| `package.json` | Project manifest | `dependencies`, `scripts`, `main` |
| `tsconfig.json` | TypeScript config | `compilerOptions`, `include` |
| `.env.example` | Environment template | Key-value pairs |
| `vite.config.ts` | Vite bundler | `plugins`, `build` |
| `next.config.js` | Next.js config | `experimental`, `images` |

### Python
| File | Purpose | Key Fields |
|------|---------|------------|
| `pyproject.toml` | Project metadata | `[project]`, `[tool]` |
| `requirements.txt` | Dependencies | Package==version |
| `setup.py` | Legacy packaging | `install_requires` |
| `.python-version` | Python version | Version string |

### Go
| File | Purpose | Key Fields |
|------|---------|------------|
| `go.mod` | Module definition | `module`, `require` |
| `go.sum` | Dependency checksums | Hash values |

### Rust
| File | Purpose | Key Fields |
|------|---------|------------|
| `Cargo.toml` | Crate manifest | `[package]`, `[dependencies]` |
| `Cargo.lock` | Locked versions | Resolved versions |

## Detection Patterns

### Language Detection Script
```bash
#!/bin/bash
detect_language() {
    local dir="$1"

    # TypeScript
    [ -f "$dir/tsconfig.json" ] && echo "typescript" && return

    # Python
    [ -f "$dir/pyproject.toml" ] || [ -f "$dir/requirements.txt" ] && echo "python" && return

    # Go
    [ -f "$dir/go.mod" ] && echo "go" && return

    # Rust
    [ -f "$dir/Cargo.toml" ] && echo "rust" && return

    # JavaScript (fallback)
    [ -f "$dir/package.json" ] && echo "javascript" && return

    echo "unknown"
}
```

### Framework Detection
```bash
#!/bin/bash
detect_framework() {
    local dir="$1"

    if [ -f "$dir/package.json" ]; then
        # Check for specific frameworks
        jq -r '.dependencies | keys[]' "$dir/package.json" 2>/dev/null | while read dep; do
            case "$dep" in
                next) echo "nextjs" ;;
                react) echo "react" ;;
                vue) echo "vue" ;;
                express) echo "express" ;;
                fastify) echo "fastify" ;;
                @nestjs/core) echo "nestjs" ;;
            esac
        done | head -1
    fi

    if [ -f "$dir/requirements.txt" ] || [ -f "$dir/pyproject.toml" ]; then
        grep -qE "^fastapi|fastapi==" "$dir/requirements.txt" 2>/dev/null && echo "fastapi"
        grep -qE "^django|django==" "$dir/requirements.txt" 2>/dev/null && echo "django"
        grep -qE "^flask|flask==" "$dir/requirements.txt" 2>/dev/null && echo "flask"
    fi
}
```

## Config Parsing

### package.json Analysis
```javascript
function analyzePackageJson(content) {
    const pkg = JSON.parse(content);

    return {
        name: pkg.name,
        version: pkg.version,
        type: pkg.type || 'commonjs',
        main: pkg.main,
        scripts: Object.keys(pkg.scripts || {}),
        dependencies: {
            production: Object.keys(pkg.dependencies || {}),
            development: Object.keys(pkg.devDependencies || {}),
            peer: Object.keys(pkg.peerDependencies || {})
        },
        engines: pkg.engines,
        workspaces: pkg.workspaces
    };
}
```

### pyproject.toml Analysis
```python
import tomllib

def analyze_pyproject(content):
    data = tomllib.loads(content)

    project = data.get('project', {})

    return {
        'name': project.get('name'),
        'version': project.get('version'),
        'python_requires': project.get('requires-python'),
        'dependencies': project.get('dependencies', []),
        'optional_dependencies': project.get('optional-dependencies', {}),
        'tools': list(data.get('tool', {}).keys())
    }
```

### Environment Variable Extraction
```bash
#!/bin/bash
extract_env_vars() {
    local file="$1"

    # Parse .env.example format
    grep -E "^[A-Z_]+=" "$file" 2>/dev/null | while read line; do
        name=$(echo "$line" | cut -d= -f1)
        value=$(echo "$line" | cut -d= -f2-)

        # Determine if sensitive
        is_sensitive="false"
        echo "$name" | grep -qiE "password|secret|key|token" && is_sensitive="true"

        echo "{\"name\": \"$name\", \"example\": \"$value\", \"sensitive\": $is_sensitive}"
    done
}
```

## Output Format

```json
{
  "config_analysis": {
    "language": "typescript",
    "framework": "fastify",
    "package_manager": "npm",

    "configs": [
      {
        "file": "package.json",
        "type": "package_manifest",
        "key_data": {
          "name": "my-api",
          "scripts": ["dev", "build", "test"]
        }
      },
      {
        "file": "tsconfig.json",
        "type": "typescript_config",
        "key_data": {
          "target": "ES2022",
          "module": "NodeNext"
        }
      }
    ],

    "environment_variables": [
      {"name": "DATABASE_URL", "sensitive": true, "required": true},
      {"name": "PORT", "sensitive": false, "default": "3000"}
    ]
  }
}
```
