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
