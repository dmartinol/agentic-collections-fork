### Supported runtimes

| Runtime | Typical use | Setup |
|---------|------------|--------|
| **vLLM** | Open-source LLMs (Llama, Granite, Mixtral, Mistral) | None beyond cluster/serving |
| **NVIDIA NIM** | TensorRT-LLM on NVIDIA GPUs | Run **`/nim-setup`** first |
| **Caikit+TGIS** | Caikit-format models, gRPC | Model conversion as required |

Full comparison: **[supported-runtimes.md](../docs/references/supported-runtimes.md)**.

### Example model / GPU profiles

| Model | Params | Min GPUs (typical) | Default runtime |
|-------|--------|--------------------|-----------------|
| Llama 3.1 8B | 8B | 1× (16GB VRAM) | vLLM |
| Llama 3.1 70B | 70B | 4× A100 80GB | vLLM / NIM |
| Granite 3.1 8B | 8B | 1× (16GB VRAM) | vLLM |
| Mixtral 8x7B | 46.7B MoE | 2× A100 80GB | vLLM |
| Mistral 7B | 7B | 1× (16GB VRAM) | vLLM |

Extended tables and guidance: **[known-model-profiles.md](../docs/references/known-model-profiles.md)**. Models not listed are still supported via product docs and live cluster checks.

### In-repo examples

- NIM walkthrough: [nim-setup.md](../docs/examples/nim-setup.md) (also linked from **References** below).
