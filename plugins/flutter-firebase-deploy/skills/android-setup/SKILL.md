---
name: android-setup
description: Configure Android/Gradle settings for Flutter Firebase deployment. Set up signing configs, ProGuard rules, and build variants. Use when configuring Android platform.
trigger_keywords:
  - android setup
  - gradle config
  - android signing
  - proguard
  - build.gradle
---

# Android Setup

Configure Gradle project for Flutter Firebase deployment.

## Key Files

| File | Purpose |
|------|---------|
| `android/build.gradle` | Project-level config |
| `android/app/build.gradle` | App-level config |
| `android/app/google-services.json` | Firebase config |
| `android/key.properties` | Signing credentials |

## Signing Configuration

### key.properties
```properties
storePassword=yourpassword
keyPassword=yourpassword
keyAlias=upload
storeFile=upload-keystore.jks
```

### build.gradle
```groovy
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

## Build Commands

```bash
flutter build apk --release
flutter build appbundle --release
```

## References

See `references/` for detailed Gradle configuration.
