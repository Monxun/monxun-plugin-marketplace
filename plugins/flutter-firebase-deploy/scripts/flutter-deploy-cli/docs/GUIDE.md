# 🚀 Flutter Deploy CLI - Comprehensive Guide

```
    ███████╗██╗     ██╗   ██╗████████╗████████╗███████╗██████╗ 
    ██╔════╝██║     ██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
    █████╗  ██║     ██║   ██║   ██║      ██║   █████╗  ██████╔╝
    ██╔══╝  ██║     ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
    ██║     ███████╗╚██████╔╝   ██║      ██║   ███████╗██║  ██║
    ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝
    ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
    ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
    ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
    ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
```

> **The complete automation toolkit for deploying Flutter apps to iOS and Android**

---

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Architecture Overview](#architecture-overview)
6. [Phase 1: Project Analysis](#phase-1-project-analysis)
7. [Phase 2: App Store Setup](#phase-2-app-store-setup)
8. [Phase 3: Firebase Configuration](#phase-3-firebase-configuration)
9. [Phase 4: OAuth Providers](#phase-4-oauth-providers)
10. [Phase 5: Configuration Wizard](#phase-5-configuration-wizard)
11. [Phase 6: Fastlane Generation](#phase-6-fastlane-generation)
12. [Phase 7: Credentials & Code Signing](#phase-7-credentials--code-signing)
13. [Phase 8: GitHub Actions Workflows](#phase-8-github-actions-workflows)
14. [Phase 9: Self-Hosted Runner Setup](#phase-9-self-hosted-runner-setup)
15. [Configuration Reference](#configuration-reference)
16. [CI/CD Pipeline Deep Dive](#cicd-pipeline-deep-dive)
17. [Troubleshooting](#troubleshooting)
18. [Best Practices](#best-practices)
19. [FAQ](#faq)
20. [Contributing](#contributing)

---

## Introduction

Flutter Deploy CLI is a comprehensive automation tool designed to eliminate the complexity of deploying Flutter applications to both iOS and Android platforms. It automates everything from analyzing your project's requirements to setting up complete CI/CD pipelines with GitHub Actions and self-hosted Mac Mini runners.

### Why Flutter Deploy CLI?

| Challenge | Solution |
|-----------|----------|
| Complex iOS provisioning | Automated Match setup with certificate management |
| Multiple environment configs | Per-environment builds (dev, staging, prod) |
| CI/CD setup complexity | Pre-configured GitHub Actions workflows |
| Build machine management | Mac Mini runner setup with maintenance scripts |
| Permission detection | Automatic pubspec.yaml analysis |
| Code signing headaches | Fastlane Match integration |

### Key Features

- **🔍 Intelligent Analysis** - Automatically detects required permissions, entitlements, and features
- **🏪 Store Integration** - Streamlines App Store Connect and Google Play Console setup
- **🔥 Firebase Ready** - Complete Firebase project configuration with per-environment support
- **🔐 OAuth Support** - Google, Apple, Facebook, and more authentication providers
- **🚀 Fastlane Automation** - Production-ready Fastlane configurations
- **🔄 GitHub Actions** - Complete CI/CD pipelines with self-hosted runner support
- **🖥️ Runner Management** - Mac Mini setup and maintenance automation
- **🎨 Beautiful Interface** - Stunning terminal UI with intuitive navigation

---

## Prerequisites

Before using Flutter Deploy CLI, ensure you have:

### Required Accounts

| Account | Purpose | Link |
|---------|---------|------|
| Apple Developer | iOS app distribution | [developer.apple.com](https://developer.apple.com) |
| Google Play Console | Android app distribution | [play.google.com/console](https://play.google.com/console) |
| GitHub | Source control & CI/CD | [github.com](https://github.com) |
| Firebase (optional) | Backend services | [firebase.google.com](https://firebase.google.com) |

### Required Software

```bash
# Python 3.10+
python3 --version  # Should be 3.10 or higher

# Git
git --version

# Flutter (for your project)
flutter --version
```

### For Mac Mini Runner

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| macOS | 13.0 (Ventura) | 14.0+ (Sonoma) |
| Xcode | 14.0 | 15.0+ |
| RAM | 8GB | 16GB+ |
| Storage | 128GB SSD | 256GB+ SSD |
| Processor | Apple Silicon or Intel | Apple Silicon (M1/M2/M3) |

---

## Installation

### Method 1: pip Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/flutter-deploy-cli.git
cd flutter-deploy-cli

# Install in development mode
pip install -e .

# Verify installation
flutter-deploy --help
```

### Method 2: Direct Execution

```bash
# Clone and run directly
git clone https://github.com/your-org/flutter-deploy-cli.git
cd flutter-deploy-cli

# Install dependencies
pip install rich questionary pyyaml

# Run directly
python src/cli.py
```

### Method 3: From Archive

```bash
# Extract the archive
tar -xzf flutter-deploy-cli.tar.gz
cd flutter-deploy-cli

# Install
pip install -e .
```

### Verify Installation

```bash
# Run the CLI
flutter-deploy

# Or use the short alias
fd
```

You should see the beautiful ASCII banner and main menu.

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Navigate to your Flutter project
cd /path/to/your/flutter-app

# 2. Run Flutter Deploy CLI
flutter-deploy

# 3. Select "📂 Select Flutter Project"
#    → Choose your project directory

# 4. Select "🚀 Start Full Deployment Pipeline"
#    → Follow the interactive prompts

# 5. Done! Check your generated files:
#    - ios/fastlane/
#    - android/fastlane/
#    - .github/workflows/
```

### Typical Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Your Flutter Project                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Flutter Deploy CLI                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │  Analyze  │→ │ Configure │→ │ Generate  │→ │  Output   │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Fastlane │   │  GitHub  │   │  Runner  │
        │  Config  │   │ Actions  │   │  Setup   │
        └──────────┘   └──────────┘   └──────────┘
```

---

## Architecture Overview

### Project Structure

```
flutter-deploy-cli/
├── src/
│   ├── cli.py                      # Main CLI application
│   │                               # - ASCII art banner
│   │                               # - Main menu system
│   │                               # - Phase orchestration
│   │
│   ├── analyzers/
│   │   └── flutter_analyzer.py     # Project analysis
│   │                               # - pubspec.yaml parsing
│   │                               # - Permission detection
│   │                               # - Feature detection
│   │
│   ├── generators/
│   │   ├── fastlane_generator.py   # Fastlane configs
│   │   │                           # - iOS Fastfile
│   │   │                           # - Android Fastfile
│   │   │                           # - Matchfile
│   │   │
│   │   ├── github_actions_generator.py  # CI/CD workflows
│   │   │                                # - ci.yml
│   │   │                                # - cd.yml
│   │   │                                # - release.yml
│   │   │
│   │   └── runner_setup.py         # Mac Mini setup
│   │                               # - setup-runner.sh
│   │                               # - maintenance.sh
│   │
│   ├── providers/                  # OAuth provider configs
│   │
│   └── utils/
│       └── config_wizard.py        # Interactive configuration
│                                   # - App metadata
│                                   # - Team settings
│                                   # - Environment config
│
├── templates/                      # Template files
├── pyproject.toml                  # Package configuration
└── README.md                       # Quick reference
```

### Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Analysis   │────▶│ Configuration│────▶│  Generation  │
│    Phase     │     │    Phase     │     │    Phase     │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Detected    │     │    User      │     │  Generated   │
│ Requirements │     │   Choices    │     │    Files     │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │    config    │
                   │    .json     │
                   └──────────────┘
```

---

## Phase 1: Project Analysis

### What It Does

The analyzer scans your Flutter project to automatically detect:

- **iOS Permissions** - Info.plist keys required
- **iOS Entitlements** - Xcode capabilities needed
- **iOS Background Modes** - Background execution requirements
- **Android Permissions** - AndroidManifest.xml entries
- **Firebase Services** - Which Firebase packages are used
- **Auth Providers** - Authentication methods detected
- **App Features** - High-level features identified

### How It Works

```python
# The analyzer parses pubspec.yaml
dependencies:
  camera: ^0.10.5          # → NSCameraUsageDescription
  geolocator: ^10.1.0      # → NSLocationWhenInUseUsageDescription
  firebase_messaging: ^14.7.0  # → aps-environment entitlement
  local_auth: ^2.1.7       # → NSFaceIDUsageDescription
```

### Permission Mapping

#### iOS Permissions

| Package | Info.plist Key | Description |
|---------|---------------|-------------|
| `camera` | `NSCameraUsageDescription` | Camera access |
| `image_picker` | `NSPhotoLibraryUsageDescription` | Photo library |
| `geolocator` | `NSLocationWhenInUseUsageDescription` | Location |
| `local_auth` | `NSFaceIDUsageDescription` | Face ID |
| `contacts_service` | `NSContactsUsageDescription` | Contacts |
| `flutter_blue` | `NSBluetoothAlwaysUsageDescription` | Bluetooth |
| `health` | `NSHealthShareUsageDescription` | HealthKit |
| `record` | `NSMicrophoneUsageDescription` | Microphone |

#### iOS Entitlements

| Package | Entitlement | Capability |
|---------|-------------|------------|
| `firebase_messaging` | `aps-environment` | Push Notifications |
| `sign_in_with_apple` | `com.apple.developer.applesignin` | Sign in with Apple |
| `in_app_purchase` | `com.apple.developer.in-app-payments` | In-App Purchases |
| `health` | `com.apple.developer.healthkit` | HealthKit |

#### Android Permissions

| Package | Permission |
|---------|------------|
| `camera` | `android.permission.CAMERA` |
| `geolocator` | `android.permission.ACCESS_FINE_LOCATION` |
| `contacts_service` | `android.permission.READ_CONTACTS` |
| `local_auth` | `android.permission.USE_BIOMETRIC` |
| `flutter_blue` | `android.permission.BLUETOOTH_CONNECT` |

### Running Analysis

```bash
# From the CLI menu
Select: "🔍 Phase 1: Analyze Flutter App"

# Output example:
╭─────────────────────── 📦 Project Information ───────────────────────╮
│ Name: my_awesome_app                                                  │
│ Path: /Users/dev/projects/my_awesome_app                             │
│ Dependencies: 20 packages                                             │
╰───────────────────────────────────────────────────────────────────────╯

                        🍎 iOS Requirements                              
╭────────────┬────────────────────────────────┬────────────────────────╮
│ Type       │ Key/Value                      │ Description            │
├────────────┼────────────────────────────────┼────────────────────────┤
│ Permission │ NSCameraUsageDescription       │ Camera access needed   │
│ Permission │ NSLocationWhenInUseUsageDesc...│ Location for maps      │
│ Entitlement│ aps-environment                │ Push notifications     │
│ Background │ remote-notification            │ Background push        │
╰────────────┴────────────────────────────────┴────────────────────────╯
```

### Generated Info.plist Template

After analysis, you'll get a template for your Info.plist:

```xml
<!-- Add to ios/Runner/Info.plist -->
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to take photos and videos.</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to select images.</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>This app needs your location to show nearby places.</string>

<key>NSFaceIDUsageDescription</key>
<string>This app uses Face ID for secure authentication.</string>

<key>UIBackgroundModes</key>
<array>
    <string>remote-notification</string>
</array>
```

---

## Phase 2: App Store Setup

### Apple App Store Connect

#### Prerequisites

1. Active Apple Developer Program membership ($99/year)
2. Admin or App Manager role in App Store Connect
3. Apple Team ID (found in Membership section)

#### What Gets Configured

```
App Store Connect
├── App ID (Bundle Identifier)
│   └── com.yourcompany.yourapp
├── Provisioning Profiles
│   ├── Development
│   ├── Ad Hoc
│   └── App Store Distribution
├── Capabilities
│   ├── Push Notifications
│   ├── Sign in with Apple
│   └── (based on analysis)
└── TestFlight
    ├── Internal Testing Group
    └── External Testing Group
```

#### App Store Connect API Key

For automation, create an API key:

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Navigate to **Users and Access** → **Keys**
3. Click **Generate API Key**
4. Select **Admin** role
5. Download the `.p8` file (only available once!)
6. Note the **Key ID** and **Issuer ID**

```bash
# Store these securely
APP_STORE_CONNECT_API_KEY_ID=ABC123XYZ
APP_STORE_CONNECT_API_ISSUER_ID=12345678-1234-1234-1234-123456789012
APP_STORE_CONNECT_API_KEY_CONTENT=$(cat AuthKey_ABC123XYZ.p8 | base64)
```

### Google Play Console

#### Prerequisites

1. Google Play Developer account ($25 one-time)
2. App created in Play Console
3. Service account with API access

#### What Gets Configured

```
Google Play Console
├── App Listing
│   ├── Package Name
│   └── App Metadata
├── Testing Tracks
│   ├── Internal Testing
│   ├── Closed Testing (Alpha)
│   ├── Open Testing (Beta)
│   └── Production
├── App Signing
│   └── Google-managed or Upload Key
└── Service Account
    └── API Access JSON Key
```

#### Creating Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Navigate to **IAM & Admin** → **Service Accounts**
4. Create service account with **Editor** role
5. Create JSON key and download
6. In Play Console, grant access to this service account

```bash
# The JSON key file looks like:
{
  "type": "service_account",
  "project_id": "your-project",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "your-service@your-project.iam.gserviceaccount.com",
  ...
}
```

---

## Phase 3: Firebase Configuration

### Overview

Firebase provides backend services for your Flutter app. The CLI helps configure:

- **Firebase Core** - Base SDK
- **Authentication** - User sign-in
- **Cloud Firestore** - NoSQL database
- **Realtime Database** - Real-time sync
- **Cloud Storage** - File storage
- **Cloud Messaging (FCM)** - Push notifications
- **Analytics** - Usage tracking
- **Crashlytics** - Crash reporting
- **Remote Config** - Feature flags
- **Dynamic Links** - Deep linking

### Per-Environment Projects

Best practice is separate Firebase projects per environment:

```
Firebase Projects
├── myapp-dev
│   ├── GoogleService-Info.plist (iOS)
│   └── google-services.json (Android)
├── myapp-staging
│   ├── GoogleService-Info.plist (iOS)
│   └── google-services.json (Android)
└── myapp-prod
    ├── GoogleService-Info.plist (iOS)
    └── google-services.json (Android)
```

### Firebase CLI Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize in your project
cd your-flutter-app
firebase init

# Or use FlutterFire CLI
dart pub global activate flutterfire_cli
flutterfire configure
```

### iOS FCM Setup (APNs)

For push notifications on iOS:

1. Create APNs Key in Apple Developer Portal
2. Upload to Firebase Console → Project Settings → Cloud Messaging
3. Add capability in Xcode

```
Apple Developer Portal
└── Certificates, Identifiers & Profiles
    └── Keys
        └── Create APNs Key
            ├── Key ID: ABC123
            └── Download .p8 file

Firebase Console
└── Project Settings
    └── Cloud Messaging
        └── iOS app configuration
            └── Upload APNs key (.p8)
```

### Configuration Files

The CLI generates environment-aware Firebase initialization:

```dart
// lib/firebase_options_dev.dart
// lib/firebase_options_staging.dart
// lib/firebase_options_prod.dart

// main.dart
import 'firebase_options_${environment}.dart';

await Firebase.initializeApp(
  options: DefaultFirebaseOptions.currentPlatform,
);
```

---

## Phase 4: OAuth Providers

### Supported Providers

| Provider | Package | Configuration Required |
|----------|---------|----------------------|
| Google | `google_sign_in` | OAuth Client IDs |
| Apple | `sign_in_with_apple` | Services ID, Entitlement |
| Facebook | `flutter_facebook_auth` | App ID, Client Token |
| Twitter/X | `twitter_login` | API Key, Secret |
| GitHub | `github_sign_in` | OAuth App credentials |

### Google Sign-In

#### iOS Configuration

1. Create OAuth Client ID in [Google Cloud Console](https://console.cloud.google.com)
2. Download client ID
3. Add reversed client ID to URL schemes

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <!-- Reversed client ID -->
            <string>com.googleusercontent.apps.123456789-abcdefg</string>
        </array>
    </dict>
</array>
```

#### Android Configuration

1. Add SHA-1 and SHA-256 fingerprints to Firebase
2. Download updated `google-services.json`

```bash
# Get SHA fingerprints
cd android
./gradlew signingReport

# Add to Firebase Console → Project Settings → Your Android App
```

### Apple Sign-In

#### Configuration

1. Enable capability in Xcode
2. Create Services ID in Apple Developer Portal
3. Configure return URLs

```
Apple Developer Portal
└── Certificates, Identifiers & Profiles
    └── Identifiers
        ├── App ID: com.yourcompany.yourapp
        │   └── Enable "Sign in with Apple"
        └── Services ID: com.yourcompany.yourapp.signin
            └── Configure return URLs
```

#### Xcode Entitlement

```xml
<!-- ios/Runner/Runner.entitlements -->
<key>com.apple.developer.applesignin</key>
<array>
    <string>Default</string>
</array>
```

### Facebook Login

#### Configuration

1. Create app in [Meta Developer Portal](https://developers.facebook.com)
2. Configure iOS and Android platforms
3. Add App ID and Client Token

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>fb{your-app-id}</string>
        </array>
    </dict>
</array>
<key>FacebookAppID</key>
<string>{your-app-id}</string>
<key>FacebookClientToken</key>
<string>{your-client-token}</string>
<key>FacebookDisplayName</key>
<string>{your-app-name}</string>
```

---

## Phase 5: Configuration Wizard

### Interactive Prompts

The configuration wizard collects all necessary information through beautiful interactive prompts:

```
╭────────────────────── ⚙️  Configuration Wizard ──────────────────────╮
│                                                                       │
│  Welcome to the Configuration Wizard!                                 │
│                                                                       │
│  This wizard will guide you through setting up your deployment       │
│  configuration. Press Ctrl+C at any time to cancel.                  │
│                                                                       │
╰───────────────────────────────────────────────────────────────────────╯

? App Display Name: My Awesome App
? iOS Bundle Identifier: com.example.myawesomeapp
? Android Package Name: com.example.myawesomeapp
? Initial Version: 1.0.0
```

### Configuration Sections

#### 1. Basic App Information

```yaml
app_name: "My Awesome App"
ios_bundle_id: "com.example.myawesomeapp"
android_package_name: "com.example.myawesomeapp"
version: "1.0.0"
```

#### 2. Team & Organization

```yaml
organization_name: "Example Inc."
team_email: "team@example.com"
apple_team_id: "ABC123XYZ"
```

#### 3. Environments

```yaml
environments:
  - dev
  - staging
  - prod

env_config:
  dev:
    api_url: "https://api.dev.example.com"
  staging:
    api_url: "https://api.staging.example.com"
  prod:
    api_url: "https://api.example.com"
```

#### 4. Firebase Configuration

```yaml
firebase:
  project_id: "myapp"
  per_env: true
  dev_project_id: "myapp-dev"
  staging_project_id: "myapp-staging"
  prod_project_id: "myapp-prod"
  services:
    - auth
    - firestore
    - messaging
    - analytics
    - crashlytics
```

#### 5. Authentication Providers

```yaml
auth_providers:
  - google
  - apple
  - facebook

oauth_config:
  google:
    ios_client_id: "123456789-abc.apps.googleusercontent.com"
    web_client_id: "123456789-xyz.apps.googleusercontent.com"
  apple:
    service_id: "com.example.myawesomeapp.signin"
  facebook:
    app_id: "1234567890"
    client_token: "abcdef123456"
```

#### 6. Code Signing

```yaml
code_signing:
  ios_method: "match"  # match, manual, or automatic
  match:
    git_url: "git@github.com:myorg/certificates.git"
    storage_mode: "git"  # git, s3, or google_cloud
    type: "appstore"
  android:
    keystore_path: "android/app/release.keystore"
    key_alias: "release"
```

#### 7. CI/CD Configuration

```yaml
cicd:
  github_repo: "myorg/my-awesome-app"
  use_self_hosted: true
  runner:
    labels:
      - self-hosted
      - macOS
      - ARM64
    xcode_version: "15.2"
  triggers:
    build_on_pr: true
    deploy_on_merge: true
    deploy_on_tag: true
```

### Saving Configuration

Configuration is saved to `flutter-deploy-config.json`:

```bash
# Export configuration
Select: "💾 Export Configuration"
? Export filename: flutter-deploy-config.json

# Import configuration
Select: "📥 Import Configuration"
? Import configuration file: flutter-deploy-config.json
```

---

## Phase 6: Fastlane Generation

### Generated Files

```
your-flutter-app/
├── ios/
│   ├── Gemfile
│   └── fastlane/
│       ├── Fastfile       # Build and deployment lanes
│       ├── Appfile        # App identifiers
│       ├── Matchfile      # Code signing config
│       └── Pluginfile     # Required plugins
└── android/
    ├── Gemfile
    └── fastlane/
        ├── Fastfile       # Build and deployment lanes
        ├── Appfile        # Package name
        └── Pluginfile     # Required plugins
```

### iOS Fastfile Lanes

```ruby
# Generated lanes for iOS

# Code Signing
lane :sync_dev_certs      # Sync development certificates
lane :sync_dist_certs     # Sync distribution certificates
lane :sync_adhoc_certs    # Sync ad hoc certificates

# Per-Environment Builds
lane :build_dev           # Build development version
lane :build_staging       # Build staging version
lane :build_prod          # Build production version

# Deployment
lane :beta                # Upload to TestFlight
lane :release             # Submit to App Store

# Testing
lane :test                # Run unit tests
```

### Android Fastfile Lanes

```ruby
# Generated lanes for Android

# Per-Environment Builds
lane :build_dev           # Build dev AAB/APK
lane :build_staging       # Build staging AAB/APK
lane :build_prod          # Build production AAB/APK

# Deployment
lane :deploy_dev          # Deploy to internal track
lane :deploy_staging      # Deploy to alpha track
lane :deploy_prod         # Deploy to production
lane :release             # Full production release

# Testing
lane :test                # Run unit tests
lane :build_debug         # Build debug APK
```

### Using Fastlane Locally

```bash
# iOS
cd ios
bundle install
bundle exec fastlane beta env:staging

# Android
cd android
bundle install
bundle exec fastlane deploy_staging
```

### Environment Variables for Fastlane

```bash
# iOS
export MATCH_PASSWORD="your-match-password"
export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export APP_STORE_CONNECT_API_KEY_ID="ABC123"
export APP_STORE_CONNECT_API_ISSUER_ID="12345678-..."
export APP_STORE_CONNECT_API_KEY_CONTENT="base64-encoded-p8"

# Android
export KEYSTORE_PATH="/path/to/release.keystore"
export KEYSTORE_PASSWORD="your-keystore-password"
export KEY_ALIAS="release"
export KEY_PASSWORD="your-key-password"
export PLAY_STORE_JSON_KEY="/path/to/play-store-key.json"

# Optional
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

---

## Phase 7: Credentials & Code Signing

### iOS Code Signing with Match

Fastlane Match manages certificates and provisioning profiles in a shared repository.

#### Initial Setup

```bash
# Create certificates repository
# This should be a PRIVATE repository
git init ios-certificates
cd ios-certificates
git remote add origin git@github.com:myorg/certificates.git

# Initialize Match
cd your-flutter-app/ios
bundle exec fastlane match init

# Generate certificates (run once per team)
bundle exec fastlane match development
bundle exec fastlane match appstore
bundle exec fastlane match adhoc
```

#### Match Storage Options

| Storage | Pros | Cons |
|---------|------|------|
| Git | Free, version controlled | Requires Git access |
| S3 | Scalable, AWS integrated | AWS costs |
| Google Cloud | GCP integrated | GCP costs |

#### Matchfile Configuration

```ruby
# ios/fastlane/Matchfile
git_url("git@github.com:myorg/certificates.git")
storage_mode("git")
type("appstore")
app_identifier(["com.example.myawesomeapp"])
username("team@example.com")
team_id("ABC123XYZ")
```

### Android Code Signing

#### Creating a Keystore

```bash
# Generate release keystore
keytool -genkey -v \
  -keystore release.keystore \
  -alias release \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Store securely!
# NEVER commit to version control
```

#### Keystore Configuration

```properties
# android/key.properties (DO NOT COMMIT)
storePassword=your-store-password
keyPassword=your-key-password
keyAlias=release
storeFile=../release.keystore
```

```groovy
// android/app/build.gradle
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
            storeFile file(keystoreProperties['storeFile'])
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

### Secrets Management

#### GitHub Actions Secrets

| Secret | Description |
|--------|-------------|
| `MATCH_PASSWORD` | Match encryption password |
| `MATCH_SSH_KEY` | SSH key for certificates repo |
| `APP_STORE_CONNECT_API_KEY_ID` | App Store Connect API Key ID |
| `APP_STORE_CONNECT_API_ISSUER_ID` | App Store Connect Issuer ID |
| `APP_STORE_CONNECT_API_KEY_CONTENT` | Base64 encoded .p8 key |
| `ANDROID_KEYSTORE_BASE64` | Base64 encoded keystore |
| `ANDROID_KEYSTORE_PASSWORD` | Keystore password |
| `ANDROID_KEY_ALIAS` | Key alias |
| `ANDROID_KEY_PASSWORD` | Key password |
| `PLAY_STORE_JSON_KEY` | Play Store service account JSON |

#### Setting Up GitHub Secrets

```bash
# 1. Go to your repository on GitHub
# 2. Navigate to Settings → Secrets and variables → Actions
# 3. Click "New repository secret"
# 4. Add each secret

# For base64 encoding:
cat release.keystore | base64 > keystore_base64.txt
cat AuthKey_ABC123.p8 | base64 > api_key_base64.txt
```

---

## Phase 8: GitHub Actions Workflows

### Generated Workflows

```
.github/
├── workflows/
│   ├── ci.yml              # Continuous Integration
│   ├── cd.yml              # Continuous Deployment
│   ├── release.yml         # Production releases
│   └── runner-health.yml   # Self-hosted runner monitoring
└── dependabot.yml          # Dependency updates
```

### CI Workflow (ci.yml)

Triggered on: Pull requests and pushes to main/develop

```yaml
Jobs:
  analyze:     # Code analysis and formatting
  test:        # Run Flutter tests
  build-ios:   # Build iOS (no codesign)
  build-android: # Build Android APK/AAB
```

```
┌─────────┐     ┌─────────┐     ┌─────────────┐
│ Analyze │────▶│  Test   │────▶│ Build iOS   │
└─────────┘     └─────────┘     └─────────────┘
                     │          ┌─────────────┐
                     └─────────▶│Build Android│
                                └─────────────┘
```

### CD Workflow (cd.yml)

Triggered on: Push to main, version tags, manual dispatch

```yaml
Jobs:
  setup:        # Determine environment and version
  deploy-ios:   # Build and upload to TestFlight
  deploy-android: # Build and upload to Play Store
  notify:       # Send Slack notification
```

```
┌─────────┐     ┌─────────────┐     ┌─────────┐
│  Setup  │────▶│ Deploy iOS  │────▶│ Notify  │
└─────────┘     └─────────────┘     └─────────┘
     │          ┌─────────────┐          ▲
     └─────────▶│Deploy Android│─────────┘
                └─────────────┘
```

### Release Workflow (release.yml)

Triggered on: GitHub Release published

```yaml
Jobs:
  release-ios:     # Submit to App Store
  release-android: # Submit to Play Store (production)
```

### Runner Health Workflow (runner-health.yml)

Scheduled: Every 6 hours

```yaml
Jobs:
  health-check:   # Verify runner is operational
    - System info
    - Xcode version
    - Flutter version
    - Disk space
    - Optional: Clean caches
```

### Workflow Triggers

| Trigger | CI | CD | Release |
|---------|----|----|---------|
| PR opened | ✅ | ❌ | ❌ |
| Push to main | ✅ | ✅ | ❌ |
| Push to develop | ✅ | ❌ | ❌ |
| Version tag (v*) | ❌ | ✅ | ❌ |
| Release published | ❌ | ❌ | ✅ |
| Manual dispatch | ❌ | ✅ | ❌ |

### Manual Deployment

```yaml
# Trigger CD workflow manually
workflow_dispatch:
  inputs:
    environment:
      description: 'Deployment environment'
      options: [staging, production]
    platform:
      description: 'Platform to deploy'
      options: [ios, android, both]
```

---

## Phase 9: Self-Hosted Runner Setup

### Why Self-Hosted?

| Aspect | GitHub-Hosted | Self-Hosted Mac Mini |
|--------|--------------|---------------------|
| Cost | Free (limited mins) / $0.08/min | One-time hardware cost |
| Speed | Slower (cold start) | Faster (always warm) |
| Xcode | Limited versions | Any version |
| Storage | Reset each run | Persistent caches |
| Customization | Limited | Full control |
| iOS Builds | ✅ (macOS runners) | ✅ |

### Generated Setup Scripts

```
runner-setup/
├── setup-runner.sh         # Main installation script
├── maintenance.sh          # Cleanup and health checks
├── runner.env.template     # Environment variables template
└── com.github.actions.runner.plist  # launchd auto-start
```

### Setup Script Features

The `setup-runner.sh` script installs:

```bash
# Core Tools
✓ Homebrew
✓ Git, gh, jq, wget

# Development
✓ Ruby (via rbenv)
✓ Java 17 (OpenJDK)
✓ Flutter
✓ CocoaPods
✓ Fastlane

# Runner
✓ GitHub Actions Runner
✓ Auto-start configuration
✓ Helper scripts
```

### Installation Steps

```bash
# 1. Copy setup files to Mac Mini
scp -r runner-setup/ user@mac-mini:~/

# 2. SSH into Mac Mini
ssh user@mac-mini

# 3. Run setup script
cd ~/runner-setup
chmod +x setup-runner.sh
./setup-runner.sh

# 4. Configure runner with GitHub token
cd ~/actions-runner
./config.sh --url https://github.com/OWNER/REPO --token YOUR_TOKEN --labels self-hosted,macOS,ARM64

# 5. Install as service
sudo ./svc.sh install
sudo ./svc.sh start

# 6. Verify
sudo ./svc.sh status
```

### Runner Labels

Configure labels to target your runner:

```yaml
# In workflow files
jobs:
  build-ios:
    runs-on: [self-hosted, macOS, ARM64]
```

Common labels:
- `self-hosted` - Required for self-hosted runners
- `macOS` - Operating system
- `ARM64` or `X64` - Architecture
- `xcode-15` - Specific Xcode version
- `flutter-stable` - Flutter channel

### Maintenance

```bash
# Run health check
~/maintenance.sh health

# Clean build caches
~/maintenance.sh cleanup

# Update dependencies
~/maintenance.sh update

# Restart runner
~/maintenance.sh restart

# Full maintenance (all tasks)
~/maintenance.sh full
```

### Scheduled Maintenance

Add to crontab for automatic maintenance:

```bash
# Edit crontab
crontab -e

# Add weekly cleanup (Sundays at 3 AM)
0 3 * * 0 /Users/runner/maintenance.sh full >> /Users/runner/maintenance.log 2>&1
```

### Security Considerations

1. **Dedicated User** - Create a dedicated user for the runner
2. **Firewall** - Enable macOS firewall
3. **Updates** - Keep macOS and Xcode updated
4. **Secrets** - Never store secrets in plain text
5. **Network** - Use secure network connection
6. **Physical** - Secure physical access to the machine

---

## Configuration Reference

### Complete Configuration Schema

```json
{
  "app_name": "string",
  "ios_bundle_id": "string (com.example.app)",
  "android_package_name": "string (com.example.app)",
  "version": "string (1.0.0)",
  
  "organization_name": "string",
  "team_email": "string (email)",
  "apple_team_id": "string (10 chars)",
  
  "environments": ["dev", "staging", "prod"],
  "env_config": {
    "dev": { "api_url": "string" },
    "staging": { "api_url": "string" },
    "prod": { "api_url": "string" }
  },
  
  "firebase": {
    "project_id": "string",
    "per_env": "boolean",
    "dev_project_id": "string",
    "staging_project_id": "string",
    "prod_project_id": "string",
    "services": ["auth", "firestore", "messaging", "analytics", "crashlytics"]
  },
  
  "auth_providers": ["google", "apple", "facebook"],
  "oauth_config": {
    "google": {
      "ios_client_id": "string",
      "web_client_id": "string"
    },
    "apple": {
      "service_id": "string"
    },
    "facebook": {
      "app_id": "string",
      "client_token": "string"
    }
  },
  
  "code_signing": {
    "ios_method": "match | manual | automatic",
    "match": {
      "git_url": "string",
      "storage_mode": "git | s3 | google_cloud",
      "type": "appstore | adhoc | all"
    },
    "android": {
      "keystore_path": "string",
      "key_alias": "string"
    }
  },
  
  "cicd": {
    "github_repo": "string (owner/repo)",
    "use_self_hosted": "boolean",
    "runner": {
      "labels": ["string"],
      "xcode_version": "string"
    },
    "triggers": {
      "build_on_pr": "boolean",
      "deploy_on_merge": "boolean",
      "deploy_on_tag": "boolean"
    }
  },
  
  "aws": {
    "region": "string",
    "api_gateway_id": "string"
  },
  
  "cloudflare": {
    "zone_id": "string",
    "domain": "string"
  }
}
```

---

## CI/CD Pipeline Deep Dive

### Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DEVELOPMENT                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Developer                                                              │
│      │                                                                   │
│      ▼                                                                   │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                       │
│   │  Commit  │────▶│   Push   │────▶│   PR     │                       │
│   └──────────┘     └──────────┘     └──────────┘                       │
│                                           │                              │
└───────────────────────────────────────────┼──────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CI PIPELINE (ci.yml)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐      │
│   │ Checkout │────▶│ Analyze  │────▶│   Test   │────▶│  Build   │      │
│   └──────────┘     └──────────┘     └──────────┘     └──────────┘      │
│                                                             │            │
│                                                             ▼            │
│                                                      ┌──────────┐       │
│                                                      │ Artifacts│       │
│                                                      └──────────┘       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │ Merge to main
                                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        CD PIPELINE (cd.yml)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐      │
│   │  Setup   │────▶│  Build   │────▶│   Sign   │────▶│  Upload  │      │
│   └──────────┘     └──────────┘     └──────────┘     └──────────┘      │
│        │                                                    │            │
│        ▼                                                    ▼            │
│   ┌──────────┐                                       ┌──────────┐       │
│   │ Version  │                                       │TestFlight│       │
│   │ + Build# │                                       │Play Store│       │
│   └──────────┘                                       │ Internal │       │
│                                                      └──────────┘       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                            │
                                            │ Create Release
                                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     RELEASE PIPELINE (release.yml)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐      │
│   │  Build   │────▶│   Sign   │────▶│  Upload  │────▶│  Submit  │      │
│   │   Prod   │     │   Prod   │     │  Stores  │     │  Review  │      │
│   └──────────┘     └──────────┘     └──────────┘     └──────────┘      │
│                                                             │            │
│                                                             ▼            │
│                                                      ┌──────────┐       │
│                                                      │App Store │       │
│                                                      │Play Store│       │
│                                                      └──────────┘       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Build Number Strategy

```yaml
# Automatic build number generation
BUILD_NUMBER=$(date +%Y%m%d%H%M)
# Example: 202401151430

# Or use GitHub run number
BUILD_NUMBER=${{ github.run_number }}
```

### Version Tagging

```bash
# Create version tag
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# This triggers:
# 1. CD workflow (deploy to staging)
# 2. Create GitHub Release for production
```

---

## Troubleshooting

### Common Issues

#### 1. Match Certificate Errors

```
Error: Could not find a valid signing identity
```

**Solution:**
```bash
# Re-sync certificates
cd ios
bundle exec fastlane match nuke development
bundle exec fastlane match nuke distribution
bundle exec fastlane match development
bundle exec fastlane match appstore
```

#### 2. Android Build Failures

```
Error: Could not read key from keystore
```

**Solution:**
```bash
# Verify keystore
keytool -list -v -keystore release.keystore

# Check environment variables
echo $KEYSTORE_PASSWORD
echo $KEY_PASSWORD
```

#### 3. Runner Not Picking Up Jobs

```
Warning: Runner is offline
```

**Solution:**
```bash
# SSH to Mac Mini
ssh user@mac-mini

# Check runner status
~/runner-manage.sh status

# Restart if needed
~/runner-manage.sh restart

# Check logs
~/runner-manage.sh logs
```

#### 4. Xcode Version Mismatch

```
Error: The requested Xcode version is not available
```

**Solution:**
```bash
# List installed Xcode versions
ls /Applications | grep Xcode

# Switch Xcode version
sudo xcode-select -s /Applications/Xcode_15.2.app

# In workflow, specify version
- uses: maxim-lobanov/setup-xcode@v1
  with:
    xcode-version: '15.2'
```

#### 5. Flutter Build Cache Issues

```
Error: Gradle build failed
```

**Solution:**
```bash
# Clean Flutter
flutter clean
flutter pub get

# Clean Gradle
cd android
./gradlew clean

# Clean iOS
cd ios
rm -rf Pods Podfile.lock
pod install
```

### Debug Mode

Enable verbose logging in workflows:

```yaml
env:
  FASTLANE_LOG_LEVEL: debug
  FL_OUTPUT_DIR: output
  VERBOSE: true
```

### Log Locations

| Component | Log Location |
|-----------|-------------|
| GitHub Actions | GitHub UI → Actions → Workflow run |
| Fastlane | `ios/fastlane/logs/` or `android/fastlane/logs/` |
| Runner | `~/actions-runner/_diag/` |
| Xcode | `~/Library/Logs/DiagnosticReports/` |

---

## Best Practices

### 1. Security

- ✅ Use GitHub Secrets for all credentials
- ✅ Enable branch protection on main
- ✅ Require PR reviews
- ✅ Use separate Firebase projects per environment
- ✅ Rotate credentials regularly
- ❌ Never commit secrets to repository
- ❌ Never hardcode API keys

### 2. Versioning

```bash
# Semantic versioning
MAJOR.MINOR.PATCH+BUILD
1.2.3+456

# Version in pubspec.yaml
version: 1.2.3+456
```

### 3. Branch Strategy

```
main (production)
  │
  ├── develop (staging)
  │     │
  │     ├── feature/new-feature
  │     ├── feature/another-feature
  │     └── bugfix/fix-issue
  │
  └── hotfix/critical-fix
```

### 4. Testing

- Run tests locally before pushing
- Maintain > 80% code coverage
- Include integration tests
- Test on real devices periodically

### 5. Monitoring

- Enable Crashlytics for crash reporting
- Use Analytics for usage tracking
- Set up alerts for build failures
- Monitor runner health

### 6. Documentation

- Keep README updated
- Document custom configurations
- Maintain CHANGELOG
- Comment complex code

---

## FAQ

### General

**Q: How long does the initial setup take?**

A: About 30-60 minutes for the first run, depending on your familiarity with the tools and whether you have all accounts ready.

**Q: Can I use this for existing projects?**

A: Yes! The CLI analyzes your existing project and generates configurations accordingly.

**Q: Does it work with Flutter web?**

A: Currently focused on iOS and Android. Web deployment may be added in future versions.

### iOS

**Q: Do I need a Mac for iOS builds?**

A: Yes, Xcode only runs on macOS. Either use a Mac Mini runner or GitHub's macOS runners.

**Q: How do I handle multiple apps with the same bundle ID prefix?**

A: Use Match with multiple app identifiers:
```ruby
app_identifier(["com.example.app", "com.example.app.widget"])
```

### Android

**Q: Should I use Google-managed signing or upload key?**

A: Google-managed is recommended for new apps. It's more secure and allows key recovery.

**Q: How do I handle 64-bit requirements?**

A: Flutter handles this automatically. Both arm64-v8a and armeabi-v7a are included.

### CI/CD

**Q: How many GitHub Actions minutes do I get?**

A: Free tier: 2,000 minutes/month (3,000 for Pro). Self-hosted runners have unlimited minutes.

**Q: Can I use this with GitLab CI or Bitrise?**

A: Currently generates GitHub Actions workflows. Similar concepts apply to other CI systems.

### Runner

**Q: Can I use a cloud Mac instead of Mac Mini?**

A: Yes, services like MacStadium, AWS EC2 Mac, or GitHub's larger macOS runners work.

**Q: How do I handle multiple projects on one runner?**

A: Runners can handle multiple repositories. Use labels to target specific runners if needed.

---

## Contributing

We welcome contributions! Here's how to help:

### Reporting Issues

1. Check existing issues first
2. Include Flutter doctor output
3. Include relevant logs
4. Describe steps to reproduce

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/flutter-deploy-cli.git
cd flutter-deploy-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

---

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

## Support

- **Documentation**: This guide
- **Issues**: [GitHub Issues](https://github.com/your-org/flutter-deploy-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/flutter-deploy-cli/discussions)

---

<p align="center">
  <b>Built with ❤️ for Flutter developers</b>
  <br>
  <sub>Making deployment as beautiful as your apps</sub>
</p>
