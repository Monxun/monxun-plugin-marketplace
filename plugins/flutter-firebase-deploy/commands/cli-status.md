---
name: flutter-firebase-deploy:cli-status
description: Check flutter-deploy CLI installation status and version information
---

# CLI Status

Check the installation status and version of the flutter-deploy CLI tool.

## Usage

```
/flutter-firebase-deploy:cli-status
```

## What This Does

1. Checks if flutter-deploy CLI is installed
2. Reports CLI version if installed
3. Shows Python version and pip status
4. Verifies bundled source availability

## Output Information

| Field | Description |
|-------|-------------|
| CLI Installed | Whether flutter-deploy command is available |
| CLI Version | Version string from flutter-deploy --version |
| Python Version | System Python version |
| Bundled Source | Whether CLI source is bundled with plugin |
| Installation Path | Where CLI is installed |

## Example Output

```
Flutter Deploy CLI Status
========================

CLI Installed: Yes
CLI Version: v1.0.0
Python Version: 3.11.5
Bundled Source: Available at scripts/flutter-deploy-cli/
Installation Path: ~/.local/lib/python3.11/site-packages/flutter_deploy

Commands Available:
  - flutter-deploy
  - fd (alias)
```

## If Not Installed

If the CLI is not installed, the output will include:

```
CLI Installed: No

To install, run:
  /flutter-firebase-deploy:install-cli

Or manually:
  pip install -e scripts/flutter-deploy-cli/
```

## Example

```
/flutter-firebase-deploy:cli-status
```
