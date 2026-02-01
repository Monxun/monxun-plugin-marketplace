# Variable Interpolation Reference

Complete reference for Genesis Template Language (GTL) variable syntax.

## Basic Syntax

### Simple Variables
```handlebars
{{ variable_name }}
```

Variables must be:
- Lowercase letters and underscores only
- Defined in `genesis.json` prompts

### With Whitespace Control
```handlebars
{{~ variable_name }}   <!-- Trim leading whitespace -->
{{ variable_name ~}}   <!-- Trim trailing whitespace -->
{{~ variable_name ~}}  <!-- Trim both -->
```

## Filters

### String Transformation
| Filter | Input | Output |
|--------|-------|--------|
| `kebab-case` | `MyProject` | `my-project` |
| `pascal-case` | `my-project` | `MyProject` |
| `camel-case` | `my-project` | `myProject` |
| `snake-case` | `MyProject` | `my_project` |
| `upper` | `hello` | `HELLO` |
| `lower` | `HELLO` | `hello` |
| `capitalize` | `hello world` | `Hello World` |
| `title` | `hello world` | `Hello World` |

### Usage
```handlebars
{{ project_name | kebab-case }}
{{ class_name | pascal-case }}
{{ CONSTANT_NAME | upper }}
```

### Chaining Filters
```handlebars
{{ input | trim | lower | kebab-case }}
```

## Default Values

### Simple Default
```handlebars
{{ variable | default: 'fallback_value' }}
```

### Variable as Default
```handlebars
{{ author_name | default: git_user_name }}
{{ author_email | default: git_user_email }}
```

### Conditional Default
```handlebars
{{ port | default: (use_https ? '443' : '80') }}
```

## Built-in Variables

### Git Context
| Variable | Description | Example |
|----------|-------------|---------|
| `git_user_name` | Git config user.name | `John Doe` |
| `git_user_email` | Git config user.email | `john@example.com` |
| `git_remote_url` | Git remote origin | `github.com/user/repo` |

### Environment
| Variable | Description | Example |
|----------|-------------|---------|
| `current_date` | ISO date | `2026-01-22` |
| `current_year` | Year | `2026` |
| `cwd_name` | Current directory name | `my-project` |

### Usage
```handlebars
{
  "author": "{{ author | default: git_user_name }}",
  "year": "{{ current_year }}"
}
```

## Escaping

### Literal Braces
```handlebars
\{{ this is not interpolated \}}

<!-- Or use raw block -->
{{{{raw}}}}
  {{ this is literal }}
{{{{/raw}}}}
```

### JSON Context
```handlebars
{
  "template": "{{ value | json-escape }}"
}
```

## Variable Validation

### In genesis.json
```json
{
  "prompts": [
    {
      "name": "project_name",
      "type": "string",
      "message": "Project name",
      "validate": "^[a-z][a-z0-9-]*$"
    },
    {
      "name": "port",
      "type": "number",
      "message": "Port number",
      "validate": "^[0-9]{2,5}$",
      "default": 3000
    }
  ]
}
```

### Validation Regex Patterns
| Pattern | Description |
|---------|-------------|
| `^[a-z][a-z0-9-]*$` | kebab-case identifier |
| `^[A-Z][a-zA-Z0-9]*$` | PascalCase identifier |
| `^[0-9]{2,5}$` | Port number (10-65535) |
| `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | Email |

## Complex Examples

### package.json Template
```handlebars
{
  "name": "{{ project_name | kebab-case }}",
  "version": "{{ version | default: '1.0.0' }}",
  "description": "{{ description }}",
  "author": {
    "name": "{{ author_name | default: git_user_name }}",
    "email": "{{ author_email | default: git_user_email }}"
  },
  "license": "{{ license | default: 'MIT' }}",
  "main": "{{ use_typescript ? 'dist/index.js' : 'src/index.js' }}"
}
```

### TypeScript Config
```handlebars
{
  "compilerOptions": {
    "target": "{{ ts_target | default: 'ES2022' }}",
    "module": "{{ ts_module | default: 'NodeNext' }}",
    "outDir": "{{ output_dir | default: 'dist' }}",
    "strict": {{ strict_mode | default: true }}
  }
}
```
