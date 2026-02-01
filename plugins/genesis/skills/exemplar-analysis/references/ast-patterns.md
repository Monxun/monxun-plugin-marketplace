# AST Patterns Reference

Detailed patterns for Abstract Syntax Tree parsing and analysis.

## Tree-sitter Integration

### Supported Languages
| Language | Parser | Query Pattern |
|----------|--------|---------------|
| TypeScript | `tree-sitter-typescript` | `(function_declaration name: (identifier) @name)` |
| Python | `tree-sitter-python` | `(function_definition name: (identifier) @name)` |
| Go | `tree-sitter-go` | `(function_declaration name: (identifier) @name)` |
| Rust | `tree-sitter-rust` | `(function_item name: (identifier) @name)` |

## Common Queries

### Extract Function Names
```scheme
; TypeScript/JavaScript
(function_declaration
  name: (identifier) @function.name)

(arrow_function
  parameters: (formal_parameters) @function.params)

(method_definition
  name: (property_identifier) @method.name)
```

### Extract Class Definitions
```scheme
; TypeScript
(class_declaration
  name: (type_identifier) @class.name
  body: (class_body) @class.body)

; Python
(class_definition
  name: (identifier) @class.name
  body: (block) @class.body)
```

### Extract Imports
```scheme
; TypeScript/JavaScript
(import_statement
  source: (string) @import.source)

(import_clause
  (named_imports
    (import_specifier
      name: (identifier) @import.name)))

; Python
(import_statement
  name: (dotted_name) @import.module)

(import_from_statement
  module_name: (dotted_name) @import.from
  name: (identifier) @import.name)
```

## Pattern Recognition Heuristics

### Function Complexity
```python
def calculate_complexity(ast_node):
    """Calculate cyclomatic complexity from AST."""
    complexity = 1
    for node in ast_node.children:
        if node.type in ['if_statement', 'while_statement', 'for_statement']:
            complexity += 1
        elif node.type == 'try_statement':
            complexity += len([c for c in node.children if c.type == 'except_clause'])
    return complexity
```

### Dependency Extraction
```python
def extract_dependencies(source_file):
    """Extract import dependencies from source file."""
    tree = parser.parse(source_file)
    imports = []

    for node in tree.root_node.children:
        if node.type == 'import_statement':
            imports.append({
                'type': 'import',
                'module': node.children[1].text.decode()
            })
        elif node.type == 'import_from_statement':
            imports.append({
                'type': 'from',
                'module': node.children[1].text.decode(),
                'names': [n.text.decode() for n in node.children if n.type == 'identifier']
            })

    return imports
```

## Architecture Detection via AST

### Layered Architecture Indicators
```python
def detect_layered_architecture(project_path):
    """Detect layered architecture patterns via AST analysis."""
    indicators = {
        'controllers': [],
        'services': [],
        'repositories': []
    }

    for file in glob.glob(f"{project_path}/**/*.ts", recursive=True):
        tree = parse_file(file)

        # Check for controller decorators
        if has_decorator(tree, '@Controller'):
            indicators['controllers'].append(file)

        # Check for service decorators or naming
        if has_decorator(tree, '@Service') or 'Service' in file:
            indicators['services'].append(file)

        # Check for repository patterns
        if 'Repository' in file or has_decorator(tree, '@Repository'):
            indicators['repositories'].append(file)

    return indicators
```

### Microservice Detection
```python
def detect_microservices(project_path):
    """Detect microservice boundaries via AST and config analysis."""
    services = []

    # Find all package.json or go.mod files
    for config in glob.glob(f"{project_path}/**/package.json", recursive=True):
        if 'node_modules' in config:
            continue

        # Analyze entry points
        entry_points = find_entry_points(config)

        # Check for HTTP server setup
        if has_http_server(entry_points):
            services.append({
                'path': os.path.dirname(config),
                'type': 'http',
                'entry': entry_points
            })

    return services
```

## Output Format

```json
{
  "ast_analysis": {
    "functions": [
      {"name": "getUserById", "complexity": 3, "lines": 15}
    ],
    "classes": [
      {"name": "UserService", "methods": 5, "dependencies": ["UserRepository"]}
    ],
    "imports": [
      {"module": "@prisma/client", "names": ["PrismaClient"]}
    ],
    "architecture_indicators": {
      "pattern": "layered",
      "confidence": 0.85,
      "evidence": ["controller decorators", "service layer"]
    }
  }
}
```
