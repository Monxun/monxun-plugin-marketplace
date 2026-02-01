---
name: create-template
description: Create a production-ready project template from example projects, prompts, and web research
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebSearch, WebFetch
argument-validation: optional
---

# Create Template Command

Generate a production-ready project template with multi-agent orchestration.

## Usage

```
/genesis:create-template [options]
```

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--from <path>` | Learn from existing project | `--from ./my-project` |
| `--name <name>` | Template name (kebab-case) | `--name fastapi-api` |
| `--description <desc>` | Template description | `--description "FastAPI template"` |
| `--include-workflows` | Generate GitHub Actions | Flag |
| `--include-infra <provider>` | Generate IaC | `--include-infra terraform` |
| `--research-depth <level>` | Web research depth | `--research-depth deep` |

## Arguments

- `$1` - Template name or path to example project
- `$ARGUMENTS` - Full argument string

## Workflow

This command delegates to the `orchestrator` agent which coordinates:

1. **Ingestion Phase** - Analyze example project via `exemplar-analyzer`
2. **Research Phase** - Web research via `web-researcher`
3. **Synthesis Phase** - Pattern extraction via `pattern-extractor`
4. **Generation Phase** - Template creation via specialist builders
5. **Validation Phase** - Quality checks via `genesis-validator`
6. **Output Phase** - Documentation via `documenter`

## Examples

```bash
# Create from example project
/genesis:create-template --from ./my-fastapi-project --name fastapi-template

# Create from prompt with research
/genesis:create-template --name nextjs-app \
  --description "Next.js 15 with TypeScript and Tailwind" \
  --research-depth deep \
  --include-workflows

# Full template with infrastructure
/genesis:create-template --from ./example \
  --name fullstack-template \
  --include-workflows \
  --include-infra terraform
```

## Output

Creates a template directory with:
- `genesis.json` - Template manifest
- `templates/` - Parameterized source files
- `docs/` - README, QUICKSTART
- `.github/workflows/` - CI/CD (if requested)
- `terraform/` or `pulumi/` - IaC (if requested)

## Injected Skills

- `template-patterns` - GTL syntax and patterns
- `heuristics-engine` - Quality validation

## Next Steps

After creation:
```bash
/genesis:validate-template ./my-template
```
