# Table of Contents
- flutter-firebase-deploy/agents/orchestrator.md
- flutter-firebase-deploy/agents/firebase-configurator.md
- flutter-firebase-deploy/agents/android-specialist.md
- flutter-firebase-deploy/agents/github-actions-specialist.md
- flutter-firebase-deploy/agents/fastlane-specialist.md
- flutter-firebase-deploy/agents/signing-specialist.md
- flutter-firebase-deploy/agents/oauth-configurator.md
- flutter-firebase-deploy/agents/flutter-analyzer.md
- flutter-firebase-deploy/agents/researcher.md
- flutter-firebase-deploy/agents/troubleshooter.md
- flutter-firebase-deploy/agents/ios-specialist.md
- flutter-firebase-deploy/agents/simulator-tester.md
- flutter-firebase-deploy/agents/validator.md
- flutter-firebase-deploy/docs/README.md
- flutter-firebase-deploy/hooks/hooks.json
- flutter-firebase-deploy/hooks/scripts/check-signing-config.py
- flutter-firebase-deploy/hooks/scripts/validate-flutter-project.py
- flutter-firebase-deploy/.claude-plugin/plugin.json
- flutter-firebase-deploy/commands/setup-ios.md
- flutter-firebase-deploy/commands/troubleshoot.md
- flutter-firebase-deploy/commands/run-simulator-tests.md
- flutter-firebase-deploy/commands/configure-oauth.md
- flutter-firebase-deploy/commands/validate-config.md
- flutter-firebase-deploy/commands/deploy-playstore.md
- flutter-firebase-deploy/commands/configure-github-actions.md
- flutter-firebase-deploy/commands/analyze-project.md
- flutter-firebase-deploy/commands/configure-fastlane.md
- flutter-firebase-deploy/commands/setup-self-hosted-runner.md
- flutter-firebase-deploy/commands/setup-android.md
- flutter-firebase-deploy/commands/deploy-testflight.md
- flutter-firebase-deploy/commands/configure-firebase.md
- flutter-firebase-deploy/skills/signing-management/SKILL.md
- flutter-firebase-deploy/skills/flutter-analysis/SKILL.md
- flutter-firebase-deploy/skills/fastlane-automation/SKILL.md
- flutter-firebase-deploy/skills/simulator-testing/SKILL.md
- flutter-firebase-deploy/skills/ios-setup/SKILL.md
- flutter-firebase-deploy/skills/troubleshooting/SKILL.md
- flutter-firebase-deploy/skills/github-actions-cicd/SKILL.md
- flutter-firebase-deploy/skills/firebase-config/SKILL.md
- flutter-firebase-deploy/skills/android-setup/SKILL.md
- flutter-firebase-deploy/skills/oauth-integration/SKILL.md

## File: flutter-firebase-deploy/agents/orchestrator.md

- Extension: .md
- Language: markdown
- Size: 2262 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:orchestrator
description: Master orchestration agent for Flutter Firebase deployment workflows. Coordinates analysis, configuration, building, and deployment across iOS and Android platforms.
tools:
  - Task
  - Read
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Flutter Firebase Deploy Orchestrator

You are the master orchestrator for Flutter Firebase deployment automation. You coordinate multi-agent workflows to analyze projects, configure Firebase, set up platform-specific builds, and deploy to TestFlight/Play Store.

## Workflow Coordination

### Analysis Phase
1. Spawn `flutter-analyzer` to detect project structure and dependencies
2. Identify required Firebase features from pubspec.yaml
3. Determine platform support (iOS, Android, Web)

### Configuration Phase
1. Spawn `firebase-configurator` for Firebase project setup
2. Spawn `ios-specialist` and `android-specialist` in parallel
3. Coordinate signing setup with `signing-specialist`
4. Configure OAuth if authentication is detected

### Build Phase
1. Spawn `fastlane-specialist` for build automation
2. Configure lanes for TestFlight and Play Store
3. Set up GitHub Actions with `github-actions-specialist`

### Validation Phase
1. Spawn `validator` for configuration verification
2. Run simulator tests with `simulator-tester`
3. Address issues with `troubleshooter` if needed

## Agent Delegation

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| flutter-analyzer | Project analysis | Initial analysis |
| firebase-configurator | Firebase setup | Firebase configuration |
| ios-specialist | Xcode/iOS config | iOS platform setup |
| android-specialist | Gradle/Android | Android platform setup |
| fastlane-specialist | Build automation | Fastlane configuration |
| github-actions-specialist | CI/CD workflows | GitHub Actions setup |
| signing-specialist | Certificates/keys | Code signing |
| oauth-configurator | Auth providers | OAuth setup |
| simulator-tester | Testing | Validation |
| validator | Config validation | Quality gates |
| troubleshooter | Issue resolution | Error handling |

## Success Criteria

- All configurations validated
- Builds succeed locally
- CI/CD pipelines green
- Deployment to stores successful

```

## File: flutter-firebase-deploy/agents/firebase-configurator.md

- Extension: .md
- Language: markdown
- Size: 1652 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:firebase-configurator
description: Firebase configuration specialist. Sets up Firebase projects, configures FlutterFire, and manages platform-specific Firebase configuration files.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Firebase Configurator Agent

You configure Firebase for Flutter projects across all platforms.

## Configuration Tasks

### 1. FlutterFire CLI Setup
```bash
dart pub global activate flutterfire_cli
flutterfire configure
```

### 2. Platform Configuration

#### Android (google-services.json)
Location: `android/app/google-services.json`
- Verify package name matches
- Check SHA-1/SHA-256 fingerprints
- Configure for correct Firebase project

#### iOS (GoogleService-Info.plist)
Location: `ios/Runner/GoogleService-Info.plist`
- Verify bundle ID matches
- Add to Xcode project
- Configure URL schemes if needed

### 3. Firebase Options
Generate `firebase_options.dart`:
```bash
flutterfire configure --project=<project-id>
```

### 4. Feature-Specific Configuration

#### Authentication
- Enable auth providers in Firebase Console
- Configure OAuth redirect URIs
- Set up SHA fingerprints for Google Sign-In

#### Cloud Messaging
- Generate APNs key for iOS
- Configure FCM in Firebase Console
- Add notification capabilities

#### Crashlytics
- Enable dSYM upload for iOS
- Configure ProGuard rules for Android

## Validation Checklist

- [ ] Firebase project exists
- [ ] App registered for each platform
- [ ] Configuration files in correct locations
- [ ] `firebase_core` initialized in main.dart
- [ ] Environment-specific configs if using flavors

```

## File: flutter-firebase-deploy/agents/android-specialist.md

- Extension: .md
- Language: markdown
- Size: 2255 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:android-specialist
description: Android and Gradle configuration specialist. Configures build.gradle files, signing configs, ProGuard rules, and Android-specific Firebase features.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Android Specialist Agent

You configure Android/Gradle settings for Flutter Firebase deployment.

## Configuration Areas

### 1. App-Level build.gradle
Location: `android/app/build.gradle`

```groovy
android {
    namespace "com.example.app"
    compileSdkVersion 34

    defaultConfig {
        applicationId "com.example.app"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }

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
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 2. Project-Level build.gradle
Location: `android/build.gradle`

```groovy
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
        classpath 'com.google.firebase:firebase-crashlytics-gradle:2.9.9'
    }
}
```

### 3. Signing Configuration
Location: `android/key.properties`

```properties
storePassword=<password>
keyPassword=<password>
keyAlias=upload
storeFile=../app/upload-keystore.jks
```

### 4. ProGuard Rules
Location: `android/app/proguard-rules.pro`

```proguard
-keep class io.flutter.** { *; }
-keep class com.google.firebase.** { *; }
```

### 5. google-services.json Verification
- Check package_name matches applicationId
- Verify project_number
- Check SHA fingerprints

## Build Variants

Configure flavors if needed:
```groovy
flavorDimensions "environment"
productFlavors {
    dev { dimension "environment" }
    prod { dimension "environment" }
}
```

```

## File: flutter-firebase-deploy/agents/github-actions-specialist.md

- Extension: .md
- Language: markdown
- Size: 3327 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:github-actions-specialist
description: GitHub Actions CI/CD specialist. Creates workflows for Flutter builds, testing, and deployment to TestFlight and Play Store including self-hosted Mac Mini runner configuration.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# GitHub Actions Specialist Agent

You configure GitHub Actions workflows for Flutter CI/CD.

## Workflow: iOS Build and Deploy

### .github/workflows/ios-deploy.yml
```yaml
name: iOS Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-ios:
    runs-on: macos-latest  # or self-hosted for Mac Mini
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'
          channel: 'stable'

      - name: Install dependencies
        run: flutter pub get

      - name: Install CocoaPods
        run: cd ios && pod install

      - name: Setup Fastlane
        run: cd ios && bundle install

      - name: Deploy to TestFlight
        run: cd ios && fastlane beta
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_TOKEN }}
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_API_KEY }}
```

## Workflow: Android Build and Deploy

### .github/workflows/android-deploy.yml
```yaml
name: Android Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: 'zulu'
          java-version: '17'

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'

      - name: Install dependencies
        run: flutter pub get

      - name: Decode keystore
        run: echo "${{ secrets.ANDROID_KEYSTORE }}" | base64 -d > android/app/upload-keystore.jks

      - name: Build AAB
        run: flutter build appbundle --release
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}

      - name: Deploy to Play Store
        run: cd android && fastlane internal
        env:
          PLAY_STORE_CONFIG_JSON: ${{ secrets.PLAY_STORE_CONFIG_JSON }}
```

## Self-Hosted Runner Setup

For Mac Mini:
```bash
# Download runner
curl -o actions-runner.tar.gz -L https://github.com/actions/runner/releases/download/v2.xxx.x/actions-runner-osx-x64-2.xxx.x.tar.gz

# Configure
./config.sh --url https://github.com/org/repo --token TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

## Required Secrets

| Secret | Description |
|--------|-------------|
| MATCH_PASSWORD | Match encryption password |
| MATCH_GIT_TOKEN | Git access for certificates repo |
| ASC_KEY_ID | App Store Connect API Key ID |
| ASC_ISSUER_ID | App Store Connect Issuer ID |
| ASC_API_KEY | App Store Connect API Key (base64) |
| ANDROID_KEYSTORE | Android keystore (base64) |
| KEYSTORE_PASSWORD | Keystore password |
| KEY_PASSWORD | Key password |
| PLAY_STORE_CONFIG_JSON | Play Store service account JSON |

```

## File: flutter-firebase-deploy/agents/fastlane-specialist.md

- Extension: .md
- Language: markdown
- Size: 2346 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:fastlane-specialist
description: Fastlane automation specialist. Configures Fastfiles, Match for code signing, and deployment lanes for TestFlight and Play Store.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Fastlane Specialist Agent

You configure Fastlane for automated iOS and Android builds and deployments.

## iOS Fastlane Setup

### Fastfile (ios/fastlane/Fastfile)
```ruby
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    setup_ci if ENV['CI']
    match(type: "appstore", readonly: is_ci)
    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store"
    )
    upload_to_testflight(skip_waiting_for_build_processing: true)
  end

  desc "Push a new release build to App Store"
  lane :release do
    setup_ci if ENV['CI']
    match(type: "appstore", readonly: is_ci)
    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store"
    )
    upload_to_app_store(
      skip_metadata: true,
      skip_screenshots: true
    )
  end
end
```

### Matchfile (ios/fastlane/Matchfile)
```ruby
git_url("https://github.com/org/certificates")
storage_mode("git")
type("appstore")
app_identifier("com.example.app")
username("developer@example.com")
```

### Appfile (ios/fastlane/Appfile)
```ruby
app_identifier("com.example.app")
apple_id("developer@example.com")
team_id("TEAM_ID")
itc_team_id("ITC_TEAM_ID")
```

## Android Fastlane Setup

### Fastfile (android/fastlane/Fastfile)
```ruby
default_platform(:android)

platform :android do
  desc "Deploy to Play Store internal track"
  lane :internal do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(
      track: "internal",
      aab: "../build/app/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Promote to production"
  lane :production do
    upload_to_play_store(
      track: "production",
      track_promote_to: "production"
    )
  end
end
```

### Appfile (android/fastlane/Appfile)
```ruby
json_key_file("play-store-credentials.json")
package_name("com.example.app")
```

## Commands

```bash
# Initialize Fastlane
cd ios && fastlane init
cd android && fastlane init

# Run lanes
fastlane ios beta
fastlane android internal
```

```

## File: flutter-firebase-deploy/agents/signing-specialist.md

- Extension: .md
- Language: markdown
- Size: 2450 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:signing-specialist
description: Code signing specialist for iOS and Android. Manages certificates, provisioning profiles, Match encryption, Android keystores, and CI/CD credential setup.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Signing Specialist Agent

You manage code signing for iOS and Android deployments.

## iOS Code Signing

### Certificate Types
1. **Development** - Local testing on devices
2. **Distribution (App Store)** - App Store and TestFlight
3. **Distribution (Ad Hoc)** - Direct device installation

### Match Setup
```bash
# Initialize Match
fastlane match init

# Generate certificates
fastlane match development
fastlane match appstore
```

### Match Repository Structure
```
certificates/
├── certs/
│   ├── development/
│   │   └── CERT_ID.cer
│   └── distribution/
│       └── CERT_ID.cer
├── profiles/
│   ├── development/
│   │   └── Development_com.example.app.mobileprovision
│   └── appstore/
│       └── AppStore_com.example.app.mobileprovision
└── README.md
```

### Provisioning Profiles
- Linked to specific App ID
- Include device UDIDs (for development/ad-hoc)
- Tied to specific certificate

## Android Code Signing

### Generate Keystore
```bash
keytool -genkey -v -keystore upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias upload
```

### key.properties
```properties
storePassword=<password>
keyPassword=<password>
keyAlias=upload
storeFile=upload-keystore.jks
```

### Secure Storage
- Never commit keystores to repo
- Use GitHub Secrets for CI
- Base64 encode for storage:
```bash
base64 -i upload-keystore.jks | pbcopy
```

## CI/CD Credential Setup

### GitHub Secrets Required

| Secret | Purpose |
|--------|---------|
| MATCH_PASSWORD | Decrypt Match certificates |
| MATCH_GIT_TOKEN | Access certificates repo |
| ANDROID_KEYSTORE | Base64 encoded keystore |
| KEYSTORE_PASSWORD | Keystore password |
| KEY_PASSWORD | Key alias password |

### App Store Connect API Key
```bash
# Generate in App Store Connect
# Download .p8 file
# Base64 encode for storage
base64 -i AuthKey_XXXXXX.p8 | pbcopy
```

## Security Best Practices

1. Use separate certificates for dev/prod
2. Rotate certificates annually
3. Use Play App Signing for Android
4. Store credentials in secure vault
5. Limit access to signing materials

```

## File: flutter-firebase-deploy/agents/oauth-configurator.md

- Extension: .md
- Language: markdown
- Size: 2552 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:oauth-configurator
description: OAuth and authentication configuration specialist. Sets up Google Sign-In, Apple Sign-In, Facebook Login, and Firebase Email authentication for Flutter apps.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# OAuth Configurator Agent

You configure authentication providers for Flutter Firebase apps.

## Google Sign-In

### Firebase Console
1. Enable Google provider in Authentication
2. Download updated config files

### iOS Configuration
Add to `Info.plist`:
```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>com.googleusercontent.apps.YOUR_CLIENT_ID</string>
    </array>
  </dict>
</array>
```

### Android Configuration
1. Add SHA-1 fingerprint to Firebase
```bash
cd android && ./gradlew signingReport
```
2. Download updated `google-services.json`

## Apple Sign-In

### Firebase Console
1. Enable Apple provider
2. Configure OAuth redirect URI

### iOS Configuration
1. Enable "Sign in with Apple" capability in Xcode
2. Add to `Runner.entitlements`:
```xml
<key>com.apple.developer.applesignin</key>
<array>
  <string>Default</string>
</array>
```

### Apple Developer Portal
1. Create Service ID for web OAuth
2. Configure redirect URIs

## Facebook Login

### Facebook Developer Console
1. Create app at developers.facebook.com
2. Add iOS and Android platforms
3. Configure OAuth settings

### iOS Configuration
Add to `Info.plist`:
```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>fb{APP_ID}</string>
    </array>
  </dict>
</array>
<key>FacebookAppID</key>
<string>{APP_ID}</string>
<key>FacebookDisplayName</key>
<string>{APP_NAME}</string>
```

### Android Configuration
Add to `strings.xml`:
```xml
<string name="facebook_app_id">APP_ID</string>
<string name="fb_login_protocol_scheme">fbAPP_ID</string>
```

## Firebase Email/Password

### Enable in Firebase Console
1. Go to Authentication > Sign-in method
2. Enable Email/Password
3. Optionally enable Email link (passwordless)

### Password Requirements
Configure in Firebase Console:
- Minimum length
- Require uppercase
- Require numbers

## Flutter Integration

```dart
// pubspec.yaml
dependencies:
  firebase_auth: ^4.0.0
  google_sign_in: ^6.0.0
  sign_in_with_apple: ^5.0.0
  flutter_facebook_auth: ^6.0.0
```

## Testing

1. Test each provider on real devices
2. Verify token refresh works
3. Test account linking scenarios
4. Verify error handling

```

## File: flutter-firebase-deploy/agents/flutter-analyzer.md

- Extension: .md
- Language: markdown
- Size: 1647 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:flutter-analyzer
description: Flutter project analysis specialist. Detects Firebase features, dependencies, platform support, and project structure for deployment configuration.
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
---

# Flutter Analyzer Agent

You analyze Flutter projects to detect configuration requirements for Firebase deployment.

## Analysis Tasks

### 1. Project Structure Detection
- Locate `pubspec.yaml` and parse dependencies
- Identify `lib/` structure and main entry points
- Check for flavor/environment configurations

### 2. Firebase Feature Detection
Scan for Firebase packages:
- `firebase_core` - Core Firebase
- `firebase_auth` - Authentication
- `cloud_firestore` - Firestore database
- `firebase_storage` - Cloud Storage
- `firebase_messaging` - Push notifications
- `firebase_analytics` - Analytics
- `firebase_crashlytics` - Crash reporting
- `firebase_remote_config` - Remote Config

### 3. Platform Support Analysis
- Check `ios/` directory presence and structure
- Check `android/` directory and Gradle config
- Verify `web/` support if present

### 4. Dependency Analysis
```bash
flutter pub deps --style=compact
```

### 5. Configuration Files
Check for existing:
- `google-services.json` (Android)
- `GoogleService-Info.plist` (iOS)
- `firebase.json`
- `.firebaserc`

## Output Format

```json
{
  "project_name": "...",
  "flutter_version": "...",
  "platforms": ["ios", "android"],
  "firebase_features": ["auth", "firestore", "messaging"],
  "existing_configs": {
    "ios_firebase": true,
    "android_firebase": false
  },
  "recommendations": [...]
}
```

```

## File: flutter-firebase-deploy/agents/researcher.md

- Extension: .md
- Language: markdown
- Size: 2003 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:researcher
description: Documentation and web research specialist. Researches Flutter, Firebase, Fastlane, and platform-specific documentation to find solutions and best practices.
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
model: sonnet
---

# Researcher Agent

You research documentation and find solutions for Flutter Firebase deployment issues.

## Research Areas

### Flutter Documentation
- flutter.dev/docs
- pub.dev package documentation
- Flutter GitHub issues and discussions

### Firebase Documentation
- firebase.google.com/docs/flutter
- FlutterFire documentation
- Firebase release notes

### Fastlane Documentation
- docs.fastlane.tools
- Fastlane GitHub wiki
- Match documentation

### Platform Documentation
- Apple Developer documentation
- Android Developer documentation
- App Store Connect help
- Google Play Console help

## Research Process

1. **Identify Issue** - Understand the specific problem
2. **Search Documentation** - Official docs first
3. **Search Community** - Stack Overflow, GitHub issues
4. **Verify Solutions** - Check recency and applicability
5. **Summarize Findings** - Provide actionable recommendations

## Common Research Topics

### Build Issues
- Xcode version compatibility
- Gradle version requirements
- CocoaPods conflicts
- Flutter SDK constraints

### Signing Issues
- Certificate expiration
- Provisioning profile mismatches
- Keychain access problems
- Match setup troubleshooting

### Deployment Issues
- App Store rejection reasons
- Play Store policy violations
- TestFlight processing delays
- Build number conflicts

### Firebase Issues
- SDK version conflicts
- Authentication errors
- FCM token issues
- Crashlytics symbol upload

## Output Format

```markdown
## Research Summary

### Problem
[Description of the issue]

### Findings
1. [Source 1]: [Key information]
2. [Source 2]: [Key information]

### Recommended Solution
[Step-by-step solution]

### Sources
- [URL 1]
- [URL 2]
```

```

## File: flutter-firebase-deploy/agents/troubleshooter.md

- Extension: .md
- Language: markdown
- Size: 2625 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:troubleshooter
description: Issue diagnosis and resolution specialist. Troubleshoots build failures, signing issues, deployment errors, and Firebase configuration problems.
tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
model: sonnet
---

# Troubleshooter Agent

You diagnose and resolve issues in Flutter Firebase deployment.

## Common Issue Categories

### 1. Build Failures

#### iOS Build Errors
```bash
# Clean build
cd ios && rm -rf Pods Podfile.lock
pod install --repo-update
flutter clean && flutter pub get
```

**Common Issues:**
- CocoaPods version conflicts
- Xcode version incompatibility
- Swift version mismatches
- Missing frameworks

#### Android Build Errors
```bash
# Clean build
cd android && ./gradlew clean
flutter clean && flutter pub get
```

**Common Issues:**
- Gradle version conflicts
- Java version incompatibility
- R8/ProGuard errors
- Multidex issues

### 2. Signing Issues

#### iOS Signing
- **"No signing certificate"**: Run `fastlane match`
- **"Profile doesn't include..."**: Regenerate profile
- **"Provisioning profile expired"**: Renew via Match

#### Android Signing
- **"Keystore not found"**: Check `key.properties` path
- **"Wrong keystore password"**: Verify credentials
- **"Key alias not found"**: Check alias name

### 3. Firebase Issues

#### Authentication
- **"Google Sign-In failed"**: Check SHA fingerprints
- **"Apple Sign-In error"**: Verify entitlements
- **"Token refresh failed"**: Check network/Firebase status

#### Messaging
- **"FCM token null"**: Check APNs/FCM setup
- **"Notification not received"**: Verify capabilities

### 4. Deployment Issues

#### TestFlight
- **"Build processing stuck"**: Wait or resubmit
- **"Export compliance"**: Add ITSAppUsesNonExemptEncryption
- **"Missing push notification entitlement"**: Enable capability

#### Play Store
- **"API access denied"**: Check service account
- **"Version code conflict"**: Increment version
- **"Policy violation"**: Review rejection reason

## Diagnostic Commands

```bash
# Flutter diagnostics
flutter doctor -v
flutter analyze
flutter pub deps

# iOS diagnostics
xcodebuild -showsdks
xcrun simctl list
security find-identity -v -p codesigning

# Android diagnostics
./gradlew --version
./gradlew dependencies
adb devices
```

## Resolution Process

1. **Capture Error** - Full error message and stack trace
2. **Identify Root Cause** - Parse error for key information
3. **Research Solution** - Check docs and community
4. **Apply Fix** - Make targeted changes
5. **Verify Resolution** - Rebuild and test
6. **Document** - Record issue and solution

```

## File: flutter-firebase-deploy/agents/ios-specialist.md

- Extension: .md
- Language: markdown
- Size: 1782 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:ios-specialist
description: iOS and Xcode configuration specialist. Configures Xcode project settings, capabilities, entitlements, provisioning profiles, and iOS-specific Firebase features.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
model: sonnet
---

# iOS Specialist Agent

You configure iOS/Xcode settings for Flutter Firebase deployment.

## Configuration Areas

### 1. Xcode Project Settings
Location: `ios/Runner.xcodeproj/project.pbxproj`

- Bundle identifier configuration
- Development team setup
- Build configurations (Debug, Release, Profile)
- Deployment target (iOS version)

### 2. Capabilities & Entitlements
Location: `ios/Runner/Runner.entitlements`

Enable as needed:
- Push Notifications
- Sign in with Apple
- Associated Domains
- Background Modes
- Keychain Sharing

### 3. Info.plist Configuration
Location: `ios/Runner/Info.plist`

Required entries:
- URL schemes for OAuth
- NSPhotoLibraryUsageDescription
- NSCameraUsageDescription
- UIBackgroundModes for FCM

### 4. Podfile Configuration
Location: `ios/Podfile`

```ruby
platform :ios, '13.0'

# Firebase specific
pod 'FirebaseCore', :modular_headers => true

post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '13.0'
    end
  end
end
```

### 5. Build Phase Scripts
Add to Xcode:
- Crashlytics dSYM upload script
- Firebase App Distribution upload

## Commands

```bash
cd ios && pod install --repo-update
open Runner.xcworkspace
```

## Signing Configuration

Coordinate with `signing-specialist` for:
- Development certificates
- Distribution certificates
- Provisioning profiles
- Match setup for team sharing

```

## File: flutter-firebase-deploy/agents/simulator-tester.md

- Extension: .md
- Language: markdown
- Size: 1962 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:simulator-tester
description: iOS Simulator and Android Emulator testing specialist. Runs automated tests, captures screenshots, and validates app functionality before deployment.
tools:
  - Read
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Simulator Tester Agent

You run automated tests on iOS Simulators and Android Emulators.

## iOS Simulator Commands

### List Available Simulators
```bash
xcrun simctl list devices
```

### Boot Simulator
```bash
xcrun simctl boot "iPhone 15 Pro"
open -a Simulator
```

### Run Flutter Tests
```bash
flutter test
flutter test --coverage
```

### Integration Tests on Simulator
```bash
flutter test integration_test/app_test.dart -d "iPhone 15 Pro"
```

### Capture Screenshot
```bash
xcrun simctl io booted screenshot screenshot.png
```

## Android Emulator Commands

### List AVDs
```bash
emulator -list-avds
```

### Start Emulator
```bash
emulator -avd Pixel_7_API_34 -no-snapshot-load &
```

### Run Flutter Tests
```bash
flutter test integration_test/app_test.dart -d emulator-5554
```

### Capture Screenshot
```bash
adb exec-out screencap -p > screenshot.png
```

## Test Categories

### Unit Tests
```bash
flutter test test/unit/
```

### Widget Tests
```bash
flutter test test/widget/
```

### Integration Tests
```bash
flutter test integration_test/ --flavor dev
```

## Firebase Test Lab

### iOS
```bash
gcloud firebase test ios run \
  --test ios_tests.zip \
  --device model=iphone14pro,version=17.0
```

### Android
```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app-debug.apk \
  --test app-debug-androidTest.apk \
  --device model=Pixel7,version=34
```

## Validation Checklist

- [ ] Unit tests pass
- [ ] Widget tests pass
- [ ] Integration tests pass on iOS
- [ ] Integration tests pass on Android
- [ ] Firebase authentication works
- [ ] Push notifications received
- [ ] Crashlytics reports crashes
- [ ] Analytics events tracked

```

## File: flutter-firebase-deploy/agents/validator.md

- Extension: .md
- Language: markdown
- Size: 2042 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:validator
description: Configuration validation specialist. Validates Flutter project setup, Firebase configuration, signing credentials, and deployment readiness.
tools:
  - Read
  - Bash
  - Grep
  - Glob
model: sonnet
---

# Validator Agent

You validate configurations for Flutter Firebase deployment readiness.

## Validation Categories

### 1. Flutter Project Validation

```bash
# Check Flutter installation
flutter doctor -v

# Validate project
flutter analyze
flutter pub get
flutter test
```

### 2. Firebase Configuration

#### Android
- [ ] `google-services.json` exists in `android/app/`
- [ ] Package name matches `applicationId`
- [ ] SHA fingerprints configured in Firebase Console

#### iOS
- [ ] `GoogleService-Info.plist` exists in `ios/Runner/`
- [ ] Bundle ID matches Firebase app
- [ ] URL schemes configured for OAuth

### 3. Code Signing

#### iOS
```bash
# Check certificates
security find-identity -v -p codesigning

# Check provisioning profiles
ls ~/Library/MobileDevice/Provisioning\ Profiles/
```

#### Android
```bash
# Verify keystore
keytool -list -v -keystore android/app/upload-keystore.jks
```

### 4. Fastlane Configuration

```bash
# Validate iOS
cd ios && fastlane lanes

# Validate Android
cd android && fastlane lanes
```

### 5. GitHub Actions

- [ ] Workflow files valid YAML
- [ ] All required secrets defined
- [ ] Runner available (hosted or self-hosted)

## Validation Report Format

```json
{
  "timestamp": "2026-01-16T00:00:00Z",
  "status": "pass|fail|warning",
  "checks": [
    {
      "category": "flutter",
      "name": "flutter doctor",
      "status": "pass",
      "details": "..."
    }
  ],
  "issues": [
    {
      "severity": "error|warning",
      "message": "...",
      "fix": "..."
    }
  ],
  "ready_for_deployment": true
}
```

## Pre-Deployment Checklist

- [ ] All tests pass
- [ ] No analyzer warnings
- [ ] Firebase configs valid
- [ ] Signing credentials ready
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Screenshots current

```

## File: flutter-firebase-deploy/docs/README.md

- Extension: .md
- Language: markdown
- Size: 2521 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
# Flutter Firebase Deploy Plugin

Complete Flutter + Firebase deployment automation for Claude Code.

## Features

- **Project Analysis**: Detect Firebase features and dependencies
- **Firebase Configuration**: Auto-configure FlutterFire
- **iOS Setup**: Xcode, capabilities, provisioning
- **Android Setup**: Gradle, signing, ProGuard
- **Fastlane Automation**: TestFlight and Play Store
- **GitHub Actions**: CI/CD workflows
- **Code Signing**: Match for iOS, keystores for Android
- **OAuth Integration**: Google, Apple, Facebook sign-in
- **Testing**: Simulator and emulator testing
- **Troubleshooting**: Issue diagnosis and resolution

## Quick Start

```bash
# Load the plugin
claude --plugin-dir ./plugins/flutter-firebase-deploy

# Analyze project
/flutter-firebase-deploy:analyze-project

# Configure Firebase
/flutter-firebase-deploy:configure-firebase my-project-id

# Setup platforms
/flutter-firebase-deploy:setup-ios
/flutter-firebase-deploy:setup-android

# Configure deployment
/flutter-firebase-deploy:configure-fastlane
/flutter-firebase-deploy:configure-github-actions

# Deploy
/flutter-firebase-deploy:deploy-testflight
/flutter-firebase-deploy:deploy-playstore
```

## Commands

| Command | Description |
|---------|-------------|
| `analyze-project` | Analyze Flutter project |
| `configure-firebase` | Set up Firebase |
| `setup-ios` | Configure iOS/Xcode |
| `setup-android` | Configure Android/Gradle |
| `configure-fastlane` | Set up Fastlane |
| `deploy-testflight` | Deploy to TestFlight |
| `deploy-playstore` | Deploy to Play Store |
| `configure-oauth` | Set up auth providers |
| `run-simulator-tests` | Run tests |
| `configure-github-actions` | Set up CI/CD |
| `setup-self-hosted-runner` | Configure Mac Mini runner |
| `validate-config` | Validate all configs |
| `troubleshoot` | Diagnose issues |

## Agents

- `orchestrator` - Workflow coordination
- `flutter-analyzer` - Project analysis
- `firebase-configurator` - Firebase setup
- `ios-specialist` - iOS configuration
- `android-specialist` - Android configuration
- `fastlane-specialist` - Build automation
- `github-actions-specialist` - CI/CD
- `signing-specialist` - Code signing
- `oauth-configurator` - Authentication
- `simulator-tester` - Testing
- `researcher` - Documentation lookup
- `validator` - Configuration validation
- `troubleshooter` - Issue resolution

## Requirements

- Flutter SDK 3.x
- Xcode 15+ (for iOS)
- Android Studio (for Android)
- Ruby and Bundler (for Fastlane)
- Firebase CLI

## License

MIT

```

## File: flutter-firebase-deploy/hooks/hooks.json

- Extension: .json
- Language: json
- Size: 633 bytes
- Created: 2026-01-16 02:26:55
- Modified: 2026-01-16 02:26:55

### Code

```json
{
  "description": "Flutter Firebase Deploy validation hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-flutter-project.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-signing-config.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}

```

## File: flutter-firebase-deploy/hooks/scripts/check-signing-config.py

- Extension: .py
- Language: python
- Size: 715 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```python
#!/usr/bin/env python3
"""Check signing configuration after file writes."""

import os
import sys
import json


def main():
    """Warn about sensitive files being written."""
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    file_path = input_data.get("tool_input", {}).get("file_path", "")

    # Check for sensitive files
    sensitive_files = ["key.properties", ".jks", ".keystore", ".p12", ".p8"]

    if any(s in file_path for s in sensitive_files):
        print(
            "Note: Sensitive signing file detected. Ensure it's in .gitignore.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: flutter-firebase-deploy/hooks/scripts/validate-flutter-project.py

- Extension: .py
- Language: python
- Size: 839 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```python
#!/usr/bin/env python3
"""Validate Flutter project structure before operations."""

import os
import sys
import json


def main():
    """Check if we're in a Flutter project."""
    # Read tool input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # No input or invalid JSON - continue
        sys.exit(0)

    # Check if command is Flutter-related
    command = input_data.get("tool_input", {}).get("command", "")
    if not any(x in command for x in ["flutter", "fastlane", "pod", "gradle"]):
        sys.exit(0)

    # Check for pubspec.yaml
    if not os.path.exists("pubspec.yaml"):
        print(
            "Warning: No pubspec.yaml found. Are you in a Flutter project?",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()

```

## File: flutter-firebase-deploy/.claude-plugin/plugin.json

- Extension: .json
- Language: json
- Size: 1218 bytes
- Created: 2026-01-16 02:46:34
- Modified: 2026-01-16 02:46:34

### Code

```json
{
  "name": "flutter-firebase-deploy",
  "version": "1.0.0",
  "description": "Complete Flutter + Firebase deployment automation plugin. Configures iOS/Android builds, Fastlane, TestFlight, Play Store, GitHub Actions CI/CD, code signing, OAuth providers, and self-hosted Mac Mini runners.",
  "author": { "name": "monxun" },
  "license": "MIT",
  "repository": "https://github.com/monxun/claude-code-plugins",
  "keywords": [
    "flutter",
    "firebase",
    "deployment",
    "ios",
    "android",
    "fastlane",
    "testflight",
    "playstore",
    "github-actions",
    "code-signing",
    "oauth",
    "ci-cd",
    "automation"
  ],
  "commands": "./commands/",
  "agents": [
    "./agents/orchestrator.md",
    "./agents/flutter-analyzer.md",
    "./agents/firebase-configurator.md",
    "./agents/ios-specialist.md",
    "./agents/android-specialist.md",
    "./agents/fastlane-specialist.md",
    "./agents/github-actions-specialist.md",
    "./agents/signing-specialist.md",
    "./agents/oauth-configurator.md",
    "./agents/simulator-tester.md",
    "./agents/researcher.md",
    "./agents/validator.md",
    "./agents/troubleshooter.md"
  ],
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json"
}

```

## File: flutter-firebase-deploy/commands/setup-ios.md

- Extension: .md
- Language: markdown
- Size: 860 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/troubleshoot.md

- Extension: .md
- Language: markdown
- Size: 931 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:troubleshoot
description: Diagnose and fix common Flutter Firebase deployment issues. Provides solutions for build, signing, and deployment errors.
---

# Troubleshoot

Diagnose and resolve deployment issues.

## Usage

```
/flutter-firebase-deploy:troubleshoot [error-message]
```

## Arguments

- `error-message` - Optional error message to diagnose

## Common Issues Diagnosed

### Build Errors
- CocoaPods conflicts
- Gradle failures
- SDK version mismatches

### Signing Errors
- Certificate issues
- Provisioning profile problems
- Keystore errors

### Deployment Errors
- App Store rejections
- Play Store failures
- API authentication issues

## What This Does

1. Analyzes error message or logs
2. Identifies root cause
3. Suggests specific fixes
4. Optionally applies fixes
5. Verifies resolution

## Example

```
/flutter-firebase-deploy:troubleshoot "No signing certificate found"
```

```

## File: flutter-firebase-deploy/commands/run-simulator-tests.md

- Extension: .md
- Language: markdown
- Size: 846 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:run-simulator-tests
description: Run tests on iOS Simulator or Android Emulator. Executes unit, widget, and integration tests.
---

# Run Simulator Tests

Execute tests on simulators/emulators.

## Usage

```
/flutter-firebase-deploy:run-simulator-tests [--platform ios|android] [--type unit|widget|integration]
```

## Options

- `--platform` - Target platform (default: both)
- `--type` - Test type (default: all)

## Test Types

- `unit` - Unit tests (test/unit/)
- `widget` - Widget tests (test/widget/)
- `integration` - Integration tests (integration_test/)

## What This Does

1. Boots appropriate simulator/emulator
2. Runs specified test suite
3. Captures screenshots on failure
4. Reports test results

## Example

```
/flutter-firebase-deploy:run-simulator-tests --platform ios --type integration
```

```

## File: flutter-firebase-deploy/commands/configure-oauth.md

- Extension: .md
- Language: markdown
- Size: 838 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/validate-config.md

- Extension: .md
- Language: markdown
- Size: 896 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:validate-config
description: Validate all deployment configurations. Checks Firebase, signing, Fastlane, and CI/CD setup for deployment readiness.
---

# Validate Configuration

Comprehensive validation of deployment configuration.

## Usage

```
/flutter-firebase-deploy:validate-config [--fix]
```

## Options

- `--fix` - Attempt to automatically fix issues

## Validation Checks

### Flutter
- [ ] Flutter doctor passes
- [ ] No analyzer warnings
- [ ] Tests pass

### Firebase
- [ ] Config files present
- [ ] Package names match
- [ ] SHA fingerprints configured

### Signing
- [ ] iOS certificates valid
- [ ] Android keystore accessible
- [ ] Match configured

### Fastlane
- [ ] Lanes defined
- [ ] Credentials configured

### CI/CD
- [ ] Workflow files valid
- [ ] Secrets documented

## Example

```
/flutter-firebase-deploy:validate-config --fix
```

```

## File: flutter-firebase-deploy/commands/deploy-playstore.md

- Extension: .md
- Language: markdown
- Size: 892 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/configure-github-actions.md

- Extension: .md
- Language: markdown
- Size: 943 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:configure-github-actions
description: Set up GitHub Actions workflows for CI/CD. Creates workflows for testing, building, and deploying to stores.
---

# Configure GitHub Actions

Set up CI/CD pipelines with GitHub Actions.

## Usage

```
/flutter-firebase-deploy:configure-github-actions [--triggers push,pr] [--platforms ios,android]
```

## Options

- `--triggers` - Workflow triggers (default: push)
- `--platforms` - Platforms to deploy (default: ios,android)

## What This Does

1. Creates workflow files
2. Documents required secrets
3. Configures build steps
4. Sets up deployment steps
5. Provides secret setup guidance

## Generated Workflows

- `.github/workflows/test.yml` - Run tests on PR
- `.github/workflows/ios-deploy.yml` - iOS deployment
- `.github/workflows/android-deploy.yml` - Android deployment

## Example

```
/flutter-firebase-deploy:configure-github-actions --triggers push,pr
```

```

## File: flutter-firebase-deploy/commands/analyze-project.md

- Extension: .md
- Language: markdown
- Size: 930 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:analyze-project
description: Analyze a Flutter project to detect Firebase features, dependencies, and platform support for deployment configuration.
---

# Analyze Flutter Project

Analyze the current Flutter project to understand its deployment requirements.

## Usage

```
/flutter-firebase-deploy:analyze-project [path]
```

## Arguments

- `path` - Optional path to Flutter project (defaults to current directory)

## What This Does

1. Parses `pubspec.yaml` for dependencies
2. Detects Firebase packages and features
3. Checks iOS and Android platform support
4. Identifies existing configuration files
5. Reports missing configurations

## Output

Detailed analysis report with:
- Project info (name, Flutter version)
- Detected Firebase features
- Platform status (iOS/Android)
- Configuration recommendations

## Example

```
/flutter-firebase-deploy:analyze-project ./my-flutter-app
```

```

## File: flutter-firebase-deploy/commands/configure-fastlane.md

- Extension: .md
- Language: markdown
- Size: 957 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/setup-self-hosted-runner.md

- Extension: .md
- Language: markdown
- Size: 957 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:setup-self-hosted-runner
description: Configure a self-hosted GitHub Actions runner on Mac Mini for iOS builds requiring hardware access.
---

# Setup Self-Hosted Runner

Configure Mac Mini as a self-hosted GitHub Actions runner.

## Usage

```
/flutter-firebase-deploy:setup-self-hosted-runner [--labels ios,macos]
```

## Options

- `--labels` - Runner labels for workflow targeting

## What This Does

1. Downloads GitHub Actions runner
2. Configures runner with repository
3. Installs as launch daemon
4. Configures Xcode CLI tools
5. Sets up required certificates

## Prerequisites

- Mac Mini with macOS
- Admin access
- GitHub repository admin access
- Runner registration token

## Runner Labels

Use labels to target specific runners:
- `ios` - iOS build capable
- `macos` - macOS runner
- `self-hosted` - Not GitHub-hosted

## Example

```
/flutter-firebase-deploy:setup-self-hosted-runner --labels ios,macos
```

```

## File: flutter-firebase-deploy/commands/setup-android.md

- Extension: .md
- Language: markdown
- Size: 796 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/deploy-testflight.md

- Extension: .md
- Language: markdown
- Size: 816 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/commands/configure-firebase.md

- Extension: .md
- Language: markdown
- Size: 814 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-firebase-deploy:configure-firebase
description: Configure Firebase for a Flutter project. Sets up FlutterFire CLI, generates config files, and initializes Firebase in the app.
---

# Configure Firebase

Set up Firebase integration for the Flutter project.

## Usage

```
/flutter-firebase-deploy:configure-firebase [project-id]
```

## Arguments

- `project-id` - Firebase project ID

## What This Does

1. Installs FlutterFire CLI
2. Runs `flutterfire configure`
3. Generates platform config files
4. Updates main.dart with Firebase initialization
5. Validates configuration

## Prerequisites

- Firebase project created in Firebase Console
- Firebase CLI installed and logged in
- Flutter project initialized

## Example

```
/flutter-firebase-deploy:configure-firebase my-firebase-project
```

```

## File: flutter-firebase-deploy/skills/signing-management/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1202 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/skills/flutter-analysis/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1207 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: flutter-analysis
description: Analyze Flutter projects to detect Firebase features, dependencies, platform support, and configuration requirements. Use when analyzing a new Flutter project for deployment setup.
trigger_keywords:
  - analyze flutter
  - flutter project
  - detect firebase
  - project analysis
  - flutter setup
---

# Flutter Project Analysis

Analyze Flutter projects to understand their structure and deployment requirements.

## Quick Analysis

```bash
# Check Flutter version
flutter --version

# Get project info
flutter pub get
flutter analyze
```

## What to Analyze

### pubspec.yaml
- Flutter SDK constraints
- Firebase dependencies
- Platform support indicators

### Platform Directories
- `ios/` - iOS support
- `android/` - Android support
- `web/` - Web support

### Firebase Packages
| Package | Feature |
|---------|---------|
| firebase_core | Core SDK |
| firebase_auth | Authentication |
| cloud_firestore | Database |
| firebase_messaging | Push notifications |
| firebase_crashlytics | Crash reporting |

## Output

Report detected features, missing configurations, and recommended next steps.

## References

See `references/` for detailed analysis patterns.

```

## File: flutter-firebase-deploy/skills/fastlane-automation/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1181 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: fastlane-automation
description: Configure Fastlane for Flutter build and deployment automation. Set up lanes for TestFlight, Play Store, and Match code signing. Use when automating builds.
trigger_keywords:
  - fastlane
  - fastfile
  - matchfile
  - testflight lane
  - playstore lane
  - automate deploy
---

# Fastlane Automation

Automate Flutter builds and deployments with Fastlane.

## Initialize

```bash
# iOS
cd ios && fastlane init

# Android
cd android && fastlane init
```

## iOS Lanes

```ruby
platform :ios do
  lane :beta do
    match(type: "appstore")
    build_app(scheme: "Runner")
    upload_to_testflight
  end
end
```

## Android Lanes

```ruby
platform :android do
  lane :internal do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(track: "internal")
  end
end
```

## Match Setup

```bash
fastlane match init
fastlane match appstore
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `fastlane ios beta` | Deploy to TestFlight |
| `fastlane android internal` | Deploy to Play Store Internal |
| `fastlane match appstore` | Sync certificates |

## References

See `references/` for complete Fastfile templates.

```

## File: flutter-firebase-deploy/skills/simulator-testing/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1063 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: simulator-testing
description: Run tests on iOS Simulator and Android Emulator. Execute unit, widget, and integration tests. Use when testing before deployment.
trigger_keywords:
  - simulator
  - emulator
  - run tests
  - integration test
  - flutter test
  - device testing
---

# Simulator Testing

Test Flutter apps on simulators and emulators.

## iOS Simulator

```bash
# List simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot "iPhone 15 Pro"

# Run tests
flutter test -d "iPhone 15 Pro"
```

## Android Emulator

```bash
# List AVDs
emulator -list-avds

# Start emulator
emulator -avd Pixel_7_API_34 &

# Run tests
flutter test -d emulator-5554
```

## Test Types

```bash
# Unit tests
flutter test test/unit/

# Widget tests
flutter test test/widget/

# Integration tests
flutter test integration_test/
```

## Firebase Test Lab

```bash
# iOS
gcloud firebase test ios run --test ios_tests.zip

# Android
gcloud firebase test android run --app app.apk
```

## References

See `references/` for advanced testing patterns.

```

## File: flutter-firebase-deploy/skills/ios-setup/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1257 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: ios-setup
description: Configure iOS/Xcode settings for Flutter Firebase deployment. Set up capabilities, entitlements, provisioning, and Info.plist entries. Use when configuring iOS platform.
trigger_keywords:
  - ios setup
  - xcode config
  - ios capabilities
  - ios entitlements
  - podfile
  - info.plist
---

# iOS Setup

Configure Xcode project for Flutter Firebase deployment.

## Key Files

| File | Purpose |
|------|---------|
| `ios/Runner.xcodeproj` | Xcode project |
| `ios/Runner/Info.plist` | App configuration |
| `ios/Runner/Runner.entitlements` | Capabilities |
| `ios/Podfile` | CocoaPods dependencies |

## Capabilities

Enable in Xcode:
- Push Notifications
- Sign in with Apple
- Associated Domains
- Background Modes (remote-notification)

## Podfile Setup

```ruby
platform :ios, '13.0'

target 'Runner' do
  use_frameworks!
  use_modular_headers!
  flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
end

post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
  end
end
```

## Build Commands

```bash
cd ios
pod install --repo-update
open Runner.xcworkspace
```

## References

See `references/` for detailed Xcode configuration.

```

## File: flutter-firebase-deploy/skills/troubleshooting/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1347 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/skills/github-actions-cicd/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1359 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: github-actions-cicd
description: Configure GitHub Actions for Flutter CI/CD. Set up workflows for iOS and Android builds, testing, and deployment. Use when setting up CI/CD pipelines.
trigger_keywords:
  - github actions
  - ci cd
  - workflow
  - automated build
  - deploy pipeline
  - self-hosted runner
---

# GitHub Actions CI/CD

Configure automated builds and deployments with GitHub Actions.

## Workflow Location

`.github/workflows/`

## iOS Workflow

```yaml
name: iOS Deploy
on: [push]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: cd ios && pod install
      - run: cd ios && fastlane beta
```

## Android Workflow

```yaml
name: Android Deploy
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
      - uses: subosito/flutter-action@v2
      - run: flutter build appbundle
      - run: cd android && fastlane internal
```

## Required Secrets

| Secret | Purpose |
|--------|---------|
| MATCH_PASSWORD | Match decryption |
| ASC_API_KEY | App Store Connect |
| PLAY_STORE_JSON | Play Store API |

## Self-Hosted Runner

For macOS builds with hardware access.

## References

See `references/` for complete workflow templates.

```

## File: flutter-firebase-deploy/skills/firebase-config/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1189 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
---
name: firebase-config
description: Configure Firebase for Flutter apps. Set up FlutterFire, platform-specific config files, and Firebase Console settings. Use when setting up Firebase integration.
trigger_keywords:
  - firebase setup
  - configure firebase
  - flutterfire
  - google-services
  - firebase init
---

# Firebase Configuration

Configure Firebase for Flutter applications across all platforms.

## FlutterFire Setup

```bash
dart pub global activate flutterfire_cli
flutterfire configure --project=your-project-id
```

## Platform Files

### Android
- `android/app/google-services.json`
- Verify package name matches

### iOS
- `ios/Runner/GoogleService-Info.plist`
- Add to Xcode project

## Firebase Initialization

```dart
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}
```

## Feature Configuration

Each Firebase feature requires specific setup. See `references/` for details.

## Validation

```bash
flutter run  # Should initialize without errors
```

```

## File: flutter-firebase-deploy/skills/android-setup/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1666 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

## File: flutter-firebase-deploy/skills/oauth-integration/SKILL.md

- Extension: .md
- Language: markdown
- Size: 1185 bytes
- Created: 2026-01-16 01:59:07
- Modified: 2026-01-16 01:59:07

### Code

```markdown
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

```

