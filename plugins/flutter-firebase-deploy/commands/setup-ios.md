---
name: flutter-firebase-deploy:setup-ios
description: Configure iOS/Xcode settings for Flutter deployment. Sets up capabilities, entitlements, Info.plist, and Podfile configuration.
---

# Setup iOS

Configure Xcode project for Flutter Firebase deployment.

## Usage

```
/flutter-firebase-deploy:setup-ios [--capabilities push,apple-signin]
```

## Options

- `--capabilities` - Comma-separated capabilities to enable

## What This Does

1. Configures bundle identifier
2. Sets deployment target
3. Enables required capabilities
4. Updates Info.plist
5. Configures Podfile
6. Runs pod install

## Capabilities Supported

- `push` - Push Notifications
- `apple-signin` - Sign in with Apple
- `background` - Background Modes
- `associated-domains` - Associated Domains

## Example

```
/flutter-firebase-deploy:setup-ios --capabilities push,apple-signin
```
