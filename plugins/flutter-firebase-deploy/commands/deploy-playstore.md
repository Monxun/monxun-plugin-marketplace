---
name: flutter-firebase-deploy:deploy-playstore
description: Build and deploy Android app to Play Store. Handles signing, building AAB, and upload to specified track.
---

# Deploy to Play Store

Build and upload Android app to Google Play Store.

## Usage

```
/flutter-firebase-deploy:deploy-playstore [--track internal|alpha|beta|production]
```

## Options

- `--track` - Play Store track (default: internal)

## Tracks

- `internal` - Internal testing (up to 100 testers)
- `alpha` - Closed testing
- `beta` - Open testing
- `production` - Public release

## What This Does

1. Runs Flutter tests
2. Builds release AAB
3. Signs with upload keystore
4. Uploads to specified track
5. Reports upload status

## Prerequisites

- Fastlane configured for Android
- Keystore configured
- Play Store API credentials

## Example

```
/flutter-firebase-deploy:deploy-playstore --track beta
```
