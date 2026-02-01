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
