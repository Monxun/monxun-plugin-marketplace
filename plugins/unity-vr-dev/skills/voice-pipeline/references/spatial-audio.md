# Spatial Audio for TTS Output

## Overview

TTS responses are positioned in 3D space so the AI assistant "speaks from" a consistent location in the VR environment.

## AudioSource Configuration

### Basic Spatial Setup

```csharp
public class SpatialTTSPlayer : MonoBehaviour {
    [SerializeField] private AudioSource audioSource;

    void Awake() {
        audioSource = GetComponent<AudioSource>();

        // Full 3D spatialization
        audioSource.spatialBlend = 1.0f;

        // Rolloff settings
        audioSource.rolloffMode = AudioRolloffMode.Logarithmic;
        audioSource.minDistance = 1f;
        audioSource.maxDistance = 15f;

        // Spread for natural sound
        audioSource.spread = 60f;

        // Doppler off (stationary AI assistant)
        audioSource.dopplerLevel = 0f;
    }

    public void PlayResponse(AudioClip clip) {
        audioSource.clip = clip;
        audioSource.Play();
    }
}
```

### Positioning the AI Voice

```csharp
public class AIAssistantPosition : MonoBehaviour {
    [SerializeField] private Transform playerHead;
    [SerializeField] private float distance = 2f;
    [SerializeField] private float height = 0.3f;  // Slightly above eye level

    void Update() {
        // Position in front of player, slightly above
        Vector3 forward = playerHead.forward;
        forward.y = 0;  // Keep on horizontal plane
        forward.Normalize();

        transform.position = playerHead.position
            + forward * distance
            + Vector3.up * height;

        // Face the player
        transform.LookAt(playerHead);
    }
}
```

## Speculative TTS Processing

### Sentence-Boundary Chunking

Start TTS before the full Claude response arrives:

```csharp
public class SpeculativeTTS : MonoBehaviour {
    private Queue<AudioClip> clipQueue = new Queue<AudioClip>();
    private bool isPlaying = false;
    private StringBuilder currentSentence = new StringBuilder();

    public void OnPartialResponse(string partial) {
        currentSentence.Append(partial);
        string text = currentSentence.ToString();

        // Check for sentence boundary
        int boundaryIndex = FindSentenceBoundary(text);
        if (boundaryIndex > 0) {
            string sentence = text.Substring(0, boundaryIndex + 1).Trim();
            currentSentence.Remove(0, boundaryIndex + 1);

            // Send to TTS immediately
            RequestTTS(sentence);
        }
    }

    int FindSentenceBoundary(string text) {
        // Find last sentence-ending punctuation
        for (int i = text.Length - 1; i >= 0; i--) {
            if (text[i] == '.' || text[i] == '!' || text[i] == '?') {
                return i;
            }
        }
        return -1;
    }

    async void RequestTTS(string text) {
        // Call TTS API
        AudioClip clip = await TTSApi.Synthesize(text);
        clipQueue.Enqueue(clip);

        if (!isPlaying) PlayNext();
    }

    void PlayNext() {
        if (clipQueue.Count == 0) {
            isPlaying = false;
            return;
        }

        isPlaying = true;
        AudioClip clip = clipQueue.Dequeue();
        GetComponent<AudioSource>().clip = clip;
        GetComponent<AudioSource>().Play();

        // Play next clip when current finishes
        StartCoroutine(WaitAndPlayNext(clip.length));
    }

    IEnumerator WaitAndPlayNext(float delay) {
        yield return new WaitForSeconds(delay);
        PlayNext();
    }
}
```

### Latency Savings

| Without Speculative | With Speculative |
|--------------------|-----------------|
| Wait for full response | Send first sentence immediately |
| Then generate all TTS | TTS generates during LLM streaming |
| Then play sequentially | Play first sentence while rest generates |
| **Total: LLM + TTS + Play** | **Total: LLM + Play** (TTS overlapped) |

Typical savings: 200-500ms perceived latency reduction.

## Meta Spatial Audio SDK

### Integration with Meta Audio SDK

If using Meta's spatial audio:

```csharp
using Meta.XR.Audio;

// Add MetaXRAudioSource component for HRTF spatialization
var metaAudio = gameObject.AddComponent<MetaXRAudioSource>();
metaAudio.EnableSpatialization = true;
metaAudio.EnableRoomEffect = true;
```

### Room Acoustics

```csharp
// Configure room for natural speech acoustics
var room = FindObjectOfType<MetaXRAudioRoom>();
if (room != null) {
    room.RoomWidth = 4f;
    room.RoomHeight = 3f;
    room.RoomDepth = 4f;
    room.WallMaterial = MetaXRAudioRoom.WallMaterials.CURTAIN_HEAVY;
}
```

## Audio Format

### TTS API Response Format

Most TTS APIs return:
- Format: WAV or MP3
- Sample rate: 22050Hz or 44100Hz
- Channels: Mono (1 channel)

### Converting to AudioClip

```csharp
AudioClip CreateClipFromWav(byte[] wavData) {
    // Skip WAV header (44 bytes)
    int sampleCount = (wavData.Length - 44) / 2;  // 16-bit samples
    float[] samples = new float[sampleCount];

    for (int i = 0; i < sampleCount; i++) {
        short val = BitConverter.ToInt16(wavData, 44 + i * 2);
        samples[i] = val / (float)short.MaxValue;
    }

    AudioClip clip = AudioClip.Create("tts", sampleCount, 1, 22050, false);
    clip.SetData(samples, 0);
    return clip;
}
```

## Performance Considerations

- Audio decoding and playback have minimal CPU cost
- Spatial audio HRTF processing: <0.5ms per source
- Keep total active AudioSources under 32 for Quest
- Use AudioClip pooling to avoid GC from frequent allocations
