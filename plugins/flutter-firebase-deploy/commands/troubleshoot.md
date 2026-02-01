---
name: flutter-firebase-deploy:troubleshoot
description: Diagnose and fix common Flutter Firebase deployment issues. Provides solutions for build, signing, and deployment errors.
---

# Troubleshoot

Diagnose and resolve deployment issues.

## Usage

```
/flutter-firebase-deploy:troubleshoot [error-message]
```

## Arguments

- `error-message` - Optional error message to diagnose

## Common Issues Diagnosed

### Build Errors
- CocoaPods conflicts
- Gradle failures
- SDK version mismatches

### Signing Errors
- Certificate issues
- Provisioning profile problems
- Keystore errors

### Deployment Errors
- App Store rejections
- Play Store failures
- API authentication issues

## What This Does

1. Analyzes error message or logs
2. Identifies root cause
3. Suggests specific fixes
4. Optionally applies fixes
5. Verifies resolution

## Example

```
/flutter-firebase-deploy:troubleshoot "No signing certificate found"
```
