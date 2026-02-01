# Porcupine Wake Word Setup

## Overview

Picovoice Porcupine provides on-device wake word detection. No cloud dependency, low latency (50-200ms), power-efficient.

## Installation

### Unity Package

1. Download Porcupine Unity SDK from Picovoice Console
2. Import the `.unitypackage` into your project
3. Or install via Package Manager with the Picovoice registry

### Access Key

1. Create account at https://console.picovoice.ai
2. Generate an Access Key
3. Store in environment variable: `PICOVOICE_KEY`

## Custom Wake Word

### Using Picovoice Console

1. Go to https://console.picovoice.ai
2. Navigate to Porcupine > Custom Keywords
3. Create keyword: "Hey Claude"
4. Train for Android platform
5. Download `.ppn` model file
6. Place in `Assets/StreamingAssets/porcupine/`

### Built-in Keywords

Porcupine ships with built-in keywords for testing:
- "Alexa", "Hey Google", "Computer", "Jarvis", etc.
- Use for prototyping before creating custom "Hey Claude" keyword

## Unity Integration

### Basic Setup

```csharp
using Pv.Unity;

public class WakeWordListener : MonoBehaviour {
    private PorcupineManager porcupine;

    void Start() {
        try {
            porcupine = PorcupineManager.FromKeywordPaths(
                accessKey: Environment.GetEnvironmentVariable("PICOVOICE_KEY"),
                keywordPaths: new string[] {
                    Path.Combine(Application.streamingAssetsPath,
                        "porcupine/hey-claude_en_android.ppn")
                },
                wakeWordCallback: OnWakeWordDetected,
                sensitivities: new float[] { 0.7f }  // 0.0 to 1.0
            );
            porcupine.Start();
        } catch (PorcupineException e) {
            Debug.LogError($"Porcupine init failed: {e.Message}");
        }
    }

    void OnWakeWordDetected(int keywordIndex) {
        Debug.Log("Wake word detected - starting voice capture");
        // Trigger voice pipeline
        GetComponent<VoiceCapture>().StartListening();
    }

    void OnDestroy() {
        porcupine?.Stop();
        porcupine?.Delete();
    }
}
```

### Sensitivity Tuning

```csharp
// Higher sensitivity = more detections (more false positives)
// Lower sensitivity = fewer detections (more false negatives)
sensitivities: new float[] { 0.7f }  // Recommended starting point

// Noisy VR environment: lower sensitivity to reduce false triggers
sensitivities: new float[] { 0.5f }

// Quiet environment: higher sensitivity for better detection
sensitivities: new float[] { 0.85f }
```

## Quest-Specific Notes

### Android Compatibility

- Porcupine supports Android (Quest's base OS)
- Quest is NOT explicitly certified by Picovoice
- Android ARM64 builds work (IL2CPP compatible)
- Contact Picovoice for official Quest verification

### Microphone Access

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

### Runtime Permission Request

```csharp
#if UNITY_ANDROID && !UNITY_EDITOR
if (!Permission.HasUserAuthorizedPermission(Permission.Microphone)) {
    Permission.RequestUserPermission(Permission.Microphone);
}
#endif
```

### Power Efficiency

- Porcupine runs lightweight DSP on audio frames
- Minimal CPU impact (suitable for VR frame budget)
- Only activates full voice pipeline on wake word detection
- Battery-friendly for extended VR sessions

## Fallback Strategy

If Porcupine has issues on Quest:
1. **Push-to-talk** via controller trigger (always works)
2. **Meta Voice SDK (Wit.ai)** — fully Quest-compatible but cloud-based
3. **Keyword spotting** via Unity's built-in Microphone API (custom implementation)

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No detections | Sensitivity too low | Increase to 0.8+ |
| False triggers | Sensitivity too high | Decrease to 0.5 |
| Crash on init | Missing access key | Set PICOVOICE_KEY env var |
| No microphone | Permission denied | Request RECORD_AUDIO permission |
| Model not found | Wrong path | Check StreamingAssets path on Android |
