---
name: voice-pipeline
description: |
  In-VR voice interaction pipeline for hands-free development.
  Use when: voice commands, wake word detection, speech-to-text,
  Porcupine setup, Deepgram STT, NativeWebSocket, spatial audio,
  "Hey Claude", microphone, TTS, voice setup, Claude API voice.
  Supports: push-to-talk, wake word, streaming STT, SSE responses.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
---

# Voice Pipeline

Configure the in-VR voice interaction pipeline: Wake Word → STT → Claude API → TTS with spatial audio.

## Pipeline Architecture

```
User speaks → Porcupine Wake Word (on-device, 50-200ms)
  → Deepgram STT (WebSocket streaming, 100-500ms)
    → Claude API (SSE streaming, 350ms-1s+)
      → TTS (speculative processing, 75-200ms)
        → Spatial Audio Output (3D positioned)
```

**Total latency**: 600ms-2s (acceptable for VR assistance)

## Components

| Stage | Technology | Latency | Location |
|-------|-----------|---------|----------|
| Wake Word | Picovoice Porcupine | 50-200ms | On-device |
| Push-to-Talk | OVRInput trigger | Immediate | On-device |
| Speech-to-Text | Deepgram WebSocket | 100-500ms | Cloud |
| LLM Processing | Claude API (SSE) | 350ms-1s+ | Cloud |
| Text-to-Speech | Deepgram TTS | 75-200ms | Cloud |
| Audio Output | Unity Spatial Audio | <10ms | On-device |

## Wake Word Detection

### Picovoice Porcupine

On-device processing — no cloud dependency, low latency, power-efficient.

```csharp
using Pv.Unity;

PorcupineManager porcupine;

void Start() {
    porcupine = PorcupineManager.FromKeywordPaths(
        accessKey: Environment.GetEnvironmentVariable("PICOVOICE_KEY"),
        keywordPaths: new string[] { "hey-claude_en_android.ppn" },
        wakeWordCallback: OnWakeWord
    );
    porcupine.Start();
}

void OnWakeWord(int keywordIndex) {
    Debug.Log("Wake word detected!");
    StartListening();
}

void OnDestroy() {
    porcupine?.Stop();
    porcupine?.Delete();
}
```

**Quest compatibility**: Porcupine supports Android (Quest's base OS). Not explicitly Quest-certified — verify with Picovoice.

### Push-to-Talk Alternative

```csharp
void Update() {
    // Right trigger for push-to-talk
    if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch)) {
        StartListening();
    }
    if (OVRInput.GetUp(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch)) {
        StopListening();
    }
}
```

## Speech-to-Text (Deepgram)

### WebSocket Streaming via NativeWebSocket

```csharp
using NativeWebSocket;

WebSocket ws;

async void StartListening() {
    ws = new WebSocket(
        "wss://api.deepgram.com/v1/listen?" +
        "encoding=linear16&sample_rate=16000&channels=1",
        new Dictionary<string, string> {
            { "Authorization", $"Token {Environment.GetEnvironmentVariable("DEEPGRAM_KEY")}" }
        }
    );

    ws.OnMessage += (bytes) => {
        string json = System.Text.Encoding.UTF8.GetString(bytes);
        ProcessTranscription(json);
    };

    await ws.Connect();
    StartMicrophoneCapture();
}

void Update() {
    // Required for NativeWebSocket on Quest
    ws?.DispatchMessageQueue();
}
```

### Audio Streaming

```csharp
void StreamAudioChunk(float[] samples) {
    // Convert float PCM to 16-bit PCM bytes
    byte[] pcmBytes = new byte[samples.Length * 2];
    for (int i = 0; i < samples.Length; i++) {
        short val = (short)(samples[i] * short.MaxValue);
        pcmBytes[i * 2] = (byte)(val & 0xFF);
        pcmBytes[i * 2 + 1] = (byte)((val >> 8) & 0xFF);
    }
    ws.Send(pcmBytes);  // Stream 100-200ms chunks
}
```

**Note**: NativeWebSocket has reported connectivity issues on some Quest devices. Test thoroughly.

## Claude API Integration

### SSE Streaming via Claude-Unity

```csharp
using ClaudeUnity;

async void ProcessVoiceCommand(string transcription) {
    var client = new ClaudeClient(
        apiKey: Environment.GetEnvironmentVariable("CLAUDE_API_KEY")
    );

    // Stream responses for lower perceived latency
    await client.StreamMessageAsync(
        model: "claude-sonnet-4-20250514",
        messages: new[] {
            new Message("user", transcription)
        },
        onPartialResponse: (partial) => {
            // Begin TTS on partial response (speculative processing)
            QueueTTSChunk(partial);
        },
        onComplete: (response) => {
            Debug.Log($"Full response: {response}");
        }
    );
}
```

**IL2CPP compatible**: Claude-Unity verified working with both IL2CPP and Mono backends.

## Text-to-Speech

### Spatial Audio Output

```csharp
void PlaySpatialTTS(AudioClip clip, Vector3 sourcePosition) {
    var audioSource = GetComponent<AudioSource>();
    audioSource.spatialBlend = 1.0f;  // Full 3D
    audioSource.transform.position = sourcePosition;
    audioSource.clip = clip;
    audioSource.Play();
}
```

### Speculative Processing

Start TTS before Claude finishes generating the full response:

1. Receive partial SSE response from Claude
2. Send sentence-boundary text to TTS API
3. Queue audio clips for sequential playback
4. Continue receiving and processing in parallel

This reduces perceived latency by 200-500ms.

## API Keys

All API keys must be stored securely:

```bash
# Environment variables (never commit to source)
export PICOVOICE_KEY="your-picovoice-access-key"
export DEEPGRAM_KEY="your-deepgram-api-key"
export CLAUDE_API_KEY="your-claude-api-key"
```

**Unity Android Manifest** — Requires internet permission:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

## Protocol Constraints

- **No gRPC** — IL2CPP ARM64 linking errors (`undefined symbol: grpcsharp_init`)
- **Use NativeWebSocket** — Open-source, no external DLLs, Quest compatible
- **HTTP/WebSocket only** — All cloud APIs accessed via REST or WebSocket

## References

- `references/porcupine-setup.md` — Wake word model setup and configuration
- `references/deepgram-integration.md` — Deepgram API streaming details
- `references/spatial-audio.md` — Unity spatial audio for TTS output
