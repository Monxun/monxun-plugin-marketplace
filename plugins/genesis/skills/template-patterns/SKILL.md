---
name: template-patterns
description: |
  Template generation patterns for creating parameterized scaffolds.
  Use when: creating templates, variable interpolation, conditional generation,
  "create template", "scaffold project", template authoring, GTL syntax,
  Supports: Jinja2, Handlebars, Go templates, custom interpolation.
allowed-tools: Read, Write, Edit
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Template Patterns Skill

Generate parameterized templates using Genesis Template Language (GTL).

## Genesis Template Language (GTL)

### Variable Interpolation
```handlebars
{{!-- Basic variable --}}
{{ project_name }}

{{!-- With filter --}}
{{ project_name | kebab-case }}

{{!-- With default --}}
{{ author | default: 'Anonymous' }}
```

### Filters
| Filter | Input | Output |
|--------|-------|--------|
| `kebab-case` | `MyProject` | `my-project` |
| `pascal-case` | `my-project` | `MyProject` |
| `camel-case` | `my-project` | `myProject` |
| `snake-case` | `MyProject` | `my_project` |
| `upper` | `hello` | `HELLO` |
| `lower` | `HELLO` | `hello` |

### Conditional Blocks
```handlebars
{{#if use_typescript}}
"typescript": "^5.0.0"
{{/if}}

{{#if database == 'postgresql'}}
"pg": "^8.11.0"
{{else if database == 'mysql'}}
"mysql2": "^3.6.0"
{{else}}
{{!-- No database --}}
{{/if}}

{{#unless skip_tests}}
"vitest": "^1.0.0"
{{/unless}}
```

### Iteration
```handlebars
{{#each dependencies}}
"{{ this.name }}": "{{ this.version }}"{{#unless @last}},{{/unless}}
{{/each}}
```

### Context Variables
| Variable | Description |
|----------|-------------|
| `this` | Current item |
| `@index` | Current index (0-based) |
| `@first` | Is first item |
| `@last` | Is last item |
| `@key` | Object key |

## Template File Structure

### package.json.template
```json
{
  "name": "{{ project_name | kebab-case }}",
  "version": "{{ version | default: '1.0.0' }}",
  "description": "{{ description }}",
  {{#if use_typescript}}
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  {{else}}
  "main": "src/index.js",
  {{/if}}
  "scripts": {
    "dev": "{{ dev_command }}",
    "build": "{{ build_command }}",
    "test": "{{ test_command }}"
  }
}
```

### Conditional Directory Structure
```
templates/
├── src/
│   └── index.ts.template
{{#if use_routes}}
├── src/routes/
│   └── index.ts.template
{{/if}}
{{#if use_docker}}
├── Dockerfile.template
├── docker-compose.yml.template
{{/if}}
```

## Template Manifest (genesis.json)

```json
{
  "name": "template-name",
  "version": "1.0.0",
  "description": "Template description",

  "prompts": [
    {
      "name": "project_name",
      "type": "string",
      "message": "Project name",
      "validate": "^[a-z][a-z0-9-]*$"
    },
    {
      "name": "use_typescript",
      "type": "boolean",
      "message": "Use TypeScript?",
      "default": true
    },
    {
      "name": "database",
      "type": "select",
      "message": "Database",
      "choices": ["postgresql", "mysql", "none"],
      "default": "postgresql"
    }
  ],

  "conditionals": {
    "docker/": "use_docker",
    "terraform/": "include_infrastructure"
  },

  "postGeneration": [
    "npm install",
    "git init"
  ]
}
```

## Prompt Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text input | Project name |
| `boolean` | Yes/No | Use TypeScript? |
| `select` | Single choice | Database type |
| `multiselect` | Multiple choices | Features to include |
| `number` | Numeric | Port number |

## Quick Patterns

### Comment Block
```handlebars
{{!-- This comment won't appear in output --}}
```

### Smart Defaults from Git
```handlebars
{{ author_name | default: git_user_name }}
{{ author_email | default: git_user_email }}
```

### Conditional JSON Comma
```handlebars
{{#each items}}
"{{ this }}"{{#unless @last}},{{/unless}}
{{/each}}
```

## Detailed References

- [Variable Interpolation](references/variable-interpolation.md) - Full variable syntax
- [Conditional Blocks](references/conditional-blocks.md) - Complex conditional logic
- [Iteration Patterns](references/iteration-patterns.md) - Array and object iteration
