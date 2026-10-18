"""Build/startup regression in disposable source copies; never touch user leads."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.hrefs=set();self.scripts=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag=='link':self.hrefs.add(attrs.get('href'))
        if tag=='script':self.scripts.add(attrs.get('src'))

def assert_pages(root,contact='lead-telegram'):
    for filename in ['index.html','uz.html','en.html']:
        parser=Page();parser.feed((root/filename).read_text(encoding='utf8'))
        assert {'scenario-form','demo-open',contact}.issubset(parser.ids),filename
        assert 'funnel.css' in parser.hrefs and 'funnel.js' in parser.scripts

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/'checkout';(root/'scripts').mkdir(parents=True)
        for filename in ['build.py','funnel.py','overdrive.py']:shutil.copy2(ROOT/'scripts'/filename,root/'scripts'/filename)
        shutil.copy2(ROOT/'server.py',root/'server.py')
        for entry in ['funnel.py','build.py','build.py']:
            subprocess.run([sys.executable,str(root/'scripts'/entry)],cwd=tmp,check=True,capture_output=True)
            assert_pages(root)
        baseline={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['index.html','uz.html','en.html']}
        # In-memory base-template assembly cannot change any served page.
        spec=importlib.util.spec_from_file_location('base_template',root/'scripts'/'build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.build('ru',module.DATA['ru'],write=False)
        try:module.build('ru',module.DATA['ru'],write=True)
        except ValueError:pass
        else:raise AssertionError('historical template can overwrite current pages')
        assert baseline=={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in baseline}
        # Poison all output files to prove server startup itself repairs stale HTML.
        for filename in baseline:(root/filename).write_text('<h1>Historical sentinel</h1>',encoding='utf8')
        env=os.environ.copy();env.pop('QADAMUP_VIDEO_READY',None)
        child=subprocess.Popen([sys.executable,str(root/'server.py'),'--port','0','--database',str(Path(tmp)/'private'/'leads.sqlite3')],cwd=tmp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env)
        try:
            # Pipe reads have a bounded child lifespan even on startup failure.
            from threading import Timer
            timer=Timer(20,child.kill);timer.start()
            try:
                lines=[]
                while True:
                    line=child.stdout.readline()
                    if not line:raise AssertionError('preview startup failed')
                    lines.append(line.strip())
                    if line.startswith('Local preview: '):break
                url=lines[-1].split('Local preview: ',1)[1]
                assert_pages(root,'lead-form')
                with urllib.request.urlopen(url,timeout=5) as response:
                    assert response.read()==(root/'index.html').read_bytes()
                    assert response.headers.get('X-QadamUp-Preview')=='b2b-funnel-v1'
                    assert response.headers.get('Cache-Control')=='no-store'
                assert any(str(root) in line for line in lines)
            finally:timer.cancel()
        finally:
            child.terminate();child.communicate(timeout=10)
    print('PREVIEW_BUILD_OK')
if __name__=='__main__':main()
