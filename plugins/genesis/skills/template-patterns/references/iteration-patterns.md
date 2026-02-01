# Iteration Patterns Reference

Complete reference for GTL loops and iteration.

## Each Block

### Array Iteration
```handlebars
{{#each items}}
  {{ this }}
{{/each}}
```

### With Index
```handlebars
{{#each items}}
  {{ @index }}: {{ this }}
{{/each}}
```

### Object Iteration
```handlebars
{{#each object}}
  {{ @key }}: {{ this }}
{{/each}}
```

## Context Variables

| Variable | Description | Type |
|----------|-------------|------|
| `this` | Current item value | any |
| `@index` | Zero-based index | number |
| `@first` | Is first iteration | boolean |
| `@last` | Is last iteration | boolean |
| `@key` | Object property name | string |
| `@root` | Root context | object |

## JSON Generation

### Array to JSON Array
```handlebars
[
{{#each items}}
  "{{ this }}"{{#unless @last}},{{/unless}}
{{/each}}
]
```

### Array to JSON Object
```handlebars
{
{{#each dependencies}}
  "{{ this.name }}": "{{ this.version }}"{{#unless @last}},{{/unless}}
{{/each}}
}
```

### Nested Objects
```handlebars
{
{{#each services}}
  "{{ @key }}": {
    "port": {{ this.port }},
    "enabled": {{ this.enabled }}
  }{{#unless @last}},{{/unless}}
{{/each}}
}
```

## File Generation

### Generate Multiple Files
```handlebars
{{#each routes}}
// File: src/routes/{{ this.name }}.ts
import { Router } from 'express';

const router = Router();

router.get('/', (req, res) => {
  res.json({ message: '{{ this.name }} route' });
});

export default router;
{{/each}}
```

### Generate Index File
```handlebars
// src/routes/index.ts
{{#each routes}}
import {{ this.name }}Router from './{{ this.name }}';
{{/each}}

export const routes = {
{{#each routes}}
  '{{ this.path }}': {{ this.name }}Router{{#unless @last}},{{/unless}}
{{/each}}
};
```

## Conditional Iteration

### Filter During Iteration
```handlebars
{{#each dependencies}}
  {{#if this.type == 'production'}}
  "{{ this.name }}": "{{ this.version }}"{{#unless @last}},{{/unless}}
  {{/if}}
{{/each}}
```

### Conditional Content
```handlebars
{{#each features}}
  {{#if @first}}
  <!-- First feature has special styling -->
  <div class="featured">{{ this.name }}</div>
  {{else}}
  <div class="normal">{{ this.name }}</div>
  {{/if}}
{{/each}}
```

## Nested Iteration

### Two-Level Deep
```handlebars
{{#each categories}}
## {{ this.name }}
{{#each this.items}}
- {{ this }}
{{/each}}
{{/each}}
```

### With Parent Context
```handlebars
{{#each categories}}
{{#each this.items}}
Category: {{ @root.categories.[@index].name }} - Item: {{ this }}
{{/each}}
{{/each}}
```

## Complex Examples

### package.json Dependencies
```handlebars
{
  "dependencies": {
{{#each dependencies}}
{{#if this.type == 'production'}}
    "{{ this.name }}": "{{ this.version }}"{{#unless @last}},{{/unless}}
{{/if}}
{{/each}}
  },
  "devDependencies": {
{{#each dependencies}}
{{#if this.type == 'development'}}
    "{{ this.name }}": "{{ this.version }}"{{#unless @last}},{{/unless}}
{{/if}}
{{/each}}
  }
}
```

### GitHub Actions Matrix
```yaml
jobs:
  test:
    strategy:
      matrix:
        include:
{{#each test_matrix}}
          - os: {{ this.os }}
            node: {{ this.node }}
{{#if this.env}}
            env:
{{#each this.env}}
              {{ @key }}: {{ this }}
{{/each}}
{{/if}}
{{/each}}
```

### Docker Compose Services
```yaml
services:
{{#each services}}
  {{ this.name }}:
    image: {{ this.image }}
    ports:
{{#each this.ports}}
      - "{{ this.host }}:{{ this.container }}"
{{/each}}
{{#if this.environment}}
    environment:
{{#each this.environment}}
      {{ @key }}: {{ this }}
{{/each}}
{{/if}}
{{#if this.depends_on}}
    depends_on:
{{#each this.depends_on}}
      - {{ this }}
{{/each}}
{{/if}}
{{/each}}
```

### Route Registration
```handlebars
// src/app.ts
import express from 'express';
{{#each routes}}
import {{ this.name | camel-case }}Router from './routes/{{ this.name }}';
{{/each}}

const app = express();

{{#each routes}}
app.use('{{ this.path }}', {{ this.name | camel-case }}Router);
{{/each}}

export default app;
```

## Empty Handling

```handlebars
{{#each items}}
  {{ this }}
{{else}}
  No items found
{{/each}}
```
