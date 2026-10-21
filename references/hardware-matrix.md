# Hardware starting points

These are conservative starting points, not guarantees. Actual memory use depends on ComfyUI version, workflow, attention backend, model quantization, drivers, and other GPU workloads. Confirm against the exact workflow and stop if logs report out-of-memory errors.

| GPU / memory | Starting settings | Notes |
|---|---|---|
| NVIDIA, 8 GB VRAM | 5 seconds, 480p class (for example 864x480 landscape), 20 steps, batch 1 | Dynamic offload may need substantial system RAM; close GPU-heavy applications. |
| NVIDIA, 12 GB VRAM | Start at 5 seconds and 480p; raise one setting at a time | More headroom does not guarantee a longer clip. |
| NVIDIA, 16 GB VRAM | 5-6 seconds around 480p to start | NVFP4 needs supported hardware/software; verify the model format and kernel support. |
| NVIDIA, 24 GB+ VRAM | Start from workflow defaults, then benchmark | Increase duration, resolution, or batch separately. |
| AMD / ROCm | Use an AMD-compatible ComfyUI build and workflow | NVIDIA CUDA/NVFP4 instructions may not apply; verify ROCm and backend support first. |
| Low system RAM or low VRAM | Reduce duration/resolution, batch 1, close other workloads | Offloading shifts memory pressure to system RAM and may become very slow. |

The 8 GB row is based on a user-verified MiniMax H3 run at 864x480, 5 seconds, 20 steps on an RTX 5060 Laptop. It is not a universal benchmark.
