---
name: flutter-firebase-deploy:configure-fastlane
description: Set up Fastlane for automated builds and deployments. Configures Fastfiles, Match, and deployment lanes.
---

# Configure Fastlane

Set up Fastlane automation for iOS and Android.

## Usage

```
/flutter-firebase-deploy:configure-fastlane [--platforms ios,android] [--match-repo URL]
```

## Options

- `--platforms` - Platforms to configure (default: ios,android)
- `--match-repo` - Git repository URL for Match certificates

## What This Does

1. Initializes Fastlane for each platform
2. Creates Fastfile with deployment lanes
3. Configures Match for iOS signing
4. Sets up Appfile with credentials
5. Creates helper lanes

## Generated Files

- `ios/fastlane/Fastfile`
- `ios/fastlane/Matchfile`
- `ios/fastlane/Appfile`
- `android/fastlane/Fastfile`
- `android/fastlane/Appfile`

## Example

```
/flutter-firebase-deploy:configure-fastlane --match-repo git@github.com:org/certs.git
```
