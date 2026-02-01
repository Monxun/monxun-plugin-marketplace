---
name: flutter-firebase-deploy:configure-firebase
description: Configure Firebase for a Flutter project. Sets up FlutterFire CLI, generates config files, and initializes Firebase in the app.
---

# Configure Firebase

Set up Firebase integration for the Flutter project.

## Usage

```
/flutter-firebase-deploy:configure-firebase [project-id]
```

## Arguments

- `project-id` - Firebase project ID

## What This Does

1. Installs FlutterFire CLI
2. Runs `flutterfire configure`
3. Generates platform config files
4. Updates main.dart with Firebase initialization
5. Validates configuration

## Prerequisites

- Firebase project created in Firebase Console
- Firebase CLI installed and logged in
- Flutter project initialized

## Example

```
/flutter-firebase-deploy:configure-firebase my-firebase-project
```
