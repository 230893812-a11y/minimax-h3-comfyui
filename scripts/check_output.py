#!/usr/bin/env python3
"""Inspect a generated video/audio container using ffprobe."""
import argparse, json, pathlib, shutil, subprocess, sys
def main():
    p=argparse.ArgumentParser(); p.add_argument('file', type=pathlib.Path); a=p.parse_args()
    probe=shutil.which('ffprobe')
    if not probe: print('ffprobe not found', file=sys.stderr); return 2
    cmd=[probe,'-v','error','-show_entries','format=duration:stream=index,codec_type,width,height,avg_frame_rate','-of','json',str(a.file)]
    try: data=subprocess.check_output(cmd,text=True); print(data); return 0
    except subprocess.CalledProcessError as e: print(e.output or 'invalid media', file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())
