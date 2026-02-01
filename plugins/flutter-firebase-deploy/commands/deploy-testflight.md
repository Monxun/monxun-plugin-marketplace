---
name: flutter-firebase-deploy:deploy-testflight
description: Build and deploy iOS app to TestFlight. Handles signing, building, and upload to App Store Connect.
---

# Deploy to TestFlight

Build and upload iOS app to TestFlight for beta testing.

## Usage

```
/flutter-firebase-deploy:deploy-testflight [--skip-tests] [--bump-version]
```

## Options

- `--skip-tests` - Skip running tests before deploy
- `--bump-version` - Auto-increment build number

## What This Does

1. Runs Flutter tests (unless skipped)
2. Syncs certificates via Match
3. Builds iOS app
4. Uploads to TestFlight
5. Reports upload status

## Prerequisites

- Fastlane configured
- Match set up with valid certificates
- App Store Connect API key configured

## Example

```
/flutter-firebase-deploy:deploy-testflight --bump-version
```
