---
name: quest-build-automation
description: |
  Quest 2/3/Pro build automation with IL2CPP and Gradle optimization.
  Use when: building APK, IL2CPP compilation, ARM64 builds, Gradle caching,
  deploy to Quest, ADB install, keystore management, asset bundles,
  "build for Quest", "deploy APK", incremental builds, hot-reload.
  Supports: Unity 2022.3-Unity 6, Meta XR SDK v74+, signed APKs.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Quest Build Automation

Automate IL2CPP ARM64 builds for Meta Quest with Gradle caching, keystore management, and ADB deployment.

## Hard Constraints

| Constraint | Value | Impact |
|-----------|-------|--------|
| Scripting Backend | IL2CPP | No C# hot-reload on device |
| Architecture | ARM64 | ARMv7/Mono not supported |
| Graphics API | OpenGL ES 3.0 | Vulkan also supported |
| Color Space | Linear | Requires GLES 3.0 or Vulkan |
| Min SDK | Android API 29 | Quest 2 minimum |

## Build Configuration

### Required Player Settings

```csharp
// Scripting
PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;

// Graphics
PlayerSettings.colorSpace = ColorSpace.Linear;
PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new[] { GraphicsDeviceType.OpenGLES3 });

// Android
PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel29;
PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;

// Build system
EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;
```

### Build Command

```csharp
BuildPlayerOptions options = new BuildPlayerOptions {
    scenes = EditorBuildSettings.scenes
        .Where(s => s.enabled)
        .Select(s => s.path).ToArray(),
    locationPathName = "Builds/QuestApp.apk",
    target = BuildTarget.Android,
    targetGroup = BuildTargetGroup.Android,
    options = BuildOptions.None
};
BuildPipeline.BuildPlayer(options);
```

### Unity CLI Build

```bash
# Headless build from command line
Unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -executeMethod BuildScript.BuildQuest \
  -logFile build.log
```

## Gradle Caching

Gradle caching reduces incremental build times by 30-50%.

### Enable Caching

In `Preferences > External Tools`:
- Check "Export Project" for manual Gradle builds
- Or use embedded Gradle with cache enabled

### Gradle Properties

```properties
# gradle.properties (in exported project)
org.gradle.caching=true
org.gradle.parallel=true
org.gradle.daemon=true
android.enableBuildCache=true
```

### Cache Location

```bash
# Default cache directory
~/.gradle/caches/

# Clear cache if builds are inconsistent
rm -rf ~/.gradle/caches/build-cache-*
```

See `references/gradle-caching.md` for advanced cache optimization.

## ADB Deployment

### Install and Launch

```bash
# Install APK (replace existing)
adb install -r Builds/QuestApp.apk

# Launch application
adb shell am start -n com.company.app/com.unity3d.player.UnityPlayerActivity

# Combined install and launch
adb install -r Builds/QuestApp.apk && \
adb shell am start -n com.company.app/com.unity3d.player.UnityPlayerActivity
```

### Wireless ADB

```bash
# Setup (with USB connected)
adb tcpip 5555
adb connect <quest-ip>:5555

# Verify
adb devices
```

### Uninstall

```bash
adb uninstall com.company.app
```

## Keystore Management

### Create Keystore

```bash
keytool -genkey -v \
  -keystore quest-release.keystore \
  -alias quest-key \
  -keyalg RSA -keysize 2048 \
  -validity 10000
```

### Configure in Unity

```csharp
PlayerSettings.Android.useCustomKeystore = true;
PlayerSettings.Android.keystoreName = "path/to/quest-release.keystore";
PlayerSettings.Android.keystorePass = Environment.GetEnvironmentVariable("KEYSTORE_PASS");
PlayerSettings.Android.keyaliasName = "quest-key";
PlayerSettings.Android.keyaliasPass = Environment.GetEnvironmentVariable("KEY_PASS");
```

**Security**: Store passwords in environment variables or credential manager. Never commit to source control.

See `references/keystore-management.md` for CI/CD keystore handling.

## Hot-Reload Strategy

IL2CPP eliminates C# hot-reload on device. Use layered iteration:

| Layer | Strategy | Speed |
|-------|----------|-------|
| Editor | Hot Reload plugins (Mono in Editor) | Milliseconds |
| Content | Asset bundle streaming | Seconds |
| Device | Gradle-cached incremental build | 30-50% faster |
| Full | Clean IL2CPP build | Minutes |

### Asset Bundle Hot-Reload

```csharp
// Build bundles for Android
BuildPipeline.BuildAssetBundles(
    "Assets/StreamingAssets/Bundles",
    BuildAssetBundleOptions.ChunkBasedCompression,
    BuildTarget.Android
);
```

```bash
# Push updated bundle to device
adb push Assets/StreamingAssets/Bundles/scene-bundle \
  /sdcard/Android/data/com.company.app/files/Bundles/

# Trigger reload via MCP tool
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"reload-bundles"},"id":1}'
```

## Build Variants

### Development Build

```csharp
options.options = BuildOptions.Development |
                  BuildOptions.AllowDebugging |
                  BuildOptions.ConnectWithProfiler;
```

### Release Build

```csharp
options.options = BuildOptions.None;
// Ensure keystore is configured
// Enable code stripping for smaller APK
PlayerSettings.stripEngineCode = true;
```

## References

- `references/il2cpp-optimization.md` — IL2CPP build size and speed optimization
- `references/gradle-caching.md` — Advanced Gradle cache configuration
- `references/keystore-management.md` — Keystore creation, backup, CI/CD usage
