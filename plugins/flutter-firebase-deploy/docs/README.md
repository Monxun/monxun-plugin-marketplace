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
