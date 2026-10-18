"""Semantic static acceptance for the current funnel; no external requests."""
from pathlib import Path
from html.parser import HTMLParser
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import overdrive

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.h1=0;self.text=[];self.ignore=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script':self.ignore+=1
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        for attr in ['src','href']:
            if attr in a:self.links.append(a[attr])
    def handle_endtag(self,tag):
        if tag=='script':self.ignore-=1
    def handle_data(self,data):
        if not self.ignore:self.text.append(data)

def check(html,lang):
    p=Page();p.feed(html)
    assert p.h1==1 and len(p.ids)==len(set(p.ids))
    for link in p.links:
        if link.startswith('#'):assert link[1:] in p.ids,link
        elif not link.startswith(('https:','http:')):assert (ROOT/link).is_file(),link
    assert {'money-0','money-1','money-2','demo-message','demo-preview'}.issubset(p.ids)
    assert 'lead-form' in p.ids or 'lead-telegram' in p.ids
    assert 'money-3' not in p.ids and 'money-4' not in p.ids
    text=' '.join(p.text)
    for term in ['sandbox','backend','Пока не рассчитана','Not yet calculated','Hali hisoblanmagan']:
        assert term.casefold() not in text.casefold(),term
    c=overdrive.COPY[lang]
    for value in [c['setup'],c['risk'],c['calcCTA'],c['separate'],c['brand']]:assert value in text,value
    assert overdrive.RELEASE[lang]['notificationLabels']['title'] in text and '+998 XX XXX XX XX' in text
    assert html.count('type="range"')==5 # four visible aggregator sliders; fifth replaces fields in time mode
    assert 'fetch(' not in html
    assert 'canonical' in html and 'hreflang' in html
    return p

for lang,name in [('ru','index.html'),('uz','uz.html'),('en','en.html')]:
    html=(ROOT/name).read_text(encoding='utf8');check(html,lang)
    # A known bad positive control must fail each negative check.
    for bad in [html.replace('money-2','money-3'),html+'<p>sandbox</p>',html+'<a href="#missing-anchor">bad</a>']:
        try:check(bad,lang)
        except AssertionError:pass
        else:raise AssertionError('negative control accepted')
assert 'from funnel import generate' in (ROOT/'scripts/build.py').read_text(encoding='utf8')
assert 'prefers-reduced-motion' in (ROOT/'funnel.css').read_text(encoding='utf8')
assert 'controls preload="none"' in (ROOT/'scripts/funnel.py').read_text(encoding='utf8')
assert 'tour-poster.webp' in (ROOT/'scripts/funnel.py').read_text(encoding='utf8')
print('OVERDRIVE_STATIC_OK')
