---
name: flutter-firebase-deploy:setup-android
description: Configure Android/Gradle settings for Flutter deployment. Sets up signing configs, build.gradle, and ProGuard rules.
---

# Setup Android

Configure Gradle project for Flutter Firebase deployment.

## Usage

```
/flutter-firebase-deploy:setup-android [--create-keystore]
```

## Options

- `--create-keystore` - Generate a new upload keystore

## What This Does

1. Configures build.gradle files
2. Sets up signing configuration
3. Configures ProGuard rules
4. Verifies google-services.json
5. Sets appropriate SDK versions

## Output

- Updated `android/app/build.gradle`
- Created `android/key.properties` (if signing configured)
- Updated ProGuard rules

## Example

```
/flutter-firebase-deploy:setup-android --create-keystore
```
