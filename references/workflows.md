# Workflow selection

| Workflow | Use when | Inputs |
|---|---|---|
| T2V (text-to-video) | Creating a clip from a written scene description | Prompt, duration, aspect ratio, resolution, seed |
| I2V (image-to-video) | Animating one starting image | Image plus motion/action prompt; keep subject and camera intent explicit |
| R2V (reference-to-video) | Maintaining a subject or style from one or more references | Reference assets plus prompt; check the workflow's required reference nodes |

Choose the exact workflow variant for the installed ComfyUI release and GPU backend. Start with batch 1 and modest duration/resolution. Do not assume API workflows work without API credentials or services. Inspect node model selectors after loading; missing-model warnings indicate a path/name mismatch.
