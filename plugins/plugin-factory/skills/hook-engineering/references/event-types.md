# Hook Event Types Reference

Complete reference for all 12 Claude Code hook event types.

## PreToolUse

**When**: Before Claude executes any tool
**Matcher**: Tool name pattern (regex supported)
**Purpose**: Validate, modify, or block tool calls

### Input Schema
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  },
  "tool_use_id": "toolu_01ABC..."
}
```

### Common Matchers
- `Write` - File creation
- `Edit` - File modification
- `Bash` - Shell commands
- `Write|Edit` - Either
- `mcp__.*` - All MCP tools
- `*` or `""` - All tools

### Use Cases
- Validate file paths
- Block dangerous commands
- Modify tool inputs
- Auto-approve safe operations

## PostToolUse

**When**: After successful tool execution
**Matcher**: Tool name pattern
**Purpose**: Format, validate output, inject context

### Input Schema
```json
{
  "session_id": "abc123",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "content"
  },
  "tool_response": {
    "filePath": "/path/to/file",
    "success": true
  },
  "tool_use_id": "toolu_01ABC..."
}
```

### Use Cases
- Auto-format written files
- Run linters
- Update indexes
- Inject additional context

## PostToolUseFailure

**When**: After tool execution fails
**Matcher**: Tool name pattern
**Purpose**: Handle errors, cleanup, retry logic

### Use Cases
- Log failures
- Clean up partial operations
- Notify about errors

## PermissionRequest

**When**: Permission dialog shown to user
**Matcher**: Tool name pattern
**Purpose**: Auto-approve or deny permissions

### Input Schema
```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

### Use Cases
- Auto-approve safe commands
- Block dangerous operations
- Implement custom permission logic

## UserPromptSubmit

**When**: User submits a prompt
**Matcher**: None
**Purpose**: Validate prompts, inject context

### Input Schema
```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "User's submitted prompt text"
}
```

### Use Cases
- Block sensitive prompts
- Inject project context
- Add timestamps
- Prompt enhancement

## Notification

**When**: Claude sends notifications
**Matcher**: Notification type
**Purpose**: External alerting

### Matcher Values
- `permission_prompt` - Permission requests
- `idle_prompt` - Idle notifications
- `auth_success` - Auth completed
- `elicitation_dialog` - MCP elicitation

### Use Cases
- Desktop notifications
- Slack alerts
- Custom logging

## Stop

**When**: Claude attempts to finish
**Matcher**: None
**Purpose**: Quality gates, task completion validation

### Input Schema
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**Important**: Check `stop_hook_active` to prevent infinite loops.

### Use Cases
- Enforce task completion
- Run final validation
- Generate summaries

## SubagentStart

**When**: Subagent begins execution
**Matcher**: Agent name
**Purpose**: Setup, logging, resource allocation

### Use Cases
- Initialize resources
- Log agent activity
- Set up monitoring

## SubagentStop

**When**: Subagent completes
**Matcher**: Agent name
**Purpose**: Cleanup, validation, handoff

### Use Cases
- Validate subagent output
- Clean up resources
- Continue workflow

## SessionStart

**When**: Session begins or resumes
**Matcher**: Source type
**Purpose**: Initialize environment, inject context

### Matcher Values
- `startup` - Fresh start
- `resume` - Resuming session
- `clear` - After /clear
- `compact` - After compaction

### Special Feature: CLAUDE_ENV_FILE
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export MY_VAR=value' >> "$CLAUDE_ENV_FILE"
fi
```

### Use Cases
- Set environment variables
- Load project context
- Install dependencies

## SessionEnd

**When**: Session terminates
**Matcher**: None
**Purpose**: Cleanup, logging, state persistence

### Input Schema
```json
{
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

### Reason Values
- `clear` - /clear command
- `logout` - User logged out
- `prompt_input_exit` - User exited at prompt
- `other` - Other reasons

### Use Cases
- Save session state
- Clean up resources
- Log session statistics

## PreCompact

**When**: Before context compaction
**Matcher**: Trigger type
**Purpose**: Preserve important context

### Matcher Values
- `manual` - /compact command
- `auto` - Automatic compaction

### Use Cases
- Save context before compaction
- Inject summary instructions
