# IL2CPP Optimization Guide

## Build Size Reduction

### Managed Code Stripping

```csharp
// In Player Settings
PlayerSettings.stripEngineCode = true;
```

Stripping levels (Project Settings > Player > Other Settings):
- **Minimal**: Remove unreachable managed code
- **Low**: Remove most unreachable code
- **Medium**: Remove more aggressively (recommended for Quest)
- **High**: Maximum stripping (test thoroughly)

### link.xml Preservation

When stripping removes code needed at runtime (especially reflection-based):

```xml
<linker>
  <!-- Preserve entire assembly -->
  <assembly fullname="MyGameplay" preserve="all"/>

  <!-- Preserve specific type -->
  <assembly fullname="MyPlugins">
    <type fullname="MyPlugins.McpTools" preserve="all"/>
  </assembly>

  <!-- Preserve by namespace -->
  <assembly fullname="ThirdParty">
    <namespace fullname="ThirdParty.MCP" preserve="all"/>
  </assembly>
</linker>
```

Place `link.xml` in `Assets/` directory.

### Assembly Definitions

Use Assembly Definitions (.asmdef) to:
- Reduce recompilation scope during development
- Enable selective stripping per assembly
- Improve incremental build times

```json
{
  "name": "VR.Interactions",
  "references": [
    "Unity.XR.Interaction.Toolkit",
    "Unity.InputSystem"
  ],
  "includePlatforms": ["Android"],
  "allowUnsafeCode": false
}
```

## Build Speed Optimization

### Incremental IL2CPP

Unity caches IL2CPP output between builds. To benefit:
- Don't clean the `Library/` folder between builds
- Use the same build output directory
- Keep `Library/Il2cppBuildCache/` intact

### Build Cache Location

```
Library/Il2cppBuildCache/     # C++ compilation cache
Library/Bee/                   # Build system cache
Temp/gradleOut/               # Gradle build cache
```

### Parallel Compilation

```
# Unity Editor preferences
Preferences > External Tools > IL2CPP C++ Compiler Configuration
  - Debug: Fastest builds, no optimization
  - Release: Balanced speed and optimization
  - Master: Full optimization, slowest builds
```

For development, use **Debug** or **Release** configuration.

## APK Size Analysis

### Build Report

```csharp
// After build, check the report
var report = BuildReport.GetLatestReport();
Debug.Log($"Total size: {report.summary.totalSize}");
foreach (var step in report.steps) {
    Debug.Log($"{step.name}: {step.duration}");
}
```

### Common Size Offenders

| Asset Type | Typical Size | Optimization |
|-----------|-------------|-------------|
| Textures | 40-60% | Compress with ASTC, reduce resolution |
| Audio | 10-20% | Vorbis compression, mono for SFX |
| Meshes | 10-15% | Mesh compression, LODs |
| Scripts (IL2CPP) | 5-15% | Code stripping, assembly defs |
| Shaders | 5-10% | Strip unused variants |

### Texture Compression

Quest 2 supports ASTC natively:

```
Texture Import Settings:
  Override for Android: Yes
  Format: ASTC 6x6 (good quality/size balance)
  Compressor Quality: Best
```

## Runtime Performance

### Ahead-of-Time Compilation

IL2CPP converts all C# to C++ and compiles ahead of time. This means:
- No JIT compilation overhead at runtime
- Predictable performance without JIT warmup
- Generic types fully expanded at compile time
- Virtual method dispatch optimized

### Generic Sharing

IL2CPP shares generic implementations where possible. For best results:
- Prefer reference type generics (shared implementation)
- Value type generics create separate implementations (larger binary)
- Avoid excessive generic type variations
