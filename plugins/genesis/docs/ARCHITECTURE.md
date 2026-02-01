# Genesis Architecture

Technical architecture and design decisions for the Genesis plugin.

## System Overview

Genesis implements a multi-agent orchestration pattern with specialized agents for each phase of template generation.

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Request                              │
│     /genesis:create-template --exemplar ./project --name tpl     │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Model: Opus | Tools: Task, Read, Bash, Grep, Glob, WebSearch│  │
│  │ Coordinates 6-phase workflow                                │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
   ┌─────────┐           ┌─────────┐           ┌─────────┐
   │ Phase 1 │           │ Phase 2 │           │ Phase 3 │
   │Ingestion│           │Research │           │Synthesis│
   └─────────┘           └─────────┘           └─────────┘
        │                      │                      │
        ▼                      ▼                      ▼
   ┌─────────┐           ┌─────────┐           ┌─────────┐
   │ Phase 4 │           │ Phase 5 │           │ Phase 6 │
   │Generate │           │Validate │           │ Output  │
   └─────────┘           └─────────┘           └─────────┘
```

## Agent Architecture

### Agent Hierarchy

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Orchestrator | Opus | Task, Read, Bash, Grep, Glob, WebSearch | Master coordination |
| Exemplar Analyzer | Sonnet | Read, Grep, Glob, Bash | Project analysis |
| Web Researcher | Sonnet | Read, WebSearch, WebFetch | Documentation mining |
| Pattern Extractor | Sonnet | Read, Write, Bash | Pattern recognition |
| Template Synthesizer | Sonnet | Read, Write, Edit, Bash | Template generation |
| Workflow Builder | Sonnet | Read, Write, Edit, WebSearch | CI/CD workflows |
| Infra Architect | Sonnet | Read, Write, Edit, Bash | Infrastructure as Code |
| Validator | Haiku | Read, Bash | Quality validation |
| Documenter | Sonnet | Read, Write, Edit | Documentation |

### Tool Scoping Principles

1. **Minimum Privilege**: Each agent gets only the tools it needs
2. **Research vs Build**: Researchers get WebSearch, builders get Write/Edit
3. **Validation Safety**: Validator has no Write/Edit to prevent modification during validation

## 6-Phase Workflow

### Phase 1: Ingestion

**Agent**: Exemplar Analyzer

Analyzes input source (exemplar project, URL, or user prompt):
- Directory structure mapping
- Dependency extraction
- Configuration file detection
- Entry point identification

**Output**: Project analysis JSON conforming to `project-analysis.schema.json`

### Phase 2: Research

**Agent**: Web Researcher

Real-time web research for:
- Current framework versions
- Best practice documentation
- Security recommendations
- Alternative approaches

**Output**: Research context with sources and patterns

### Phase 3: Synthesis

**Agent**: Pattern Extractor + Template Synthesizer

Converts analysis into templates:
- Variable identification
- Conditional block detection
- Iteration pattern recognition
- GTL syntax generation

**Output**: Template files with GTL placeholders

### Phase 4: Generation

**Agents**: Workflow Builder, Infra Architect, Documenter

Parallel generation of:
- GitHub Actions workflows
- Terraform/Pulumi modules
- Kubernetes manifests
- README and documentation

**Output**: Complete template package

### Phase 5: Validation

**Agent**: Validator

Quality gate enforcement:
- Structure validation (25%)
- Syntax validation (25%)
- Completeness check (25%)
- Security scan (25%)

**Output**: Validation report with scores

### Phase 6: Output

**Agent**: Orchestrator

Final assembly and delivery:
- genesis.json manifest creation
- File organization
- Post-generation commands
- User output

## Genesis Template Language (GTL)

### Syntax Overview

GTL uses Handlebars-like syntax with custom extensions:

```handlebars
{{! Comment }}

{{ variable }}
{{ variable | default: 'fallback' }}
{{ variable | upper }}
{{ variable | kebab-case }}

{{#if condition}}
  content
{{else}}
  alternative
{{/if}}

{{#if language == 'typescript'}}
  TypeScript specific
{{/if}}

{{#each items}}
  {{ this.name }}: {{ this.value }}
{{/each}}

{{#each items as |item index|}}
  {{ index }}: {{ item.name }}
{{/each}}
```

### Variable Resolution

1. User-provided variables (highest priority)
2. Template defaults (genesis.json)
3. Inferred values (from analysis)
4. Built-in defaults (lowest priority)

## Quality Gates

### Structure Gate (25%)

Validates directory organization:
- Required directories exist
- File naming conventions
- No orphaned files
- Proper nesting depth

### Syntax Gate (25%)

Validates file syntax:
- JSON/YAML parseable
- HCL valid (Terraform)
- GTL syntax correct
- No unclosed blocks

### Completeness Gate (25%)

Validates template completeness:
- All referenced files exist
- Dependencies resolved
- Required variables defined
- Post-generate commands valid

### Security Gate (25%)

Validates security posture:
- No hardcoded secrets
- No exposed credentials
- Secure default values
- Proper permission settings

### Scoring

```
Overall Score = (Structure × 0.25) + (Syntax × 0.25) +
                (Completeness × 0.25) + (Security × 0.25)

Pass Threshold: 80%
Warning Threshold: 60%
```

## Hook System

### PreToolUse Hooks

Triggered before Write operations:
- Template syntax validation
- Variable interpolation check
- Security scan

### PostToolUse Hooks

Triggered after Write operations:
- Secret detection scan
- Syntax verification
- File organization check

### Stop Hooks

Triggered at session end:
- Generate validation report
- Cleanup temporary files
- Output summary

## Data Flow

```
┌────────────┐    ┌─────────────┐    ┌────────────┐
│  Exemplar  │───▶│  Analysis   │───▶│  Research  │
│  Project   │    │    JSON     │    │  Context   │
└────────────┘    └─────────────┘    └────────────┘
                                            │
                                            ▼
┌────────────┐    ┌─────────────┐    ┌────────────┐
│  Template  │◀───│  Synthesis  │◀───│  Patterns  │
│   Files    │    │   Engine    │    │   Catalog  │
└────────────┘    └─────────────┘    └────────────┘
      │
      ▼
┌────────────┐    ┌─────────────┐    ┌────────────┐
│ Validation │───▶│   Quality   │───▶│   Output   │
│   Report   │    │    Score    │    │  Package   │
└────────────┘    └─────────────┘    └────────────┘
```

## Extension Points

### Custom Templates

Add templates to `templates/project-scaffolds/`:
1. Create directory with scaffold name
2. Add `genesis.json` manifest
3. Add `.template` files

### Custom Workflows

Add workflow templates to `templates/workflows/`:
1. Create `*.yml.template` file
2. Use GTL syntax for variables
3. Document required variables

### Custom Infrastructure

Add infrastructure templates to `templates/infrastructure/`:
1. Create provider subdirectory
2. Add HCL/YAML templates
3. Include variable definitions

## Performance Considerations

### Parallel Execution

The orchestrator launches independent agents in parallel:
- Research and Analysis can run simultaneously
- Multiple builders (workflow, infra, docs) run in parallel
- Validation runs sequentially after generation

### Caching

- Web research results cached for 15 minutes
- Analysis results cached per-session
- Template parsing cached after first use

### Token Optimization

- Haiku model for validation (cost-effective)
- Sonnet for generation (balanced)
- Opus only for orchestration (complex reasoning)

## Error Handling

### Recoverable Errors

- Network timeouts: Retry with backoff
- Missing files: Prompt user for location
- Invalid syntax: Auto-fix when possible

### Non-Recoverable Errors

- Security violations: Hard stop
- Schema validation failures: Report and exit
- Permission errors: Surface to user

## Security Model

### Input Validation

- All user inputs sanitized
- Path traversal prevention
- URL validation and allowlisting

### Output Safety

- No secret interpolation
- Secure default permissions
- Credential detection and blocking

### Audit Trail

- All operations logged
- Template provenance tracked
- Research sources documented
