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
