---
name: create-marketplace
description: Create a plugin marketplace manifest for distribution
allowed-tools: Read, Write, Edit, Bash, Glob, WebFetch
argument-validation: optional
---

# Create Marketplace Command

Generate marketplace configuration for plugin distribution.

## Usage

```
/plugin-factory:create-marketplace [target-plugin]
```

## Arguments

- `$1` - Target plugin directory (optional, defaults to current)

## Workflow

1. Reads existing plugin.json
2. Validates plugin structure
3. Generates marketplace manifest
4. Creates distribution package
5. Validates against marketplace schema

## Marketplace Manifest

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "repository": "https://github.com/user/plugin",
  "keywords": ["claude-code", "plugin"],
  "license": "MIT",
  "engines": {
    "claude-code": ">=1.0.0"
  }
}
```

## Output

Creates:
- `marketplace.json` - Marketplace manifest
- `plugin-name-v1.0.0.zip` - Distribution package
- `CHANGELOG.md` - Version history (if not exists)

## Example

```bash
# Create marketplace manifest
/plugin-factory:create-marketplace

# Create for specific plugin
/plugin-factory:create-marketplace ./my-plugin
```

## Distribution

After creating marketplace files:

1. Host ZIP file publicly
2. Add to marketplace registry
3. Users install via marketplace URL
