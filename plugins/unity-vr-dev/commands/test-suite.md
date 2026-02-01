---
name: test-suite
description: Run Unity VR test suite with coverage and performance benchmarks
allowed-tools: Read, Write, Bash, Grep, Glob, Task
argument-validation: optional
---

# Test Suite

Run the Unity VR test suite with optional coverage reporting and performance benchmarks.

## Usage

```
/unity-vr-dev:test-suite [mode]
```

## Modes

- `all` — Run all tests (default)
- `editmode` — EditMode tests only
- `playmode` — PlayMode tests only
- `performance` — Performance benchmarks only
- `coverage` — All tests with coverage report

## Options

- `--category <name>` — Filter by test category (e.g., "VR", "Build")
- `--ci` — Generate CI-compatible output (XML results)

## Workflow

1. Delegate to **orchestrator** for environment validation
2. Orchestrator routes to **test-agent**
3. Test agent runs requested test mode via MCP or Unity CLI
4. Collects results, coverage, and performance data
5. Reports summary with pass/fail, coverage %, and frame budget compliance

## Prerequisites

- Unity Editor running with project open
- Unity Test Framework package installed
- For performance tests: Unity Performance Testing package
- For coverage: Code Coverage package

## Examples

```
/unity-vr-dev:test-suite
/unity-vr-dev:test-suite playmode
/unity-vr-dev:test-suite performance
/unity-vr-dev:test-suite coverage --category VR
```
