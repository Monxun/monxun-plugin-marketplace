# Unity API Reference for MCP Tools

## Scene Operations

### EditorSceneManager

```csharp
// Get active scene
Scene scene = EditorSceneManager.GetActiveScene();

// Save scene
EditorSceneManager.SaveScene(scene);

// Create new scene
Scene newScene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects);
```

### GameObject Creation

```csharp
// Create empty
var go = new GameObject("MyObject");

// Create primitive
var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);

// Instantiate prefab
var instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
```

### Component Management

```csharp
// Add component
var rb = go.AddComponent<Rigidbody>();

// Get component
var collider = go.GetComponent<Collider>();

// Configure XR Grab Interactable
var grab = go.AddComponent<XRGrabInteractable>();
grab.movementType = XRBaseInteractable.MovementType.VelocityTracking;
grab.throwOnDetach = true;
```

## XR Interaction Toolkit Components

### XRGrabInteractable

```csharp
var grab = go.AddComponent<XRGrabInteractable>();
grab.movementType = XRBaseInteractable.MovementType.VelocityTracking;
grab.throwOnDetach = true;
grab.smoothPosition = true;
grab.smoothRotation = true;
grab.tightenPosition = 0.5f;
grab.tightenRotation = 0.5f;
```

### XRSocketInteractor

```csharp
var socket = go.AddComponent<XRSocketInteractor>();
socket.showInteractableHoverMeshes = true;
socket.recycleDelayTime = 1f;
```

### XRRayInteractor

```csharp
var ray = go.AddComponent<XRRayInteractor>();
ray.maxRaycastDistance = 10f;
ray.enableUIInteraction = true;
```

## Asset Management

### AssetDatabase

```csharp
// Import asset
AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);

// Create material
var mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
AssetDatabase.CreateAsset(mat, "Assets/Materials/NewMaterial.mat");

// Refresh database
AssetDatabase.Refresh();
```

### PrefabUtility

```csharp
// Save as prefab
PrefabUtility.SaveAsPrefabAsset(go, "Assets/Prefabs/MyPrefab.prefab");

// Unpack prefab
PrefabUtility.UnpackPrefabInstance(go, PrefabUnpackMode.Completely, InteractionMode.AutomatedAction);
```

### AssetBundle Building

```csharp
AssetBundleBuild[] builds = new AssetBundleBuild[1];
builds[0].assetBundleName = "scene-bundle";
builds[0].assetNames = new string[] { "Assets/Scenes/MyScene.unity" };

BuildPipeline.BuildAssetBundles(
    "Assets/StreamingAssets/Bundles",
    builds,
    BuildAssetBundleOptions.ChunkBasedCompression,
    BuildTarget.Android
);
```

## Build Pipeline

### BuildPlayerOptions

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
```

### Quest-Specific Settings

```csharp
// Required for Quest
PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;

// Graphics
PlayerSettings.colorSpace = ColorSpace.Linear;
PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, new[] { GraphicsDeviceType.OpenGLES3 });

// XR
PlayerSettings.Android.minSdkVersion = AndroidSdkVersions.AndroidApiLevel29;
PlayerSettings.Android.targetSdkVersion = AndroidSdkVersions.AndroidApiLevelAuto;
```

## Test APIs

### TestRunnerApi

```csharp
var testRunnerApi = ScriptableObject.CreateInstance<TestRunnerApi>();
testRunnerApi.Execute(new ExecutionSettings {
    filter = new Filter {
        testMode = TestMode.PlayMode,
        categoryNames = new[] { "VR" }
    }
});
```

### Performance Testing

```csharp
[Test, Performance]
public void FrameBudget_MeetsTarget()
{
    Measure.Frames()
        .WarmupCount(30)
        .MeasurementCount(120)
        .ProfilerMarkers("XR.WaitForGPU")
        .Run();
}
```

## Thread Safety Pattern

```csharp
// All MCP tool implementations must wrap Unity calls:
public string MyTool(string param) {
    return MainThread.Instance.Run(() => {
        // Safe to call Unity APIs here
        var go = new GameObject(param);
        return $"Created {go.name}";
    });
}

// Async variant for long operations:
public async Task<string> MyAsyncTool(string param) {
    return await MainThread.Instance.RunAsync(() => {
        // Long-running Unity operation
        AssetDatabase.Refresh();
        return "Done";
    });
}
```
