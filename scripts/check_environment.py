#!/usr/bin/env python3
"""Create a redacted local environment report without credentials or full user paths."""
import argparse, json, pathlib, platform, shutil, subprocess, sys
def run(cmd):
    try: return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, timeout=15).strip()
    except Exception as e: return 'unavailable: ' + type(e).__name__
def main():
    p=argparse.ArgumentParser(); p.add_argument('--comfyui', type=pathlib.Path); p.add_argument('--json', action='store_true'); a=p.parse_args()
    report={'platform':platform.platform(),'python':platform.python_version(),'comfyui':str(a.comfyui) if a.comfyui else 'not provided','disk_free_bytes':shutil.disk_usage(a.comfyui or pathlib.Path.cwd()).free,'nvidia_smi':run(['nvidia-smi','--query-gpu=name,memory.total','--format=csv,noheader'])}
    print(json.dumps(report, ensure_ascii=False, indent=2) if a.json else '\n'.join('%s: %s' % x for x in report.items()))
if __name__=='__main__': main()
