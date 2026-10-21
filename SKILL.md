---
name: minimax-h3-comfyui
description: Deploy, validate, troubleshoot, and run MiniMax H3 video workflows in ComfyUI. Use for model layout checks, dependency diagnosis, workflow selection, and output verification. Do not use for unrelated ComfyUI workflows.
metadata:
  short-description: MiniMax H3 ComfyUI workflow helper
---

# MiniMax H3 ComfyUI

Use this skill to help a user install or run MiniMax H3 text-to-video, image-to-video, or reference-to-video workflows in ComfyUI.

## Operating rules

- Inspect the actual ComfyUI installation, Python environment, GPU, and model paths before changing anything.
- Reuse existing verified model files. Do not download duplicates or overwrite a model without explicit authorization.
- Keep model files in the ComfyUI shared model tree: `models/diffusion_models`, `models/text_encoders`, `models/vae`, and `models/loras`.
- Verify downloads by expected size and SHA-256 when authoritative metadata is available. Preserve incomplete `.part` or `.curlpart` files for resuming.
- Treat third-party download pages, modified model variants, archives, and executables as untrusted until their source, filename, license, and checksum are clear.
- Match workflow, resolution, duration, and attention settings to GPU memory. Explain that dynamic offloading can use substantial system RAM.
- After running a workflow, check the output directory and inspect the media container for video and audio streams.
- Ask for explicit authorization immediately before destructive actions, model replacement, external publishing, or automatic shutdown. Never infer shutdown permission from a completed download.

## Default model layout

- Diffusion model: `models/diffusion_models/`
- Text encoder: `models/text_encoders/`
- VAE files: `models/vae/`
- LoRA files: `models/loras/`

The exact filenames and repositories are configuration, not assumptions. Confirm them from the selected workflow or authoritative model page.

## Troubleshooting

If ComfyUI fails during import, read the full traceback and identify the Python executable actually used by Desktop. For `comfy_kitchen` errors, compare the installed package with the ComfyUI `requirements.txt` pin, repair only the ComfyUI virtual environment, then verify imports before restarting Desktop. Do not patch core source as a first response.

## Completion report

Report changed files, model locations, verification result, workflow settings, output path, and the next GUI action. Clearly distinguish a successful generation from a merely present output file.
