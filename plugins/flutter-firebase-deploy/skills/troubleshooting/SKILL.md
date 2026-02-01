---
name: troubleshooting
description: Diagnose and resolve Flutter Firebase deployment issues. Fix build errors, signing problems, and deployment failures. Use when encountering errors.
trigger_keywords:
  - troubleshoot
  - fix error
  - build failed
  - signing error
  - deployment failed
  - debug issue
---

# Troubleshooting

Diagnose and fix common Flutter Firebase deployment issues.

## Build Errors

### iOS
```bash
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
flutter clean && flutter pub get
```

### Android
```bash
cd android && ./gradlew clean
flutter clean && flutter pub get
```

## Signing Issues

### iOS - "No signing certificate"
```bash
fastlane match appstore --force
```

### Android - "Keystore not found"
Check `key.properties` path and file existence.

## Firebase Issues

### Auth Failed
- Check SHA fingerprints (Android)
- Verify URL schemes (iOS)

### FCM Token Null
- Enable Push Notifications capability
- Configure APNs key

## Deployment Issues

### TestFlight Stuck
- Check Info.plist for required keys
- Verify App Store Connect API key

### Play Store Rejected
- Review specific rejection reason
- Check policy compliance

## Diagnostic Commands

```bash
flutter doctor -v
flutter analyze
xcodebuild -showsdks
./gradlew dependencies
```

## References

See `references/` for detailed solutions.
