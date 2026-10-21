#!/usr/bin/env python3
import argparse, json, pathlib, subprocess, sys
def run(args):
    try: return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT, timeout=30).strip()
    except Exception as e: return 'unavailable: ' + type(e).__name__
def main():
    p=argparse.ArgumentParser(); p.add_argument('--comfyui', type=pathlib.Path); p.add_argument('--models', type=pathlib.Path); p.add_argument('--output', type=pathlib.Path); p.add_argument('--manifest', type=pathlib.Path); p.add_argument('--json', action='store_true'); a=p.parse_args()
    env_cmd=[sys.executable, str(pathlib.Path(__file__).with_name('check_environment.py')), '--json']
    if a.comfyui: env_cmd.extend(['--comfyui',str(a.comfyui)])
    r={'environment':json.loads(run(env_cmd))}
    if a.models and a.manifest:
        result=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('check_models.py')),'--root',str(a.models),'--manifest',str(a.manifest)],text=True,capture_output=True)
        r['models']=[json.loads(line) if line.startswith('{') else line for line in result.stdout.splitlines()]
        r['models_exit_code']=result.returncode
    if a.output and a.output.exists():
        files=[x for x in sorted(a.output.rglob('*')) if x.is_file()]
        media=next((x for x in reversed(files) if x.suffix.lower() in ('.mp4','.mkv','.mov','.webm')),None)
        r['output_files']=[str(x) for x in files[-20:]]
        if media: r['latest_media']=run([sys.executable,str(pathlib.Path(__file__).with_name('check_output.py')),str(media)])
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 1 if r.get('models_exit_code',0) else 0
if __name__=='__main__': sys.exit(main())
