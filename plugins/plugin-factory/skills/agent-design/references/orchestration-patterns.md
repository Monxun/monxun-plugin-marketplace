# Agent Orchestration Patterns

Patterns for coordinating multiple agents in workflows.

## Single-Agent Patterns

### Specialist Delegation
Main conversation delegates to a specialist:

```
User → Claude → Specialist Agent → Result → Claude → User
```

Use when:
- Task requires domain expertise
- Want to isolate context
- Need specific tool restrictions

### Validator Pattern
After construction, delegate validation:

```
Construction → Validator Agent → Pass/Fail → Continue/Fix
```

```yaml
name: validator
tools: Read, Bash, Grep
disallowedTools: Write, Edit
model: haiku
```

## Multi-Agent Patterns

### Sequential Pipeline
Agents process in order:

```
Agent A → Agent B → Agent C → Result
```

```markdown
## Workflow

1. Delegate to clarification agent
2. Pass requirements to planner agent
3. Pass plan to builder agent
4. Pass output to validator agent
```

### Parallel Research
Multiple agents research simultaneously:

```
                ┌─→ Research Agent A ─┐
User Request ──┼─→ Research Agent B ──┼─→ Synthesis
                └─→ Research Agent C ─┘
```

```markdown
Research authentication, database, and API modules
in parallel using separate subagents
```

### Orchestrator Pattern
Central agent coordinates specialists:

```
              ┌─→ Specialist A
Orchestrator ─┼─→ Specialist B
              └─→ Specialist C
```

Orchestrator agent:
```yaml
name: orchestrator
tools: Task, Read, Bash
model: sonnet
skills: workflow-skill
```

### Validator Loop
Iterative validation and fixing:

```
Build → Validate → [Pass] → Done
          ↓
        [Fail]
          ↓
        Fix → Build → ...
        (max 5 iterations)
```

## Agent Communication

### Context Handoff
Pass context between agents:

```markdown
When delegating to next agent, provide:
- Previous results
- Current phase
- Remaining tasks
- Constraints
```

### Result Format
Standardize agent outputs:

```json
{
  "status": "success|error",
  "phase": "current phase",
  "results": {},
  "nextSteps": []
}
```

## Quality Gate Pattern

Insert validation between phases:

```
Phase 1 → Gate 1 → Phase 2 → Gate 2 → Phase 3
```

Gate agent:
```yaml
name: quality-gate
description: |
  Validates output meets criteria before next phase.
  Use when: between workflow phases.
tools: Read, Bash, Grep
disallowedTools: Write, Edit
model: haiku
```

## Background Processing

### Parallel Execution
Run agents concurrently:

```markdown
Research authentication, database, and API modules
using separate background subagents
```

### Foreground Dependencies
Serialize dependent tasks:

```markdown
First use planner agent to design architecture.
Then use builder agent to implement.
Finally use validator to test.
```

## Error Recovery

### Retry Pattern
```markdown
If agent fails:
1. Capture error
2. Retry up to 3 times
3. If still failing, escalate
```

### Fallback Pattern
```markdown
Try specialist agent.
If fails, fall back to general-purpose.
```

### Recovery Agent
```yaml
name: recovery
description: |
  Handles failed operations and errors.
  Use when: other agents fail.
tools: Read, Bash, Grep
```

## Best Practices

### 1. Single Responsibility
Each agent does one thing well.

### 2. Clear Handoffs
Define what passes between agents.

### 3. Idempotency
Agent actions should be safe to retry.

### 4. Failure Handling
Every agent should handle errors.

### 5. Progress Tracking
Track which phase is complete.

## Complete Example

```markdown
# Orchestrator Agent

## Workflow

### Phase 1: Discovery
1. Delegate to clarification agent
2. Delegate to researcher agent
3. Gate: Requirements complete?

### Phase 2: Planning
1. Delegate to planner agent
2. Gate: Architecture approved?

### Phase 3: Construction
1. Delegate to builder agents (parallel)
2. Gate: All components created?

### Phase 4: Verification
1. Delegate to validator agent
2. If fail: delegate to builder for fix
3. Loop max 5 times
4. Gate: All tests pass?

### Phase 5: Delivery
1. Delegate to documenter agent
2. Gate: Documentation complete?

## Error Handling

If any phase fails:
1. Log failure details
2. Attempt recovery
3. If unrecoverable, report and halt
```
