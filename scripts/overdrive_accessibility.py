"""Rendered text contrast, keyboard, motion and privacy checks on loopback only."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CONTRAST=r'''() => {
 const rgb=s=>(s.match(/[\d.]+/g)||[]).map(Number);
 const light=c=>{const a=c.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return a[0]*.2126+a[1]*.7152+a[2]*.0722};
 const failures=[];
 for(const el of document.querySelectorAll('body *')){
  if(!el.getClientRects().length||['SCRIPT','STYLE','NOSCRIPT','OPTION','SVG','PATH'].includes(el.tagName))continue;
  if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
  const st=getComputedStyle(el);if(st.visibility==='hidden')continue;
  let bg=[255,255,255],node=el;
  while(node){const c=rgb(getComputedStyle(node).backgroundColor);if(c.length===3||c[3]===1){bg=c;break}node=node.parentElement;}
  const color=rgb(st.color),a=light(color),b=light(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  const large=parseFloat(st.fontSize)>=24||(parseFloat(st.fontSize)>=18.66&&Number(st.fontWeight)>=700),min=large?3:4.5;
  if(ratio+.01<min)failures.push({tag:el.tagName,cls:el.className,text:el.textContent.trim().slice(0,65),ratio:+ratio.toFixed(2),minimum:min,color:st.color,bg});
 }
 return failures;
}'''
def main(base='http://127.0.0.1:4173/'):
    records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for file in ['index.html','uz.html','en.html']:
            page=browser.new_page(reduced_motion='reduce',viewport={'width':390,'height':844})
            page.goto(base+file,wait_until='networkidle')
            page.keyboard.press('Tab');assert page.evaluate('document.activeElement.className')=='skip-link'
            page.keyboard.press('Enter');assert page.url.endswith('#main')
            page.locator('#share').focus();page.keyboard.press('ArrowRight');assert page.locator('#share').input_value()=='35'
            assert page.locator('#share').evaluate("el=>getComputedStyle(el).outlineStyle")!='none'
            assert page.locator('.btn').first.evaluate("el=>getComputedStyle(el).transitionDuration")=='0s'
            assert page.locator('input:not([type=checkbox]):not([type=range])').evaluate_all("els=>els.every(e=>e.closest('.honeypot')||e.labels.length)")
            for img in page.locator('img').all():assert img.get_attribute('alt')
            failures=page.evaluate(CONTRAST)
            records.append({'page':file,'contrast_failures':failures})
            assert not failures,json.dumps(failures,ensure_ascii=True)
            page.set_viewport_size({'width':1440,'height':1000})
            failures=page.evaluate(CONTRAST)
            assert not failures,json.dumps(failures,ensure_ascii=True)
            page.evaluate("const el=document.createElement('p');el.id='contrast-positive-control';el.textContent='known contrast failure';el.style='color:white;background:white';document.body.append(el)")
            assert any(x['text']=='known contrast failure' for x in page.evaluate(CONTRAST))
            page.evaluate("document.querySelector('#contrast-positive-control').remove()")
            # Actual client-side invalid contact path; must not claim success or send PII.
            page.route('**/api/**',lambda route: (_ for _ in ()).throw(AssertionError('invalid contact sent')))
            page.locator('#venue').fill('Synthetic Cafe');page.locator('#contact').fill('bad');page.locator('[name=consent]').check()
            page.locator('#lead-form [type=submit]').click()
            config=json.loads(page.locator('#page-config').text_content())
            assert page.locator('#lead-status').inner_text()==config['invalid']
            page.close()
        browser.close()
    (ROOT/'artifacts/funnel/accessibility.json').write_text(json.dumps(records,indent=2),encoding='utf8')
    print('OVERDRIVE_ACCESSIBILITY_OK')
if __name__=='__main__':main()
