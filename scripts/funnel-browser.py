"""Real Chromium on loopback, synthetic leads only, no external CTA clicks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
import threading
import tempfile
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
def main():
    output=ROOT/'artifacts'/'funnel';output.mkdir(parents=True,exist_ok=True)
    results=[]
    with tempfile.TemporaryDirectory() as temp:
        app=server.make_server(0,Path(temp)/'leads.sqlite3')
        threading.Thread(target=app.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{app.server_port}'
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch()
                for lang,file in [('ru','index.html'),('uz','uz.html'),('en','en.html')]:
                    page=browser.new_page(reduced_motion='reduce');errors=[];requests=[]
                    page.on('request',lambda request:requests.append((request.method,request.url)))
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    page.add_init_script("window.testEvents=[];addEventListener('qadamup:analytics',e=>testEvents.push(e.detail))")
                    page.goto(base+'/'+file,wait_until='networkidle')
                    for width in [320,375,390,768,1024,1440]:
                        page.set_viewport_size({'width':width,'height':900})
                        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{lang} overflow {width}'
                        assert page.locator('h1').is_visible()
                        assert page.evaluate('visualViewport.scale')==1
                        results.append(f'{lang}:layout:{width}')
                    # Every local link, image and fragment resolves.
                    for anchor in page.locator('a[href^="#"]').all():
                        assert page.locator(anchor.get_attribute('href')).count()==1
                    for image in page.locator('img').all():
                        assert page.request.get(base+'/'+image.get_attribute('src')).ok
                        if image.is_visible():
                            image.scroll_into_view_if_needed();image.evaluate('img=>img.decode()');assert image.evaluate('img=>img.complete&&img.naturalWidth>0')
                    assert page.locator('input[type="number"]').count()==0
                    assert page.locator('#money-2').inner_text().replace('\xa0',' ').replace('\u202f',' ').startswith(('3 600 000','3,600,000'))
                    page.locator('#share').fill('0');page.locator('#share').dispatch_event('input')
                    assert page.locator('#money-2').inner_text().startswith('0')
                    page.locator('#share').focus();page.keyboard.press('ArrowRight');assert page.locator('#share').input_value()=='5'
                    page.locator('[data-mode="direct"]').click();assert page.locator('#money-results').is_hidden();assert page.locator('#time-results').is_visible()
                    assert page.locator('#time-1').inner_text().startswith('15')
                    page.locator('[data-mode="aggregator"]').click();assert page.locator('#money-results').is_visible()
                    page.locator('.calc-terms summary').click()
                    page.locator('#scenario-plan').select_option('percentage')
                    page.locator('.calc-terms summary').click()
                    page.locator('[data-event="calculator_cta_click"]').click()
                    page.locator('[data-event="pricing_cta_click"]').first.click()
                    page.locator('.hero [data-event]').click()
                    for ident in ['demo-open','demo-dish','demo-add','demo-checkout','demo-accept','demo-ready']:
                        page.locator('#'+ident).click()
                        if ident=='demo-open':page.locator('#demo-dish img').evaluate('img=>img.decode()')
                        if ident=='demo-checkout':
                            config=json.loads(page.locator('#page-config').text_content())
                            assert config['notificationLabels']['total'] in page.locator('#demo-message').inner_text()
                            assert '+998 XX' in page.locator('#demo-message').inner_text()
                            assert page.locator('#demo-message').inner_text()==page.locator('#telegram-sample').inner_text()
                    assert page.locator('#demo-status').inner_text()==json.loads(page.locator('#page-config').text_content())['complete']
                    assert all(method=='GET' and url.startswith(base) for method,url in requests),requests
                    page.locator('#demo-reset').click();assert page.locator('#demo-open').is_visible();assert page.locator('#demo-checkout').is_hidden()
                    for summary in page.locator('summary').all():
                        summary.focus();page.keyboard.press('Enter');assert summary.evaluate('el=>el.parentElement.open');page.keyboard.press('Enter')
                    page.locator('#venue').fill('Synthetic Browser Cafe '+lang)
                    page.locator('#contact').fill('@synthetic_test')
                    page.locator('[name="consent"]').check()
                    page.locator('#lead-form [type="submit"]').click()
                    page.wait_for_function("() => document.querySelector('#lead-status').textContent===JSON.parse(document.querySelector('#page-config').textContent).queued")
                    assert page.locator('#venue').input_value()==''
                    page.route('**/api/leads',lambda route:route.fulfill(status=503,content_type='application/json',body='{"error":"unavailable"}'))
                    page.locator('#venue').fill('Synthetic retry')
                    page.locator('#contact').fill('@synthetic_test');page.locator('[name="consent"]').check();page.locator('#lead-form [type="submit"]').click()
                    page.wait_for_function("() => document.querySelector('#lead-status').textContent===JSON.parse(document.querySelector('#page-config').textContent).error")
                    assert page.locator('#venue').input_value()=='Synthetic retry'
                    events=page.evaluate('testEvents')
                    assert {'demo_start','demo_completion','calculator_interaction','hero_cta_click','calculator_cta_click','pricing_cta_click','pricing_view','lead_form_start','lead_form_success','lead_form_error'}.issubset({e['event'] for e in events})
                    assert all(set(e)=={'event','locale','variant'} for e in events)
                    assert not errors,errors
                    page.set_viewport_size({'width':1440,'height':1000});page.goto(base+'/'+file)
                    for img in page.locator('img').all():
                        if img.is_visible():img.scroll_into_view_if_needed();img.evaluate('img=>img.decode()')
                    page.evaluate('scrollTo(0,0)')
                    page.screenshot(path=str(output/f'{lang}-desktop.png'),full_page=True)
                    if lang=='ru':page.screenshot(path=str(output/'ru-hero.png'))
                    if lang=='ru':
                        page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(output/'ru-mobile.png'),full_page=True)
                        page.set_viewport_size({'width':375,'height':812});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(output/'ru-hero-375.png'))
                        page.set_viewport_size({'width':1440,'height':1000})
                        for ident in ['calculator','demo','telegram','pricing','contacts']:
                            page.locator('#'+ident).screenshot(path=str(output/f'ru-{ident}.png'))
                    for variant in ['aggregator','manual']:
                        page.goto(base+'/'+file+'?offer='+variant,wait_until='networkidle')
                        config=json.loads(page.locator('#page-config').text_content())
                        assert page.locator('h1').inner_text()==config['variantA' if variant=='aggregator' else 'variantB']
                    page.close();results.append(f'{lang}:calculator-demo-faq-form-error-events')
                # CPU/network budget scenario: actual CDP emulation, lab timing only.
                page=browser.new_page(viewport={'width':375,'height':812})
                cdp=page.context.new_cdp_session(page)
                cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
                cdp.send('Network.enable')
                cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':200000,'uploadThroughput':90000})
                page.add_init_script("window.lab={lcp:0,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())window.lab.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.lab.cls+=e.value}).observe({type:'layout-shift',buffered:true})")
                page.goto(base,wait_until='networkidle');assert page.locator('h1').is_visible()
                timing=page.evaluate('({domContentLoaded:performance.getEntriesByType("navigation")[0].domContentLoadedEventEnd,transfer:performance.getEntriesByType("resource").reduce((s,r)=>s+r.transferSize,0)})')
                timing.update(page.evaluate('window.lab'))
                page.emulate_media(reduced_motion='reduce')
                interaction=page.evaluate("async()=>{const el=document.querySelector('#share');const start=performance.now();el.value='50';el.dispatchEvent(new Event('input',{bubbles:true}));await new Promise(requestAnimationFrame);await new Promise(requestAnimationFrame);return performance.now()-start}")
                assert '6' in page.locator('#money-2').inner_text()
                page.locator('#demo-open').click();assert page.locator('#demo-menu').is_visible()
                timing['slider_to_two_frames_ms']=interaction
                timing['scope']='Lab only: 4x CPU, 150ms latency, 200 KB/s download; not field Core Web Vitals'
                (output/'budget-lab.json').write_text(json.dumps(timing,indent=2),encoding='utf8');page.close()
                nojs=browser.new_context(java_script_enabled=False);page=nojs.new_page();page.goto(base);assert page.locator('h1').is_visible();assert page.locator('noscript').count()>=1;assert page.locator('.language-switch a').count()==3;nojs.close()
                browser.close()
        finally:app.shutdown();app.server_close()
    (output/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf8')
    print('FUNNEL_BROWSER_OK',len(results),'groups; 18 responsive layouts; throttled lab; no-JS')
if __name__=='__main__':main()
