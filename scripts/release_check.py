"""Check actual publishable root output and, when staged, all release blobs."""
from pathlib import Path
import re
import json
import subprocess
from urllib.parse import urlparse,parse_qs
import overdrive
from overdrive_check import check

ROOT=Path(__file__).resolve().parents[1]
def scan(name,data):
    assert not re.search(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',data),name
    assert not re.search(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-)?[A-Za-z0-9_-]{35,})',data),name
    assert not re.search(rb'\b[0-9]{8,12}:[A-Za-z0-9_-]{30,50}\b',data),name
    assert not name.endswith(('.sqlite3','.db','.pyc','.zip')) and not any(p in name.split('/') for p in ['artifacts','.unlazy','__pycache__','.env']),name

def main():
    assert (ROOT/'CNAME').read_text().strip()=='qadamup.uz'
    for lang,file,url in [('ru','index.html','https://qadamup.uz/'),('uz','uz.html','https://qadamup.uz/uz.html'),('en','en.html','https://qadamup.uz/en.html')]:
        html=(ROOT/file).read_text(encoding='utf8');check(html,lang)
        assert 'id="lead-form"' not in html and 'id="lead-telegram"' in html
        config=json.loads(re.search(r'id="page-config">(.*?)</script>',html,re.S)[1])
        assert config['contactMode']=='telegram'
        assert f'<link rel="canonical" href="{url}">' in html
        assert all(f'hreflang="{x}"' in html for x in ['ru','uz','en','x-default'])
        assert '<title>' in html and '<meta name="description"' in html and 'og:image' in html
        href=re.search(r'id="lead-telegram"[^>]*href="([^"]+)"',html)[1]
        parsed=urlparse(href);assert parsed.scheme=='https' and parsed.netloc=='t.me' and parsed.path=='/hacker_ronin'
        assert parse_qs(parsed.query)['text']==[overdrive.RELEASE[lang]['draft']]
        sample=re.search(r'id="telegram-sample">(.*?)</pre>',html,re.S)[1]
        assert '[NEW ORDER' not in sample and '× 1' in sample and '1042' in sample
        assert '+998 XX XXX XX XX' in sample
        assert all(tag in html for tag in overdrive.RELEASE[lang]['planTags'])
        assert 'id="trust"' in html and '<video' not in html # no real footage supplied
        scan(file,html.encode())
    for fixture in [b'-----BEGIN '+b'PRIVATE KEY-----',b'ghp_'+b'a'*40,b'123456789:'+b'A'*35]:
        try:scan('positive-control',fixture)
        except AssertionError:pass
        else:raise AssertionError('secret positive control accepted')
    staged=subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().split('\0')
    for name in filter(None,staged):scan(name,subprocess.check_output(['git','show',':'+name],cwd=ROOT))
    assert 'scripts' in (ROOT/'_config.yml').read_text() and 'server.py' in (ROOT/'_config.yml').read_text()
    print('RELEASE_STATIC_OK')
if __name__=='__main__':main()
