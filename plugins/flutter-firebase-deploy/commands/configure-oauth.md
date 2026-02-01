---
name: flutter-firebase-deploy:configure-oauth
description: Configure OAuth authentication providers. Sets up Google, Apple, and Facebook sign-in for Firebase Auth.
---

# Configure OAuth

Set up authentication providers for Firebase Auth.

## Usage

```
/flutter-firebase-deploy:configure-oauth [--providers google,apple,facebook]
```

## Options

- `--providers` - Comma-separated list of providers to configure

## Supported Providers

- `google` - Google Sign-In
- `apple` - Sign in with Apple
- `facebook` - Facebook Login
- `email` - Email/Password

## What This Does

1. Enables providers in Firebase Console guidance
2. Configures iOS Info.plist
3. Configures Android manifests
4. Adds required packages
5. Provides implementation guidance

## Example

```
/flutter-firebase-deploy:configure-oauth --providers google,apple
```
