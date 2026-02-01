# Deepgram STT Integration

## Overview

Deepgram provides streaming speech-to-text via WebSocket with sub-300ms latency. Audio streams in 100-200ms chunks for real-time transcription.

## WebSocket Connection

### Endpoint

```
wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1
```

### Query Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| encoding | linear16 | 16-bit PCM audio |
| sample_rate | 16000 | 16kHz sample rate |
| channels | 1 | Mono audio |
| model | nova-2 | Latest model (best accuracy) |
| language | en | Language code |
| punctuate | true | Add punctuation |
| interim_results | true | Get partial transcriptions |
| endpointing | 300 | Silence endpoint in ms |

### Full URL

```
wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1&model=nova-2&language=en&punctuate=true&interim_results=true&endpointing=300
```

## NativeWebSocket Implementation

### Connection

```csharp
using NativeWebSocket;

WebSocket deepgramWs;

async Task ConnectDeepgram() {
    string url = "wss://api.deepgram.com/v1/listen?" +
        "encoding=linear16&sample_rate=16000&channels=1" +
        "&model=nova-2&punctuate=true&interim_results=true";

    deepgramWs = new WebSocket(url, new Dictionary<string, string> {
        { "Authorization", $"Token {Environment.GetEnvironmentVariable("DEEPGRAM_KEY")}" }
    });

    deepgramWs.OnOpen += () => Debug.Log("Deepgram connected");

    deepgramWs.OnMessage += (bytes) => {
        string json = System.Text.Encoding.UTF8.GetString(bytes);
        HandleTranscription(json);
    };

    deepgramWs.OnError += (error) => Debug.LogError($"Deepgram error: {error}");
    deepgramWs.OnClose += (code) => Debug.Log($"Deepgram closed: {code}");

    await deepgramWs.Connect();
}
```

### Audio Streaming

```csharp
AudioClip micClip;
int lastSample = 0;

void StartMicrophone() {
    micClip = Microphone.Start(null, true, 10, 16000);
}

void StreamAudio() {
    int currentPos = Microphone.GetPosition(null);
    if (currentPos == lastSample) return;

    int sampleCount;
    if (currentPos > lastSample) {
        sampleCount = currentPos - lastSample;
    } else {
        sampleCount = (micClip.samples - lastSample) + currentPos;
    }

    float[] samples = new float[sampleCount];
    micClip.GetData(samples, lastSample);
    lastSample = currentPos;

    // Convert to 16-bit PCM
    byte[] pcm = new byte[samples.Length * 2];
    for (int i = 0; i < samples.Length; i++) {
        short val = (short)(Mathf.Clamp(samples[i], -1f, 1f) * short.MaxValue);
        pcm[i * 2] = (byte)(val & 0xFF);
        pcm[i * 2 + 1] = (byte)((val >> 8) & 0xFF);
    }

    deepgramWs.Send(pcm);
}

void Update() {
    deepgramWs?.DispatchMessageQueue();  // Required for NativeWebSocket
    if (isListening) StreamAudio();
}
```

### Handling Transcription Results

```csharp
[System.Serializable]
class DeepgramResponse {
    public string type;
    public DeepgramChannel channel;
    public bool is_final;
}

[System.Serializable]
class DeepgramChannel {
    public DeepgramAlternative[] alternatives;
}

[System.Serializable]
class DeepgramAlternative {
    public string transcript;
    public float confidence;
}

void HandleTranscription(string json) {
    var response = JsonUtility.FromJson<DeepgramResponse>(json);

    if (response.channel?.alternatives?.Length > 0) {
        string text = response.channel.alternatives[0].transcript;
        float confidence = response.channel.alternatives[0].confidence;

        if (response.is_final && !string.IsNullOrEmpty(text)) {
            Debug.Log($"Final: {text} ({confidence:P0})");
            ProcessVoiceCommand(text);
        } else if (!string.IsNullOrEmpty(text)) {
            // Interim result — show in UI for feedback
            UpdateInterimDisplay(text);
        }
    }
}
```

### Closing Connection

```csharp
async Task StopListening() {
    Microphone.End(null);

    // Send empty byte array to signal end of audio
    await deepgramWs.Send(new byte[0]);

    await deepgramWs.Close();
}
```

## Latency Optimization

| Technique | Impact |
|-----------|--------|
| Use `interim_results=true` | Show partial text immediately |
| Stream small chunks (100-200ms) | Reduce per-chunk latency |
| Use `endpointing=300` | Detect speech end faster |
| Use `nova-2` model | Best accuracy/speed balance |
| Keep WebSocket open | Avoid reconnection overhead |

## Error Handling

```csharp
deepgramWs.OnError += (error) => {
    Debug.LogError($"Deepgram WebSocket error: {error}");
    // Attempt reconnection
    StartCoroutine(ReconnectAfterDelay(2f));
};

deepgramWs.OnClose += (code) => {
    if (code != WebSocketCloseCode.Normal) {
        Debug.LogWarning($"Unexpected close: {code}");
        StartCoroutine(ReconnectAfterDelay(1f));
    }
};
```

## Quest-Specific Notes

- NativeWebSocket works on Android (Quest base OS)
- Some connectivity issues reported on Quest 2/3 — test thoroughly
- Ensure `INTERNET` permission in AndroidManifest.xml
- `DispatchMessageQueue()` must be called in `Update()` on Quest
