---
name: deterministic-inference
description: |
  Techniques for achieving reproducible LLM inference outputs.
  Use when: requiring exact reproducibility, batch-invariant inference,
  RL training reproducibility, consistent heuristic evaluation.
  Supports: SGLang deterministic mode, seed configuration, validation.
---

# Deterministic Inference Skill

## Quick Start

Achieve mathematically reproducible LLM outputs for consistent heuristic evaluation and validation.

### The Challenge

Even with `temperature=0`, LLM inference is non-deterministic due to:
- Batch-sensitive kernel operations (primary cause)
- Dynamic batching in servers
- Radix cache behavior

### Solution

Use batch-invariant kernels (SGLang) for true determinism.

## Configuration

### SGLang (Recommended)

```bash
python -m sglang.launch_server \
    --model your-model \
    --enable-deterministic-inference \
    --attention-backend flashinfer
```

### Multi-Provider Settings

| Provider | Method | Level |
|----------|--------|-------|
| SGLang | `--enable-deterministic-inference` | Perfect |
| OpenAI | `seed` parameter | Best-effort |
| Anthropic | `temperature=0` | Near-deterministic |
| vLLM | `seed` + env flag | High |
| llama.cpp | `seed=42, temp=0, top_p=1, top_k=1` | High |

## Core Components

### Batch-Invariant Operations

Three operations require special handling:
1. **RMSNorm** - Normalization layer
2. **Matrix Multiplication** - Core computation
3. **Attention** - Self-attention mechanism

### Validation Tests

```bash
# Single prompt, varying batch sizes
python -m sglang.test.test_deterministic --test-mode single

# Mixed prompts in same batch
python -m sglang.test.test_deterministic --test-mode mixed

# Prefix cache consistency
python -m sglang.test.test_deterministic --test-mode prefix
```

## Performance Trade-offs

| Configuration | Slowdown | Reproducibility |
|---------------|----------|-----------------|
| Default | 0% | ~80% |
| Deterministic | 34.35% | 100% |
| + CUDA graphs | 12% | 100% |

## Validation Pattern

```python
class DeterministicValidator:
    def test_single(self, prompt: str, n_runs: int = 50) -> bool:
        """Same prompt across varying batch sizes."""
        outputs = set()
        for batch_size in range(1, n_runs + 1):
            result = self.model.generate(prompt, batch_size=batch_size)
            outputs.add(result)
        return len(outputs) == 1  # Must be 1 for determinism
```

## When to Use

| Scenario | Determinism Needed |
|----------|-------------------|
| Heuristic evaluation | Yes (critical) |
| RL training | Yes (critical) |
| Production inference | Usually no |
| Debugging | Yes (helpful) |

## Additional Resources

- For SGLang setup: [sglang-setup.md](references/sglang-setup.md)
- For validation suite: [validation-suite.md](references/validation-suite.md)
- For performance tuning: [performance-tuning.md](references/performance-tuning.md)

## Research Foundation

Based on: "Towards Deterministic Inference in SGLang"
- Source: Thinking Machines Lab
- Blog: lmsys.org/blog/2025-09-22-sglang-deterministic/
