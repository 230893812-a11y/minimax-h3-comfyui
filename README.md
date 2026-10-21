# MiniMax H3 ComfyUI Skill

This package contains a Codex Skill for reusable MiniMax H3 ComfyUI deployment and troubleshooting workflows.

Copy the `minimax-h3-comfyui` folder into your Codex skills directory, for example `%CODEX_HOME%\skills\minimax-h3-comfyui`.

The package contains instructions only. It does not include model weights, credentials, private logs, or third-party executables.

## Checks

From the skill folder, run `python scripts/check_environment.py --json`, `python scripts/check_models.py --root D:\Comfy-Desktop\ComfyUI-Shared --manifest examples/models.json`, or `python scripts/check_output.py path\to\video.mp4`. Edit the example manifest to match the selected model release before checking.

## Install

On Windows, run `./install.ps1` from this folder. Then restart Codex or start a new chat. To remove the installed copy, run `./uninstall.ps1`.

## License

MIT. See `LICENSE`.
