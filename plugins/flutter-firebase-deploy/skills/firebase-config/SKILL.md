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
