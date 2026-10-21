import hashlib, json, pathlib, subprocess, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ScriptTests(unittest.TestCase):
    def test_model_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td); f=root/'model.safetensors'; f.write_bytes(b'weights')
            manifest=root/'manifest.json'; item={'path':'model.safetensors','size':7,'sha256':hashlib.sha256(b'weights').hexdigest()}; manifest.write_text(json.dumps([item]),encoding='utf-8')
            cmd=[sys.executable,str(ROOT/'scripts/check_models.py'),'--root',td,'--manifest',str(manifest)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            item['sha256']='0'*64; manifest.write_text(json.dumps([item]),encoding='utf-8')
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,1)
    def test_missing_model_fails(self):
        with tempfile.TemporaryDirectory() as td:
            manifest=pathlib.Path(td)/'manifest.json'; manifest.write_text(json.dumps([{'path':'missing.safetensors'}]),encoding='utf-8')
            cmd=[sys.executable,str(ROOT/'scripts/check_models.py'),'--root',td,'--manifest',str(manifest)]
            self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,1)
if __name__=='__main__': unittest.main()
