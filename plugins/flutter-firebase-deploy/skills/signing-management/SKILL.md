---
name: signing-management
description: Manage code signing for iOS and Android deployments. Configure certificates, provisioning profiles, Match, and keystores. Use when setting up code signing.
trigger_keywords:
  - code signing
  - certificates
  - provisioning profiles
  - match
  - keystore
  - signing config
---

# Code Signing Management

Manage certificates and signing for app deployment.

## iOS Signing (Match)

```bash
# Initialize
fastlane match init

# Generate/sync certificates
fastlane match development
fastlane match appstore
```

## Android Signing

### Generate Keystore
```bash
keytool -genkey -v -keystore upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias upload
```

### key.properties
```properties
storePassword=password
keyPassword=password
keyAlias=upload
storeFile=upload-keystore.jks
```

## CI/CD Secrets

| Platform | Secrets |
|----------|---------|
| iOS | MATCH_PASSWORD, MATCH_GIT_TOKEN |
| Android | ANDROID_KEYSTORE (base64), KEYSTORE_PASSWORD |

## Best Practices

1. Never commit credentials
2. Use separate dev/prod signing
3. Rotate annually
4. Use Play App Signing

## References

See `references/` for detailed signing guides.
