# Plugin Factory Architecture

Design decisions, workflow patterns, and system architecture.

## Design Philosophy

### Progressive Disclosure

Keep main files concise, with detailed documentation in references:

```
skills/my-skill/
├── SKILL.md              # < 500 lines, core patterns
└── references/
    ├── overview.md       # Detailed explanation
    ├── patterns.md       # Advanced patterns
    └── examples.md       # Code examples
```

### Thin Wrapper Pattern

Commands are entry points that delegate to skills/agents:

```markdown
---
name: create-plugin
allowed-tools: Read, Write, Edit, Bash
---

# Create Plugin

Delegates to orchestrator agent...
```

### Tool Scoping

Agents have minimal tool access for their purpose:

| Agent Type | Tools |
|------------|-------|
| Read-only | Read, Grep, Glob |
| Research | Read, Grep, Glob, WebSearch |
| Builder | Read, Write, Edit, Bash |
| Validator | Read, Bash (no Write) |

## Workflow Architecture

### 5-Phase Plugin Generation

```
┌─────────────┐
│  Discovery  │  ← clarification agent
└──────┬──────┘
       ▼
┌─────────────┐
│  Research   │  ← researcher agent
└──────┬──────┘
       ▼
┌─────────────┐
│Architecture │  ← planner agent
└──────┬──────┘
       ▼
┌─────────────┐
│Construction │  ← builder agents
└──────┬──────┘
       ▼
┌─────────────┐
│Verification │  ← validator agent
└─────────────┘
```

### Agent Orchestration

The orchestrator routes to specialists:

```
User Request
     │
     ▼
┌────────────┐
│Orchestrator│
└─────┬──────┘
      │
   ┌──┴───┬────────┬────────┐
   ▼      ▼        ▼        ▼
Clarify Research  Plan    Build
   │      │        │        │
   └──────┴────────┴────────┘
                   │
                   ▼
              Validate
```

### Validation Loop

```
Validate → [Pass] → Done
    ↓
  [Fail]
    ↓
  Fix → Validate (max 5x)
    ↓
  [Still Fail]
    ↓
  Report Unresolved
```

## Component Architecture

### Plugin Structure

```
plugin/
├── .claude-plugin/
│   └── plugin.json       # Manifest ONLY
├── commands/             # Entry points
├── agents/               # Subagents
├── skills/               # Progressive skills
├── hooks/
│   ├── hooks.json        # Event config
│   └── scripts/          # Hook scripts
├── templates/            # Generation templates
├── schemas/              # Validation schemas
└── docs/                 # Documentation
```

### Manifest Design

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}
```

### Skill Design

```yaml
---
name: skill-name
description: |
  Description with trigger keywords.
  Use when: specific triggers.
  Supports: capabilities.
allowed-tools: Read, Write, Edit
model: claude-sonnet-4-20250514
context: fork
---
```

### Agent Design

```yaml
---
name: agent-name
description: Agent purpose and triggers
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit
permissionMode: default
skills: skill-to-inject
context: fork
---
```

## Hook Architecture

### Event Flow

```
User Action
     │
     ▼
PreToolUse Hook ──[Exit 2]──► Block
     │
     ▼
Tool Execution
     │
     ▼
PostToolUse Hook
     │
     ▼
Result to Claude
```

### Exit Code Semantics

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Continue, parse JSON output |
| 2 | Block | Block operation, show stderr |
| Other | Error | Non-blocking, continue |

## Quality Architecture

### Quality Gates

1. **Structure** (25%): Directory layout
2. **Schema** (25%): JSON/YAML validity
3. **Components** (25%): Frontmatter
4. **Quality** (25%): Progressive disclosure

### Scoring System

```
Score = (Structure × 0.25) + (Schema × 0.25) +
        (Components × 0.25) + (Quality × 0.25)

Grade: A (90+), B (80-89), C (70-79), D (60-69), F (<60)
```

## Extension Points

### Adding New Agents

1. Create `agents/new-agent.md` with frontmatter
2. Define tool scoping
3. Add to orchestrator routing
4. Create integration tests

### Adding New Skills

1. Create `skills/new-skill/SKILL.md`
2. Add `references/` for detailed docs
3. Keep SKILL.md < 500 lines
4. Include trigger keywords

### Adding New Hooks

1. Add event handler to `hooks.json`
2. Create script in `hooks/scripts/`
3. Set executable permissions
4. Test exit code behavior
