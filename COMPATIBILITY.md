# Compatibility

| Environment | Status | Evidence |
|---|---|---|
| Windows 11 + RTX 5060 Laptop 8 GB | Verified starting point | 864x480, 5 seconds, 20 steps, MiniMax H3 output with audio |
| NVIDIA 12/16/24 GB | Starting guidance only | See `references/hardware-matrix.md` |
| AMD / ROCm | Not verified in this project | Requires an AMD-specific ComfyUI and backend check |
| ComfyUI templates | Verified locally | See source/license note in `workflows/README.md` |

Record the ComfyUI commit, Python, PyTorch, CUDA/ROCm, and `comfy-kitchen` version with each new benchmark.
