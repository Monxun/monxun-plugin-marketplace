---
name: flutter-firebase-deploy:run-cli
description: Launch flutter-deploy CLI interactive mode for guided deployment setup
---

# Run Flutter Deploy CLI

Launch the flutter-deploy CLI in interactive mode for guided deployment setup.

## Usage

```
/flutter-firebase-deploy:run-cli [path] [--phase <phase>]
```

## Arguments

- `path` - Optional path to Flutter project (defaults to current directory)
- `--phase <phase>` - Skip to a specific phase

## Available Phases

| Phase | Name | Description |
|-------|------|-------------|
| 1 | analyze | Scan Flutter app for permissions & features |
| 2 | app_stores | Setup App Store Connect & Play Console |
| 3 | firebase | Configure Firebase project & services |
| 4 | oauth | Setup authentication providers |
| 5 | configure | Interactive configuration wizard |
| 6 | fastlane | Generate Fastlane automation |
| 7 | credentials | Setup code signing & secrets |
| 8 | github_actions | Generate CI/CD workflows |
| 9 | runner_setup | Setup self-hosted Mac Mini runner |

## What This Does

1. Verifies flutter-deploy CLI is installed
2. Validates Flutter project at specified path
3. Launches interactive CLI interface
4. Guides through selected deployment phases

## Interactive Features

- Beautiful terminal UI with navigation
- Progress tracking across phases
- Configuration export/import
- Help documentation

## Example

```
# Full interactive mode
/flutter-firebase-deploy:run-cli

# Specific project path
/flutter-firebase-deploy:run-cli ./my-flutter-app

# Jump to specific phase
/flutter-firebase-deploy:run-cli --phase fastlane
```

## Note

This command launches an interactive terminal application. It requires a terminal that supports ANSI colors and cursor movement.
