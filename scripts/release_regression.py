"""Exercise retained local API mode in a disposable source tree, preserving production HTML."""
from pathlib import Path
import tempfile
import shutil
import subprocess
import sys
import hashlib

ROOT=Path(__file__).resolve().parents[1]
def main():
    before={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['index.html','uz.html','en.html']}
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory)/'checkout';root.mkdir()
        for name in ['scripts','assets']:
            shutil.copytree(ROOT/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
        for f in ROOT.iterdir():
            if f.is_file() and f.suffix in ['.js','.css','.html','.py','.txt','.ico','.png','.xml','.webmanifest']:shutil.copy2(f,root/f.name)
        def run(*args):subprocess.run(args,cwd=root,check=True,timeout=180)
        run(sys.executable,'scripts/preview_build_test.py')
        run(sys.executable,'scripts/funnel.py','--target','local')
        run('node','scripts/funnel_verify.cjs')
        run('node','scripts/verify.mjs')
        run(sys.executable,'scripts/overdrive_check.py')
        run(sys.executable,'scripts/funnel_test.py')
        run(sys.executable,'scripts/features_check.py')
        run(sys.executable,'scripts/browser_check.py')
        evidence=ROOT/'artifacts/release/local-regression'
        evidence.mkdir(parents=True,exist_ok=True)
        for name in ['budget-lab.json','checks.json','accessibility.json']:
            shutil.copy2(root/'artifacts/funnel'/name,evidence/name)
    assert before=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in before}
    print('RELEASE_REGRESSION_OK')
if __name__=='__main__':main()
