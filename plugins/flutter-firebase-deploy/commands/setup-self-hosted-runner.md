---
name: flutter-firebase-deploy:setup-self-hosted-runner
description: Configure a self-hosted GitHub Actions runner on Mac Mini for iOS builds requiring hardware access.
---

# Setup Self-Hosted Runner

Configure Mac Mini as a self-hosted GitHub Actions runner.

## Usage

```
/flutter-firebase-deploy:setup-self-hosted-runner [--labels ios,macos]
```

## Options

- `--labels` - Runner labels for workflow targeting

## What This Does

1. Downloads GitHub Actions runner
2. Configures runner with repository
3. Installs as launch daemon
4. Configures Xcode CLI tools
5. Sets up required certificates

## Prerequisites

- Mac Mini with macOS
- Admin access
- GitHub repository admin access
- Runner registration token

## Runner Labels

Use labels to target specific runners:
- `ios` - iOS build capable
- `macos` - macOS runner
- `self-hosted` - Not GitHub-hosted

## Example

```
/flutter-firebase-deploy:setup-self-hosted-runner --labels ios,macos
```
