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
