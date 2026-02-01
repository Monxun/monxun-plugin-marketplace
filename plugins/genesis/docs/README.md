# Genesis

AI-powered code templating and project scaffolding from examples, prompts, and web research.

## Overview

Genesis is a Claude Code plugin that creates production-ready repository templates by analyzing exemplar projects, researching current best practices, and synthesizing intelligent templates with proper variable interpolation.

## Features

- **Exemplar Analysis**: Deep analysis of existing projects to extract patterns
- **Web Research**: Real-time documentation mining for current best practices
- **Template Synthesis**: Intelligent template generation with GTL (Genesis Template Language)
- **GitHub Actions**: Automated CI/CD workflow generation
- **Infrastructure as Code**: Terraform, Pulumi, and Kubernetes manifest generation
- **Quality Gates**: Automated validation with structure, syntax, completeness, and security checks

## Quick Start

```bash
# Load the plugin
claude --plugin-dir ./plugins/genesis

# Create a template from an exemplar project
/genesis:create-template --exemplar ./my-project --name my-template

# Generate a project from a template
/genesis:create-template --template nodejs-api --name my-new-api
```

## Commands

| Command | Description |
|---------|-------------|
| `/genesis:create-template` | Create template from exemplar or generate from template |
| `/genesis:analyze-project` | Deep analysis of project structure and patterns |
| `/genesis:research-stack` | Research technologies and current best practices |
| `/genesis:generate-workflows` | Generate GitHub Actions CI/CD workflows |
| `/genesis:generate-infra` | Generate Infrastructure as Code |
| `/genesis:validate-template` | Validate template quality |
| `/genesis:publish-template` | Package template for distribution |

## Architecture

Genesis uses a multi-agent architecture with specialized agents for each phase:

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator (Opus)                  │
│           Master workflow coordination                   │
└────────────────────────┬────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
┌─────────┐        ┌─────────┐         ┌─────────┐
│Exemplar │        │   Web   │         │ Pattern │
│Analyzer │        │Researcher│        │Extractor│
└────┬────┘        └────┬────┘         └────┬────┘
     │                  │                   │
     └──────────────────┼───────────────────┘
                        ▼
              ┌─────────────────┐
              │    Template     │
              │   Synthesizer   │
              └────────┬────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │Workflow │  │  Infra  │  │  Doc    │
    │ Builder │  │Architect│  │ Writer  │
    └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
              ┌─────────────────┐
              │    Validator    │
              │  (Quality Gate) │
              └─────────────────┘
```

## Template Language (GTL)

Genesis uses a Handlebars-like template syntax:

```
{{ variable }}                    # Variable interpolation
{{ variable | default: 'value' }} # Default values
{{#if condition}}...{{/if}}       # Conditionals
{{#each items}}...{{/each}}       # Iteration
```

## Quality Gates

All generated templates pass through quality validation:

| Gate | Weight | Checks |
|------|--------|--------|
| Structure | 25% | Directory layout, file organization |
| Syntax | 25% | YAML/JSON/HCL parsing, linting |
| Completeness | 25% | Required files, dependency resolution |
| Security | 25% | No hardcoded secrets, secure defaults |

Minimum passing score: 80%

## Built-in Templates

Genesis includes production-ready scaffold templates:

- `nodejs-api` - Node.js API with Express/Fastify
- `python-fastapi` - Python FastAPI application
- `react-vite` - React + Vite + TypeScript
- `go-microservice` - Go microservice with Chi router
- `rust-cli` - Rust CLI with Clap

## Documentation

- [Quick Start Guide](./QUICKSTART.md)
- [Architecture Details](./ARCHITECTURE.md)

## License

MIT
