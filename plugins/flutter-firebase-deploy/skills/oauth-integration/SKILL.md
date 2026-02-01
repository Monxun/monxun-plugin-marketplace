---
name: oauth-integration
description: Configure OAuth authentication providers for Flutter Firebase apps. Set up Google, Apple, and Facebook sign-in. Use when implementing authentication.
trigger_keywords:
  - oauth
  - google sign in
  - apple sign in
  - facebook login
  - firebase auth
  - authentication
---

# OAuth Integration

Configure authentication providers for Flutter Firebase.

## Google Sign-In

### iOS
Add URL scheme to Info.plist:
```xml
<key>CFBundleURLSchemes</key>
<array>
  <string>com.googleusercontent.apps.CLIENT_ID</string>
</array>
```

### Android
Add SHA fingerprints to Firebase Console.

## Apple Sign-In

### iOS
Enable capability in Xcode:
- Sign in with Apple

### Entitlements
```xml
<key>com.apple.developer.applesignin</key>
<array><string>Default</string></array>
```

## Facebook Login

### iOS (Info.plist)
```xml
<key>FacebookAppID</key>
<string>APP_ID</string>
```

### Android (strings.xml)
```xml
<string name="facebook_app_id">APP_ID</string>
```

## Flutter Packages

```yaml
dependencies:
  firebase_auth: ^4.0.0
  google_sign_in: ^6.0.0
  sign_in_with_apple: ^5.0.0
```

## References

See `references/` for provider-specific setup.
