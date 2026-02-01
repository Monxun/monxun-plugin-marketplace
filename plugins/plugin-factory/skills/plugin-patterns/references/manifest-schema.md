# Plugin Manifest Schema Reference

Complete schema for `.claude-plugin/plugin.json`.

## Schema Overview

```json
{
  "name": "string (required)",
  "version": "string (semver)",
  "description": "string",
  "author": {
    "name": "string (required if author present)",
    "email": "string",
    "url": "string"
  },
  "homepage": "string (URL)",
  "repository": "string (URL)",
  "license": "string (SPDX)",
  "keywords": ["string"],
  "commands": "string | string[]",
  "agents": "string | string[]",
  "skills": "string | string[]",
  "hooks": "string | object",
  "mcpServers": "string | object",
  "lspServers": "string | object",
  "outputStyles": "string | string[]"
}
```

## Required Fields

### name
- **Type**: string
- **Required**: Yes
- **Pattern**: kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`)
- **Max Length**: 64 characters

```json
{
  "name": "my-awesome-plugin"
}
```

**Validation**:
```bash
echo "my-plugin" | grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'
```

## Metadata Fields

### version
- **Type**: string
- **Format**: Semantic versioning (semver)

```json
{
  "version": "1.0.0"
}
```

### description
- **Type**: string
- **Purpose**: Brief explanation of plugin purpose

```json
{
  "description": "Automates deployment workflows"
}
```

### author
- **Type**: object
- **Fields**: name (required), email, url

```json
{
  "author": {
    "name": "Developer Name",
    "email": "dev@example.com",
    "url": "https://example.com"
  }
}
```

### homepage
- **Type**: string (URL)
- **Purpose**: Documentation/landing page

```json
{
  "homepage": "https://docs.example.com/plugin"
}
```

### repository
- **Type**: string (URL)
- **Purpose**: Source code location

```json
{
  "repository": "https://github.com/user/plugin"
}
```

### license
- **Type**: string (SPDX identifier)
- **Common values**: MIT, Apache-2.0, GPL-3.0

```json
{
  "license": "MIT"
}
```

### keywords
- **Type**: string[]
- **Purpose**: Discovery and categorization

```json
{
  "keywords": ["deployment", "ci-cd", "automation"]
}
```

## Component Path Fields

### commands
- **Type**: string | string[]
- **Purpose**: Paths to command directories/files

```json
{
  "commands": "./commands/"
}
```

Or multiple paths:
```json
{
  "commands": ["./commands/", "./extra-commands/"]
}
```

### agents
- **Type**: string | string[]
- **Purpose**: Paths to agent files

```json
{
  "agents": "./agents/"
}
```

### skills
- **Type**: string | string[]
- **Purpose**: Paths to skill directories

```json
{
  "skills": "./skills/"
}
```

### outputStyles
- **Type**: string | string[]
- **Purpose**: Custom output formatting styles

```json
{
  "outputStyles": "./styles/"
}
```

## Configuration Fields

### hooks
- **Type**: string | object
- **Purpose**: Hook configuration

**Path reference**:
```json
{
  "hooks": "./hooks/hooks.json"
}
```

**Inline configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{"type": "command", "command": "./validate.sh"}]
      }
    ]
  }
}
```

### mcpServers
- **Type**: string | object
- **Purpose**: MCP server configuration

**Path reference**:
```json
{
  "mcpServers": "./.mcp.json"
}
```

**Inline configuration**:
```json
{
  "mcpServers": {
    "mcpServers": {
      "my-server": {
        "command": "${CLAUDE_PLUGIN_ROOT}/server.js"
      }
    }
  }
}
```

### lspServers
- **Type**: string | object
- **Purpose**: LSP server configuration

**Path reference**:
```json
{
  "lspServers": "./.lsp.json"
}
```

**Inline configuration**:
```json
{
  "lspServers": {
    "lspServers": {
      "python": {
        "command": "pylsp",
        "extensionToLanguage": {
          ".py": "python"
        }
      }
    }
  }
}
```

## Complete Example

```json
{
  "name": "deployment-tools",
  "version": "1.0.0",
  "description": "Automated deployment and CI/CD integration",
  "author": {
    "name": "DevOps Team",
    "email": "devops@company.com",
    "url": "https://company.com/team"
  },
  "homepage": "https://docs.company.com/deployment-tools",
  "repository": "https://github.com/company/deployment-tools",
  "license": "MIT",
  "keywords": ["deployment", "ci-cd", "automation", "devops"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

## Validation

### JSON Syntax
```bash
jq . .claude-plugin/plugin.json
```

### Required Fields
```bash
jq -e '.name' .claude-plugin/plugin.json
```

### Name Format
```bash
jq -r '.name' .claude-plugin/plugin.json | grep -E '^[a-z0-9]+(-[a-z0-9]+)*$'
```

### Path Existence
```bash
COMMANDS=$(jq -r '.commands // empty' .claude-plugin/plugin.json)
[ -z "$COMMANDS" ] || [ -e "$COMMANDS" ] || echo "Missing: $COMMANDS"
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `"name": "My Plugin"` | Contains spaces/uppercase | `"name": "my-plugin"` |
| `"version": "1"` | Not semver | `"version": "1.0.0"` |
| `"commands": "/absolute/path"` | Absolute path | `"commands": "./commands/"` |
| Components in .claude-plugin/ | Won't load | Move to plugin root |
