# Common errors

| Symptom | Check | Response |
|---|---|---|
| CUDA out of memory | ComfyUI log, VRAM use, resolution, duration, batch | Stop the run; reduce batch first, then resolution or duration. Close GPU-heavy apps and retry. |
| `comfy_kitchen` missing attribute/module | Desktop's actual Python path and ComfyUI `requirements.txt` pin | Repair the pinned package in that ComfyUI environment; verify import before restarting Desktop. |
| Model missing in node | Exact filename, extension, subfolder, configured shared model paths | Place the file in the expected category and refresh/restart model scanning. |
| Prompt executes but no output found | ComfyUI output directory and execution log | Search recent output files; inspect the final log lines for save/encode errors. |
| MP4 has no audio | `check_output.py` stream list | Confirm the selected workflow includes audio generation and muxing nodes. |
| Download stops or file is incomplete | File size, timestamp, temporary `.part`/`.aria2` files, network log | Resume with the same downloader; do not rename an incomplete file to its final name. |
| Workflow stops around a fixed frame count | Full traceback and progress log | Distinguish model/frame limits, OOM, application timeout, and cloud quota; do not infer cause from the UI alone. |

When requesting help, share the final 30-50 relevant log lines and redact usernames, tokens, and private paths.
