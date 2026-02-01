---
name: flutter-firebase-deploy:install-cli
description: Install or reinstall the flutter-deploy CLI tool from bundled source
---

# Install Flutter Deploy CLI

Install or reinstall the flutter-deploy CLI tool.

## Usage

```
/flutter-firebase-deploy:install-cli [--force]
```

## Arguments

- `--force` - Force reinstall even if already installed

## What This Does

1. Checks if flutter-deploy CLI is already installed
2. Installs from bundled source in `scripts/flutter-deploy-cli/`
3. Verifies installation was successful
4. Reports CLI version

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Installation Method

The CLI is installed using pip in editable mode from the bundled source:

```bash
pip install -e scripts/flutter-deploy-cli/ --user
```

## After Installation

The following commands become available:

- `flutter-deploy` - Main CLI command
- `fd` - Short alias

## Troubleshooting

If installation fails:

1. Check Python version: `python3 --version` (needs 3.10+)
2. Check pip is available: `pip --version`
3. Try manual install: `cd scripts/flutter-deploy-cli && pip install -e .`

## Example

```
/flutter-firebase-deploy:install-cli
```

Output:
```
Checking flutter-deploy CLI...
Installing from bundled source...
flutter-deploy CLI installed: v1.0.0
```
