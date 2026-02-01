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
