---
name: flutter-firebase-deploy:validate-config
description: Validate all deployment configurations. Checks Firebase, signing, Fastlane, and CI/CD setup for deployment readiness.
---

# Validate Configuration

Comprehensive validation of deployment configuration.

## Usage

```
/flutter-firebase-deploy:validate-config [--fix]
```

## Options

- `--fix` - Attempt to automatically fix issues

## Validation Checks

### Flutter
- [ ] Flutter doctor passes
- [ ] No analyzer warnings
- [ ] Tests pass

### Firebase
- [ ] Config files present
- [ ] Package names match
- [ ] SHA fingerprints configured

### Signing
- [ ] iOS certificates valid
- [ ] Android keystore accessible
- [ ] Match configured

### Fastlane
- [ ] Lanes defined
- [ ] Credentials configured

### CI/CD
- [ ] Workflow files valid
- [ ] Secrets documented

## Example

```
/flutter-firebase-deploy:validate-config --fix
```
