#!/usr/bin/env python3
"""Check MiniMax H3 model files from a JSON manifest."""
import argparse, hashlib, json, pathlib, sys

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', required=True, type=pathlib.Path)
    p.add_argument('--manifest', required=True, type=pathlib.Path)
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    failures = 0
    for item in manifest:
        path = args.root / item['path']
        row = {'name': item.get('name', path.name), 'path': str(path), 'expected': item.get('size')}
        if not path.is_file():
            row['status'] = 'MISSING'; failures += 1
        else:
            row['size'] = path.stat().st_size
            row['status'] = 'OK' if item.get('size') in (None, row['size']) else 'SIZE_MISMATCH'
            if row['status'] != 'OK': failures += 1
            if item.get('sha256'):
                row['sha256'] = digest(path)
                if row['sha256'].lower() != item['sha256'].lower(): row['status'] = 'HASH_MISMATCH'; failures += 1
        print(json.dumps(row, ensure_ascii=False))
    print('RESULT ' + ('FAIL' if failures else 'PASS'))
    return 1 if failures else 0
if __name__ == '__main__': sys.exit(main())
