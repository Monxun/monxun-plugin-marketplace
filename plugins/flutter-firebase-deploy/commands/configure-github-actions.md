---
name: flutter-firebase-deploy:configure-github-actions
description: Set up GitHub Actions workflows for CI/CD. Creates workflows for testing, building, and deploying to stores.
---

# Configure GitHub Actions

Set up CI/CD pipelines with GitHub Actions.

## Usage

```
/flutter-firebase-deploy:configure-github-actions [--triggers push,pr] [--platforms ios,android]
```

## Options

- `--triggers` - Workflow triggers (default: push)
- `--platforms` - Platforms to deploy (default: ios,android)

## What This Does

1. Creates workflow files
2. Documents required secrets
3. Configures build steps
4. Sets up deployment steps
5. Provides secret setup guidance

## Generated Workflows

- `.github/workflows/test.yml` - Run tests on PR
- `.github/workflows/ios-deploy.yml` - iOS deployment
- `.github/workflows/android-deploy.yml` - Android deployment

## Example

```
/flutter-firebase-deploy:configure-github-actions --triggers push,pr
```
