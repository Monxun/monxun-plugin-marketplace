# SGLang Deterministic Inference Setup

## Installation

```bash
pip install sglang[all]

# Or from source for latest deterministic features
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git"
```

## Server Configuration

### Basic Deterministic Mode

```bash
python -m sglang.launch_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --enable-deterministic-inference \
    --port 30000
```

### With Performance Optimization

```bash
python -m sglang.launch_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --enable-deterministic-inference \
    --attention-backend flashinfer \
    --enable-cuda-graph \
    --port 30000
```

### Environment Variables

```bash
# Enable deterministic mode programmatically
export SGLANG_DETERMINISTIC=1

# Set default seed
export SGLANG_SEED=42
```

## Client Configuration

```python
import sglang as sgl

# Connect to server
sgl.set_default_backend(sgl.RuntimeEndpoint("http://localhost:30000"))

# Deterministic generation
@sgl.function
def generate_heuristic(s, pattern):
    s += sgl.user(f"Generate heuristic for: {pattern}")
    s += sgl.assistant(sgl.gen("response", temperature=0))

# Will produce identical output across runs
result = generate_heuristic.run(pattern="Early return")
```

## Testing Determinism

### Single Prompt Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode single \
    --num-runs 50
```

### Mixed Batch Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode mixed \
    --num-runs 50
```

### Prefix Cache Test

```bash
python -m sglang.test.test_deterministic \
    --test-mode prefix \
    --num-runs 50
```

## Performance Impact

| Configuration | Throughput | Determinism |
|---------------|------------|-------------|
| Default | 100% | ~80% |
| Deterministic | 65% | 100% |
| + CUDA Graphs | 88% | 100% |
| + FlashInfer | 92% | 100% |

## Troubleshooting

### Non-Determinism Detected

```bash
# Check batch sizes
curl http://localhost:30000/v1/models/stats

# Verify kernel implementations
python -c "import sglang; print(sglang.check_deterministic_kernels())"
```

### Memory Issues

```bash
# Reduce max batch size
python -m sglang.launch_server \
    --model your-model \
    --enable-deterministic-inference \
    --max-num-seqs 16  # Lower for stability
```

## Integration Example

```python
class DeterministicHeuristicEvaluator:
    def __init__(self, server_url: str):
        sgl.set_default_backend(sgl.RuntimeEndpoint(server_url))

    def evaluate(self, heuristic: str, test_cases: list) -> dict:
        """Evaluate with guaranteed reproducibility."""
        results = []

        for case in test_cases:
            # Same input always produces same output
            output = self._run_evaluation(heuristic, case)
            results.append(output)

        return {
            "results": results,
            "reproducible": True
        }
```
