---
name: flutter-firebase-deploy:run-simulator-tests
description: Run tests on iOS Simulator or Android Emulator. Executes unit, widget, and integration tests.
---

# Run Simulator Tests

Execute tests on simulators/emulators.

## Usage

```
/flutter-firebase-deploy:run-simulator-tests [--platform ios|android] [--type unit|widget|integration]
```

## Options

- `--platform` - Target platform (default: both)
- `--type` - Test type (default: all)

## Test Types

- `unit` - Unit tests (test/unit/)
- `widget` - Widget tests (test/widget/)
- `integration` - Integration tests (integration_test/)

## What This Does

1. Boots appropriate simulator/emulator
2. Runs specified test suite
3. Captures screenshots on failure
4. Reports test results

## Example

```
/flutter-firebase-deploy:run-simulator-tests --platform ios --type integration
```
