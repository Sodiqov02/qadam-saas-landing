"""Current capability contract; historical mapping is in docs/release-test-mapping.md."""
from pathlib import Path
import re
import json
from html import unescape
ROOT=Path(__file__).resolve().parents[1]

def check(text,expected):
    section=re.search(r'<section class="features-section".*?</section>',text,re.S).group()
    assert section.count('class="feature"')==3
    for title in expected:assert title in unescape(section)
    assert 'class="expansion"' in section
    assert not any(word in section.casefold() for word in ['sandbox','backend','в тестировании'])
    assert 'id="trust"' in text
    return section

def main():
    from overdrive import COPY
    for lang,file in [('ru','index.html'),('uz','uz.html'),('en','en.html')]:
        text=(ROOT/file).read_text(encoding='utf8');titles=[row[0] for row in COPY[lang]['features']]
        check(text,titles)
        bad=text.replace(titles[0],'missing-feature')
        try:check(bad,titles)
        except AssertionError:pass
        else:raise AssertionError('feature positive control accepted')
    print('FEATURES_CURRENT_OK')
if __name__=='__main__':main()
