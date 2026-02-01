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

## CLI Integration

The flutter-deploy CLI provides enhanced analysis capabilities. Check if available before analysis.

### Check for CLI Analysis Output

```bash
# Check if CLI has already analyzed the project
if [ -f "flutter-deploy-config.json" ]; then
    echo "CLI analysis found"
    cat flutter-deploy-config.json
fi
```

### Using CLI for Analysis

When CLI is available, you can delegate analysis:

```bash
# Check CLI availability
flutter-deploy --version

# Run CLI analysis (interactive)
# Note: CLI analysis is interactive, best run by user directly
```

### CLI Analysis Output

The CLI produces comprehensive analysis including:
- iOS permissions (Info.plist entries needed)
- iOS entitlements (Xcode capabilities)
- iOS background modes
- Android permissions (AndroidManifest.xml)
- Firebase service detection
- OAuth provider detection
- Feature detection (camera, location, etc.)

### Fallback to Agent Analysis

If CLI is not available or hasn't been run:
1. Fall back to agent-based file analysis
2. Parse pubspec.yaml directly
3. Check platform directories
4. Generate equivalent output format

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
