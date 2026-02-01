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
