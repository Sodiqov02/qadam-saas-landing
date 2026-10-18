"""Verify the user's real URL. Read-only HTTP; form transport is mocked in browser."""
from pathlib import Path
import hashlib
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:4173/'
OUT=ROOT/'artifacts'/'preview-fix'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    checks=[];errors=[];failures=[];hashes={}
    with sync_playwright() as p:
        browser=p.chromium.launch()
        context=browser.new_context(reduced_motion='reduce')
        page=context.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
        page.on('response',lambda response:failures.append({'url':response.url,'status':response.status}) if response.status>=400 else None)
        cdp=context.new_cdp_session(page);cdp.send('Network.enable');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True})
        for filename in ['index.html','uz.html','en.html','styles.css','funnel.css','funnel.js']:
            response=context.request.get(BASE+('' if filename=='index.html' else filename))
            assert response.status==200 and response.body()==(ROOT/filename).read_bytes(),filename
            assert response.headers.get('cache-control')=='no-store'
            assert response.headers.get('x-qadamup-preview')=='b2b-funnel-v1'
            hashes[filename]=hashlib.sha256(response.body()).hexdigest()
        for filename in ['index.html','uz.html','en.html']:
            response=page.goto(BASE+('' if filename=='index.html' else filename),wait_until='networkidle')
            assert response.status==200
            assert page.locator('#scenario-form').count()==1
            assert page.locator('#demo-open').count()==1
            assert page.locator('#lead-form').count()==1
            assert page.locator('link[href="funnel.css"]').count()==1
            assert page.locator('script[src="funnel.js"]').count()==1
            page.locator('#share').fill('0');page.locator('#share').dispatch_event('input')
            assert page.locator('#money-2').inner_text().startswith('0')
            for ident in ['demo-open','demo-dish','demo-add','demo-checkout','demo-accept','demo-ready']:page.locator('#'+ident).click()
            assert page.locator('#demo-status').inner_text()==json.loads(page.locator('#page-config').text_content())['complete']
            # Do not write even synthetic leads into the user's actual preview DB.
            page.route('**/api/session',lambda route:route.fulfill(json={'csrf':'synthetic-preview-test'}))
            page.route('**/api/leads',lambda route:route.fulfill(json={'saved':True,'notification':'queued'}))
            page.locator('#venue').fill('Synthetic Preview Cafe');page.locator('#contact').fill('@synthetic_test');page.locator('[name=consent]').check()
            page.locator('#lead-form [type=submit]').click()
            page.wait_for_function("() => document.querySelector('#lead-status').textContent===JSON.parse(document.querySelector('#page-config').textContent).queued")
            page.unroute('**/api/session');page.unroute('**/api/leads')
            checks.append(filename+':calculator-demo-form')
        page.goto(BASE,wait_until='networkidle')
        assert page.url==BASE
        assert page.locator('h1').inner_text().splitlines()==['Принимайте заказы.','Без лишних звонков.','Без путаницы.']
        assert page.evaluate('document.styleSheets.length')>=2
        assert page.locator('.hero').evaluate("el=>getComputedStyle(el).backgroundColor")=='rgb(16, 45, 34)'
        for width,height,name in [(1440,1000,'desktop-1440'),(390,844,'mobile-390')]:
            page.set_viewport_size({'width':width,'height':height})
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            for img in page.locator('img').all():
                if img.is_visible():img.scroll_into_view_if_needed();img.evaluate('img=>img.decode()')
            page.evaluate('scrollTo(0,0)')
            page.mouse.move(0,0)
            page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
            page.screenshot(path=str(OUT/(name+'-hero.png')))
            checks.append('actual-url:'+name)
        # Reload with the browser cache enabled, including a second navigation.
        cdp.send('Network.setCacheDisabled',{'cacheDisabled':False})
        for _ in range(2):
            response=page.reload(wait_until='networkidle')
            assert response.headers.get('cache-control')=='no-store'
            assert page.locator('#demo-open').is_visible()
        assert page.evaluate('navigator.serviceWorker.getRegistrations().then(r=>r.length)')==0
        assert not errors,errors
        assert not failures,failures
        browser.close()
    (OUT/'live.json').write_text(json.dumps({'url':BASE,'checks':checks,'sha256':hashes,'javascript_errors':errors,'http_failures':failures,'cache':'no-store, cache disabled then enabled with reload','lead_transport':'mocked; actual preview DB untouched'},indent=2),encoding='utf8')
    print('PREVIEW_LIVE_OK')
if __name__=='__main__':main()
