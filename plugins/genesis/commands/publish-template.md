---
name: publish-template
description: Package and publish a Genesis template for distribution
allowed-tools: Read, Write, Bash
argument-validation: required
---

# Publish Template Command

Package a validated Genesis template for distribution.

## Usage

```
/genesis:publish-template <template-path> [options]
```

## Arguments

- `$1` - Path to template directory (required)
- `$ARGUMENTS` - Full argument string

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--registry <name>` | Target registry (github, npm, local) | local |
| `--version <version>` | Version to publish | from genesis.json |
| `--dry-run` | Preview without publishing | false |
| `--skip-validation` | Skip pre-publish validation | false |

## Registries

### GitHub
- Creates/updates GitHub repository
- Configures as template repository
- Sets up releases

### npm
- Publishes as npm package
- Uses `create-*` naming convention
- Enables `npm init` usage

### Local
- Creates distributable archive
- Generates checksums
- Ready for manual distribution

## Pre-Publish Checks

1. **Validation** - Run full quality gates
2. **Version** - Verify semver format
3. **Documentation** - Ensure README exists
4. **License** - Verify license file

## Examples

```bash
# Publish to GitHub
/genesis:publish-template ./my-template --registry github

# Publish to npm
/genesis:publish-template ./my-template --registry npm --version 1.0.0

# Create local archive
/genesis:publish-template ./my-template --registry local

# Dry run
/genesis:publish-template ./my-template --registry github --dry-run
```

## Output

### GitHub
```
Published to: https://github.com/user/template-name
Version: v1.0.0
Use: npx degit user/template-name my-project
```

### npm
```
Published to: https://www.npmjs.com/package/create-template-name
Version: 1.0.0
Use: npm init template-name my-project
```

### Local
```
Created: template-name-1.0.0.tar.gz
SHA256: abc123...
Size: 45.2 KB
```

## Injected Skills

- `template-patterns` - Package configuration

## Delegates To

- `documenter` agent for final documentation
- `genesis-validator` for pre-publish validation

## Post-Publish

After publishing:
1. Template is available for use
2. Version is tagged
3. Changelog is updated (if configured)
