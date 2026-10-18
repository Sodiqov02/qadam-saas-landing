/* Local-only demo, privacy-preserving event hooks and an honest scenario model. */
(function () {
  'use strict';
  function calculate(v) {
    const bounds = {orders:[0,150], average:[0,300000], commission:[0,100], share:[0,100], minutes:[0,10]};
    for (const [key,[min,max]] of Object.entries(bounds)) {
      if (typeof v[key] !== 'number' || !Number.isFinite(v[key]) || v[key]<min || v[key]>max) throw new RangeError(key);
    }
    const turnover=v.orders*v.average*30, direct=turnover*v.share/100, avoided=direct*v.commission/100;
    return {turnover,direct,avoided,netMonthly:null,netAnnual:null,manualHours:v.orders*30*v.minutes/60,savedHours:v.orders*30*v.minutes/120};
  }
  if (typeof module!=='undefined') module.exports={calculate};
  if (typeof document==='undefined') return;
  const c=JSON.parse(document.getElementById('page-config').textContent);
  const $=id=>document.getElementById(id);
  const money=n=>new Intl.NumberFormat(c.locale,{maximumFractionDigits:0}).format(n)+' '+c.currency;
  const number=n=>new Intl.NumberFormat(c.locale,{maximumFractionDigits:1}).format(n);
  // Adapter point only; no network requests, persistent identifiers or PII.
  const requestedVariant=new URLSearchParams(location.search).get('offer');
  const variant=['aggregator','manual'].includes(requestedVariant)?requestedVariant:'control';
  if(variant!=='control') { const hero=document.querySelector('[data-hero]');hero.textContent=variant==='aggregator'?c.variantA:c.variantB; }
  function event(name) { window.dispatchEvent(new CustomEvent('qadamup:analytics',{detail:{event:name,locale:document.documentElement.lang,variant}})); }
  document.querySelectorAll('[data-event]').forEach(a=>a.addEventListener('click',()=>event(a.dataset.event)));
  let mode='aggregator';
  function animatedMoney(element,value) {
    const from=element._number??value;
    if(element._animation)cancelAnimationFrame(element._animation);
    element._number=value;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches||from===value){element.textContent=money(value);return;}
    const start=performance.now();
    function frame(now){const t=Math.min((now-start)/180,1);element.textContent=money(from+(value-from)*(1-Math.pow(1-t,3)));if(t<1)element._animation=requestAnimationFrame(frame);}
    element._animation=requestAnimationFrame(frame);
  }
  function update() {
    const v=Object.fromEntries(['orders','average','commission','share','minutes'].map(k=>[k,Number($(k).value)]));
    const r=calculate(v);
    for(const key of Object.keys(v)) {
      const label=key==='average'?money(v[key]):number(v[key])+(['commission','share'].includes(key)?'%':'');
      $('value-'+key).textContent=label; $(key).setAttribute('aria-valuetext',label);
      $(key).style.setProperty('--range-fill',((v[key]-Number($(key).min))/(Number($(key).max)-Number($(key).min))*100)+'%');
    }
    [r.turnover,r.direct,r.avoided].forEach((v,i)=>animatedMoney($('money-'+i),v));
    $('time-0').textContent=number(r.manualHours)+' '+c.hours; $('time-1').textContent=number(r.savedHours)+' '+c.hours;
    $('money-results').hidden=mode==='direct'; $('time-results').hidden=mode!=='direct';
    $('share-note').hidden=mode==='direct'; $('time-note').hidden=mode!=='direct';
    ['average','commission','share'].forEach(k=>document.querySelector('[data-field="'+k+'"]').hidden=mode==='direct');
    document.querySelector('[data-field="minutes"]').hidden=mode!=='direct';
  }
  $('scenario-form').addEventListener('input',()=>{update();event('calculator_interaction');});
  $('scenario-form').addEventListener('submit',e=>e.preventDefault());
  $('scenario-plan').addEventListener('change',()=>event('calculator_interaction'));
  document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;document.querySelectorAll('[data-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b))); update();event('calculator_interaction');}));
  update();
  let count=0, stage=0;
  function notification(quantity) {
    const n=c.notificationLabels;
    return `${n.title}\n\n${c.dish} × ${quantity}\n\n${n.total}: ${money(quantity*45000)}\n\n${n.customer}: ${n.guest}\n${n.phone}: +998 XX XXX XX XX\n${n.address}: ${n.addressValue}\n${n.source}: ${n.sourceValue}`;
  }
  function step(n) {stage=n;document.querySelectorAll('[data-step]').forEach((li,i)=>{if(i===n)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');});}
  $('demo-open').onclick=()=>{$('demo-open').hidden=true;$('demo-preview').hidden=true;$('demo-menu').hidden=false;step(1);$('demo-dish').focus();event('demo_start');};
  $('demo-dish').onclick=()=>{$('demo-selected').hidden=false;$('demo-add').disabled=false;step(2);};
  $('demo-add').onclick=()=>{count=Math.min(count+1,20);$('demo-cart').textContent=c.cart+': '+count+' · '+money(count*45000);$('demo-checkout').disabled=false;step(3);};
  $('demo-checkout').onclick=()=>{if(!count)return;$('demo-menu').hidden=true;$('demo-notification').hidden=false;$('demo-quantity').textContent=String(count);$('demo-message').textContent=notification(count);$('telegram-sample').textContent=notification(count);$('demo-status').textContent=c.received;step(4);$('demo-accept').focus();};
  $('demo-accept').onclick=()=>{$('demo-status').textContent=c.accepted;$('demo-accept').hidden=true;$('demo-ready').hidden=false;step(5);$('demo-ready').focus();};
  $('demo-ready').onclick=()=>{$('demo-status').textContent=c.complete;$('demo-ready').hidden=true;document.querySelector('.imagine').setAttribute('tabindex','-1');document.querySelector('.imagine').focus();event('demo_completion');};
  $('demo-reset').onclick=()=>{count=0;step(0);$('demo-preview').hidden=false;$('demo-open').hidden=false;$('demo-menu').hidden=true;$('demo-notification').hidden=true;$('demo-selected').hidden=true;$('demo-add').disabled=true;$('demo-checkout').disabled=true;$('demo-cart').textContent=c.empty;$('demo-accept').hidden=false;$('demo-ready').hidden=true;$('demo-status').textContent='';$('demo-open').focus();};
  step(0);
  if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){event('pricing_view');observer.disconnect();}},{threshold:0.2});observer.observe($('pricing'));}
  const form=$('lead-form'); let started=false, csrf=null, requestId=null;
  if(form) {
  form.addEventListener('focusin',()=>{if(!started){event('lead_form_start');started=true;}});
  form.addEventListener('input',()=>{requestId=null;});
  form.addEventListener('submit',async e=>{
    e.preventDefault(); const status=$('lead-status'), submit=form.querySelector('[type="submit"]');
    const venue=form.elements.venue.value.trim(),contact=form.elements.contact.value.trim();
    const validContact=/^@[A-Za-z][A-Za-z0-9_]{4,31}$/.test(contact)||(/^[+\d\s()\-]+$/.test(contact)&&contact.replace(/\D/g,'').length>=7&&contact.replace(/\D/g,'').length<=15);
    if(venue.length<2||!validContact||!form.elements.consent.checked){status.textContent=c.invalid;event('lead_form_error');return;}
    submit.disabled=true;status.textContent=c.saving;
    try {
      if(!csrf){const response=await fetch('/api/session',{cache:'no-store'});if(!response.ok)throw Error();const session=await response.json();csrf=session.csrf; if(typeof csrf!=='string')throw Error();}
      if(!requestId)requestId=crypto.randomUUID();
      const response=await fetch('/api/leads',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({venue,contact,consent:true,website:form.elements.website.value,locale:document.documentElement.lang,request_id:requestId}),signal:AbortSignal.timeout(15000)});
      const result=await response.json();
      if(!response.ok||result.saved!==true)throw Error();
      status.textContent=result.notification==='delivered'?c.saved:c.queued;
      form.reset();requestId=null;event('lead_form_success');
    } catch {status.textContent=c.error;csrf=null;event('lead_form_error');} finally {submit.disabled=false;}
  });
  }
  const mobile=document.querySelector('.mobile-contact');if(mobile){mobile.href='#contacts';mobile.removeAttribute('target');mobile.textContent=c.submit;const refresh=()=>{const interactive=['calculator','demo'].some(id=>{const r=$(id).getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;});mobile.classList.toggle('is-visible',!interactive&&document.querySelector('.hero').getBoundingClientRect().bottom<0&&$('contacts').getBoundingClientRect().top>innerHeight&&!/INPUT|SELECT/.test(document.activeElement.tagName));};addEventListener('scroll',refresh,{passive:true});document.addEventListener('focusin',refresh);document.addEventListener('focusout',()=>setTimeout(refresh,0));}
})();
