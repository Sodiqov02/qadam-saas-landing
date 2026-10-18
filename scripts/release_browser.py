"""Production-like static HTTP checks; external Telegram navigation intercepted, no messages sent."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import argparse
import json
import hashlib
from urllib.parse import urlsplit,parse_qs
from playwright.sync_api import sync_playwright
from overdrive_accessibility import CONTRAST

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/release'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
def main(base=None):
    OUT.mkdir(parents=True,exist_ok=True)
    app=None
    if not base:
        app=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
        Thread(target=app.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{app.server_port}/'
    production=base.startswith('https:')
    checks=[];errors=[];network=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            context=browser.new_context(reduced_motion='reduce')
            for lang,file in [('ru','index.html'),('uz','uz.html'),('en','en.html')]:
                page=context.new_page()
                page.on('pageerror',lambda error:errors.append(str(error)))
                page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
                page.on('response',lambda response:errors.append(f'HTTP {response.status}: {response.url}') if response.status>=400 else None)
                page.on('request',lambda request:network.append({'method':request.method,'url':request.url}))
                page.add_init_script("window.testEvents=[];addEventListener('qadamup:analytics',e=>testEvents.push(e.detail))")
                url=base+('' if lang=='ru' else file)
                response=page.goto(url,wait_until='networkidle')
                assert response.status==200
                assert hashlib.sha256(response.body()).digest()==hashlib.sha256((ROOT/file).read_bytes()).digest(),file+': deployed content differs'
                assert page.locator('#lead-form').count()==0
                assert page.locator('#lead-telegram').is_visible()
                assert page.locator('#money-2').inner_text().replace('\xa0',' ').replace('\u202f',' ').startswith(('3 600 000','3,600,000'))
                for width in [320,360,375,390,430,768,1024,1440,1920]:
                    page.set_viewport_size({'width':width,'height':900 if width>800 else 844})
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && visualViewport.scale===1'),(lang,width)
                    assert not page.evaluate(CONTRAST),(lang,width,page.evaluate(CONTRAST))
                    checks.append(f'{lang}:width:{width}')
                for anchor in page.locator('a[href^="#"]').all():assert page.locator(anchor.get_attribute('href')).count()==1
                for anchor in page.locator('a').all():
                    href=anchor.get_attribute('href')
                    if not href.startswith(('#','https:')):assert page.request.get(base+href).ok
                for image in page.locator('img').all():
                    assert page.request.get(base+image.get_attribute('src')).ok
                    assert image.get_attribute('alt')
                    if image.is_visible():
                        image.scroll_into_view_if_needed();image.evaluate('i=>i.decode()')
                        assert image.evaluate('i=>i.naturalWidth>0')
                page.locator('#share').focus();page.keyboard.press('End');assert page.locator('#share').input_value()=='100'
                assert page.locator('#money-2').inner_text().replace('\xa0',' ').replace('\u202f',' ').startswith(('12 000 000','12,000,000'))
                page.locator('[data-mode=direct]').click();assert page.locator('#time-results').is_visible()
                page.locator('[data-mode=aggregator]').click()
                for ident in ['demo-open','demo-dish','demo-add','demo-add','demo-checkout']:
                    page.locator('#'+ident).click()
                config=json.loads(page.locator('#page-config').text_content())
                notification=page.locator('#demo-message').inner_text()
                assert config['dish']+' × 2' in notification
                assert '90000' in ''.join(ch for ch in notification if ch.isdigit())
                assert notification==page.locator('#telegram-sample').inner_text()
                assert page.locator('#telegram .telegram-window button').count()==0
                page.locator('#demo-accept').click();page.locator('#demo-ready').click()
                assert page.locator('#demo-status').inner_text()==config['complete']
                page.locator('#demo-reset').click()
                for summary in page.locator('summary').all():
                    summary.focus();page.keyboard.press('Enter');assert summary.evaluate('e=>e.parentElement.open');page.keyboard.press('Enter')
                link=page.locator('#lead-telegram').get_attribute('href')
                parsed=urlsplit(link);assert parsed.netloc=='t.me' and parsed.path=='/hacker_ronin'
                assert parse_qs(parsed.query).get('text')
                # Prove the click opens the intended destination, without contacting or messaging anyone.
                context.route('https://t.me/**',lambda route:route.fulfill(status=200,body='Navigation destination verified; no message sent.'))
                with page.expect_popup() as popup_info:page.locator('#lead-telegram').click()
                popup=popup_info.value;popup.wait_for_load_state();assert popup.url==link;popup.close()
                events=page.evaluate('testEvents')
                assert 'telegram_contact_click' in {e['event'] for e in events}
                assert all(set(e)=={'event','locale','variant'} for e in events)
                page.goto(url,wait_until='networkidle')
                for image in page.locator('img').all():
                    if image.is_visible():image.scroll_into_view_if_needed();image.evaluate('i=>i.decode()')
                prefix=('production-' if production else '')+lang
                page.set_viewport_size({'width':1440,'height':1000});page.evaluate('scrollTo(0,0)')
                page.screenshot(path=str(OUT/f'{prefix}-desktop.png'),full_page=True)
                if lang=='ru':
                    for ident in ['telegram','pricing','trust','contacts']:
                        page.locator('#'+ident).screenshot(path=str(OUT/f'{prefix}-{ident}.png'))
                    page.set_viewport_size({'width':390,'height':844});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/f'{prefix}-mobile.png'),full_page=True)
                    page.set_viewport_size({'width':375,'height':812});page.screenshot(path=str(OUT/f'{prefix}-hero-375.png'))
                page.close();checks.append(lang+':demo-contact-faq-images')
            assert not errors,errors
            assert not any('/api/' in r['url'] or r['method']!='GET' for r in network),network
            nojs=browser.new_context(java_script_enabled=False);page=nojs.new_page();page.goto(base)
            assert page.locator('#lead-telegram').is_visible() and page.locator('h1').is_visible();nojs.close()
            browser.close()
    finally:
        if app:app.shutdown();app.server_close()
    (OUT/('production-browser.json' if production else 'static-browser.json')).write_text(json.dumps({'base':base,'checks':checks,'errors':errors,'api_requests':0,'contact':'Telegram draft navigation verified with interception; no message sent'},indent=2),encoding='utf8')
    print('RELEASE_BROWSER_OK',len(checks),'groups',base)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base');args=parser.parse_args();main(args.base)
