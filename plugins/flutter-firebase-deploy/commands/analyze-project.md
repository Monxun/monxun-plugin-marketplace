---
name: flutter-firebase-deploy:analyze-project
description: Analyze a Flutter project to detect Firebase features, dependencies, and platform support for deployment configuration.
---

# Analyze Flutter Project

Analyze the current Flutter project to understand its deployment requirements.

## Usage

```
/flutter-firebase-deploy:analyze-project [path]
```

## Arguments

- `path` - Optional path to Flutter project (defaults to current directory)

## What This Does

1. Parses `pubspec.yaml` for dependencies
2. Detects Firebase packages and features
3. Checks iOS and Android platform support
4. Identifies existing configuration files
5. Reports missing configurations

## Output

Detailed analysis report with:
- Project info (name, Flutter version)
- Detected Firebase features
- Platform status (iOS/Android)
- Configuration recommendations

## Example

```
/flutter-firebase-deploy:analyze-project ./my-flutter-app
```
