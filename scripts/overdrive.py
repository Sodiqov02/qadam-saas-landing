"""Conversion presentation layered onto the retained funnel and historical templates."""
from html import escape as e
import re
from urllib.parse import quote

COPY = {
'ru': dict(
 hero=['Принимайте заказы.','Без лишних звонков.','Без путаницы.'],
 intro='Гость выбирает блюда в вашем онлайн-меню. Вы получаете состав заказа и контакт в одном сообщении. Под брендом вашего ресторана.',
 brand='Ваши клиенты. Ваши заказы. Ваши правила.', risk='Демонстрация бесплатно. Без обязательств.',
 variantA='Принимайте заказы напрямую. Сокращайте комиссии за своих клиентов.',
 variantB='От меню до заказа — без долгой переписки и потерянных деталей.',
 calcCTA='Рассчитать выгоду для моего ресторана',
 calcFollow='Рассчитаем итоговую выгоду с учётом вашего тарифа, оплаты и доставки.',
 results=['Оборот существующих заказов / 30 дней','Из него перейдёт в прямой канал','Потенциально можно избежать комиссии / месяц'],
 calcNote='Оценка за 30 дней, не чистая прибыль. Прямые заказы — часть существующего оборота, а не новые продажи. Тариф, эквайринг и доставка оплачиваются отдельно.',
 planNote='Подключение — 300 000 сум. Обслуживание — $10 в месяц или 5% по условиям тарифа. Эквайринг отдельно. Курс и правила начисления согласуем до оплаты.',
 finalText='Покажем меню, приём заказов и подходящий вариант подключения. Бесплатно и без обязательств.',
 personal='Хочу увидеть своё меню', imagine='Представьте это меню с названием вашего ресторана.',
 preview='Ваш ресторан · тестовое меню', previewText='Выберите блюдо, соберите корзину и посмотрите, что получит сотрудник.',
 telegramTitle='Сразу понятно: что готовить и кому передать.', telegramText='Состав, количество, сумма и контакт гостя в одном сообщении. Настроим бота и проверим доставку уведомлений при подключении.',
 simulation='Пример уведомления · синтетические данные', notification='Telegram · пример заказа',
 setup='Подключение · 300 000 сум', recurring='Далее — один из двух тарифов',
 included='В составе подключения: онлайн-меню, корзина, настройка приёма заказов и доступ к управлению меню.',
 separate='Отдельно: эквайринг и организация доставки. Дополнительные услуги согласуем до оплаты.',
 pricingCTA='Посмотреть демо и выбрать тариф',
 expansionTitle='Сначала — ваш рабочий канал заказов.',
 expansion='Нужны онлайн-оплата, бронирование или меню внутри Telegram? Обсудим отдельный объём работ и сроки. Эти возможности не включены в демонстрацию и не подключаются автоматически.',
 featuresTitle='Гостю удобно заказать. Вам — принять.',
 features=[['Меню под вашим брендом','Ссылка для ваших гостей: блюда, фотографии, цены и корзина.'],['Детали в одном месте','Сотруднику проще увидеть состав и контакт, чем собирать их из переписки.'],['Меню под вашим контролем','Меняйте блюда и цены через панель управления.']],
 queued='Заявка сохранена. Следующий шаг — обсудить ваше меню и условия подключения. Если хотите связаться сейчас, напишите нам в Telegram.',
 saved='Заявка сохранена, команда получила уведомление. Далее обсудим ваше меню и вариант подключения.',
 faqUpdates={3:'Заказы можно получать в Telegram. При подключении настроим бота и проверим уведомления на тестовом заказе. На этой странице — безопасная симуляция.',6:'Онлайн-оплата пока не входит в рабочий сценарий заказа. Возможность подключения, сроки и комиссии согласуем отдельно.'}),
'en': dict(
 hero=['Take orders.','Skip the back-and-forth.','Keep every detail.'],
 intro='Guests choose dishes from your online menu. Your team gets the order details and customer contact in one message. All under your restaurant’s brand.',
 brand='Your customers. Your orders. Your rules.', risk='Free demonstration. No commitment.',
 variantA='Take orders directly. Reduce commissions on customers who already know you.',
 variantB='From menu to order, without lengthy chats or missing details.',
 calcCTA='Work out the benefit for my restaurant', calcFollow='We’ll review the benefit with your service plan, payment and delivery costs.',
 results=['Existing order turnover / 30 days','Share moving to your direct channel','Potential commission avoided / month'],
 calcNote='A 30-day scenario, not net profit. Direct orders are a share of existing turnover, not additional sales. Service fees, acquiring and delivery are separate.',
 planNote='Setup: 300,000 UZS. Service: $10 monthly or 5% under the plan terms. Acquiring is separate. Exchange rate and charging rules are agreed before payment.',
 finalText='See the menu, order workflow and a setup option that suits your restaurant. Free, with no commitment.',
 personal='Show me my own menu', imagine='Picture this menu with your restaurant’s name.',
 preview='Your restaurant · sample menu', previewText='Choose a dish, build your cart and see what your team receives.',
 telegramTitle='Know what to prepare, and who it’s for.', telegramText='Items, quantities, total and customer contact in one message. Bot setup and notification delivery are checked during onboarding.',
 simulation='Notification example · synthetic data', notification='Telegram · sample order',
 setup='Setup · 300,000 UZS', recurring='Then choose one service plan',
 included='Setup includes an online menu, cart, order intake configuration and menu management access.',
 separate='Separate costs: payment processing and delivery operations. Any additional services are agreed before payment.',
 pricingCTA='See a demo and choose a plan', expansionTitle='Start with your own ordering channel.',
 expansion='Need online payments, reservations or a menu inside Telegram? We can discuss a separate scope and timeline. These options are outside this demo and are not connected automatically.',
 featuresTitle='Easy for guests. Clear for your team.',
 features=[['Your brand, your menu','Share one link with your guests: dishes, photos, prices and a cart.'],['Order details together','See the items and customer contact without piecing together a chat.'],['You control the menu','Update dishes and prices through the management panel.']],
 queued='Request saved. Next, we’ll discuss your menu and setup options. You can also message us on Telegram now.',
 saved='Request saved and our team has been notified. Next, we’ll discuss your menu and setup options.',
 faqUpdates={3:'Receive orders in Telegram. During onboarding, we configure the bot and check delivery with a test order. This page uses a safe simulation.',6:'Online payment is not yet part of the working checkout flow. Availability, timing and processing fees need a separate agreement.'}),
'uz': dict(
 hero=['Buyurtmalarni qabul qiling.','Ortiqcha qo‘ng‘iroqlarsiz.','Chalkashliklarsiz.'],
 intro='Mehmon onlayn menyuingizdan taom tanlaydi. Siz buyurtma tarkibi va mijozning aloqa ma’lumotini bitta xabarda olasiz. Restoraningiz brendi ostida.',
 brand='Mijozlar sizniki. Buyurtmalar sizniki. Qoidalar sizniki.', risk='Namoyish bepul. Hech qanday majburiyatsiz.',
 variantA='Buyurtmalarni bevosita oling. O‘z mijozlaringiz uchun komissiyani kamaytiring.',
 variantB='Menyudan buyurtmagacha — uzoq yozishmalarsiz va yo‘qolgan tafsilotlarsiz.',
 calcCTA='Restoranim uchun foydasini hisoblash', calcFollow='Tarif, to‘lov va yetkazib berish xarajatlarini hisobga olib, yakuniy manfaatni birga baholaymiz.',
 results=['Mavjud buyurtmalar aylanmasi / 30 kun','Shundan bevosita kanalga o‘tadigan qismi','Oyiga tejash mumkin bo‘lgan komissiya'],
 calcNote='30 kunlik taxmin, sof foyda emas. Bevosita buyurtmalar — mavjud aylanmaning bir qismi, yangi savdo emas. Tarif, ekvayring va yetkazib berish alohida to‘lanadi.',
 planNote='Ulanish — 300 000 so‘m. Xizmat — oyiga $10 yoki tarif shartlariga ko‘ra 5%. Ekvayring alohida. Kurs va hisoblash qoidalarini to‘lovdan oldin kelishamiz.',
 finalText='Menyu, buyurtma qabul qilish jarayoni va sizga mos ulanish variantini ko‘rsatamiz. Bepul va majburiyatsiz.',
 personal='O‘z menyuimni ko‘rmoqchiman', imagine='Bu menyuda restoraningiz nomini tasavvur qiling.',
 preview='Sizning restoraningiz · sinov menyusi', previewText='Taom tanlang, savatni to‘ldiring va xodimingiz qanday xabar olishini ko‘ring.',
 telegramTitle='Nima tayyorlash va kimga topshirish — aniq.', telegramText='Taomlar, soni, jami summa va mijoz bilan aloqa bitta xabarda. Ulanishda botni sozlab, xabar yetib borishini tekshiramiz.',
 simulation='Bildirishnoma namunasi · sun’iy ma’lumotlar', notification='Telegram · buyurtma namunasi',
 setup='Ulanish · 300 000 so‘m', recurring='So‘ng ikki tarifdan birini tanlang',
 included='Ulanishga onlayn menyu, savat, buyurtma qabul qilishni sozlash va menyuni boshqarish paneli kiradi.',
 separate='Alohida xarajatlar: ekvayring va yetkazib berishni tashkil qilish. Qo‘shimcha xizmatlar to‘lovdan oldin kelishiladi.',
 pricingCTA='Demoni ko‘rib, tarif tanlash', expansionTitle='Avval — o‘z buyurtma kanalingiz.',
 expansion='Onlayn to‘lov, stol band qilish yoki Telegram ichidagi menyu kerakmi? Ish hajmi va muddatini alohida muhokama qilamiz. Bu imkoniyatlar demoga kirmaydi va avtomatik ulanmaydi.',
 featuresTitle='Mehmonga qulay. Xodimga tushunarli.',
 features=[['O‘z brendingizdagi menyu','Mehmonlaringiz uchun bitta havola: taomlar, rasmlar, narxlar va savat.'],['Tafsilotlar bir joyda','Xodim taomlar va mijoz bilan aloqani yozishmalardan izlab o‘tirmaydi.'],['Menyu sizning nazoratingizda','Boshqaruv panelida taomlar va narxlarni o‘zgartiring.']],
 queued='Ariza saqlandi. Keyingi qadam — menyuingiz va ulanish shartlarini muhokama qilish. Hozir bog‘lanish uchun Telegramda yozishingiz mumkin.',
 saved='Ariza saqlandi, jamoaga xabar yetkazildi. Keyin menyuingiz va ulanish variantini muhokama qilamiz.',
 faqUpdates={3:'Buyurtmalarni Telegramda olish mumkin. Ulanishda botni sozlab, sinov buyurtmasida xabar yetib borishini tekshiramiz. Bu sahifada xavfsiz taqlid ishlatiladi.',6:'Onlayn to‘lov hali buyurtma jarayoniga ulanmagan. Ulanish imkoniyati, muddati va komissiyalar alohida kelishiladi.'}),
}

RELEASE = {
'ru': dict(
 notificationLabels=dict(title='🛎 Новый заказ №1042',total='Итого',customer='Клиент',phone='Телефон',address='Адрес',source='Источник',sourceValue='Онлайн-меню',guest='Тестовый гость',addressValue='Тестовый адрес'),
 simulation='Демонстрационные данные · подписи переведены',
 planBodies=['Знаете стоимость обслуживания заранее. Предсказуемые ежемесячные расходы на свой канал заказов.','Стоимость обслуживания зависит от объёма заказов. Оплата связана с фактическими заказами согласно правилам тарифа.'],
 planTags=['ПЛАНИРУЙТЕ РАСХОДЫ','ПЛАТИТЕ ОТ ОБЪЁМА'],
 commercialRules='Правила начисления 5% и курс расчёта долларового тарифа согласуем до оплаты.',
 trustTitle='Сначала посмотрите. Потом решайте.',
 trustItems=[['Попробуйте заказ','#demo'],['Сравните условия','#pricing'],['Посмотрите подключение','#start']],
 owner='Прямой контакт с владельцем QadamUp',
 contactCTA='Обсудить моё меню в Telegram',
 contactText='Откроется чат с владельцем QadamUp и текстом для запроса показа. Отправьте сообщение в Telegram — это ваш следующий шаг.',
 draft='Здравствуйте! Хочу посмотреть QadamUp для своего заведения. Покажите меню, приём заказов и подходящий тариф.',
 draftLabel='Текст для сообщения',
 localOnly='Автоматическая форма пока доступна только в локальном режиме. Здесь запрос демонстрации — через Telegram.',
 ),
'uz': dict(
 notificationLabels=dict(title='🛎 Yangi buyurtma №1042',total='Jami',customer='Mijoz',phone='Telefon',address='Manzil',source='Manba',sourceValue='Onlayn menyu',guest='Sinov mehmoni',addressValue='Sinov manzili'),
 simulation='Namoyish ma’lumotlari · yozuvlar tarjima qilingan',
 planBodies=['Xizmat narxini oldindan bilasiz. O‘z buyurtma kanalingiz uchun oylik xarajatni rejalashtiring.','Xizmat narxi buyurtmalar hajmiga bog‘liq. To‘lov tarif qoidalariga ko‘ra amaldagi buyurtmalar asosida hisoblanadi.'],
 planTags=['XARAJATNI REJALASHTIRING','BUYURTMA HAJMIGA QARAB'],
 commercialRules='5% hisoblash qoidalari va dollar tarifini to‘lash kursi to‘lovdan oldin kelishiladi.',
 trustTitle='Avval sinab ko‘ring. Keyin qaror qiling.',
 trustItems=[['Buyurtmani sinab ko‘ring','#demo'],['Shartlarni solishtiring','#pricing'],['Ulanish bosqichlarini ko‘ring','#start']],
 owner='QadamUp egasi bilan bevosita aloqa',
 contactCTA='Menyuimni Telegramda muhokama qilish',
 contactText='QadamUp egasi bilan chat va namoyish so‘rash uchun tayyor matn ochiladi. Keyingi qadam — xabarni Telegramda yuborish.',
 draft='Assalomu alaykum! Muassasam uchun QadamUp namoyishini ko‘rmoqchiman. Menyu, buyurtma qabul qilish va mos tarifni ko‘rsatib bering.',
 draftLabel='Xabar uchun matn',
 localOnly='Avtomatik ariza shakli hozircha faqat lokal rejimda ishlaydi. Bu yerda namoyishni Telegram orqali so‘rashingiz mumkin.',
 ),
'en': dict(
 notificationLabels=dict(title='🛎 New order #1042',total='Total',customer='Customer',phone='Phone',address='Address',source='Source',sourceValue='Online menu',guest='Test guest',addressValue='Test address'),
 simulation='Demo data · localized labels',
 planBodies=['Know your service fee in advance. Plan predictable monthly spending for your own ordering channel.','Your service fee follows order volume. Charges are linked to actual orders under the agreed plan rules.'],
 planTags=['PLAN YOUR SPENDING','LINK FEES TO ORDER VOLUME'],
 commercialRules='The 5% charging rules and exchange rate for the dollar plan are agreed before payment.',
 trustTitle='Try it first. Decide when you’re ready.',
 trustItems=[['Try an order','#demo'],['Compare the terms','#pricing'],['See the setup steps','#start']],
 owner='Contact the QadamUp owner directly',
 contactCTA='Discuss my menu on Telegram',
 contactText='Open a chat with the QadamUp owner and a draft demo request. Send the message in Telegram to start the conversation.',
 draft='Hello! I’d like to see QadamUp for my restaurant. Please show me the menu, ordering workflow and a suitable service plan.',
 draftLabel='Message draft',
 localOnly='The automatic request form is currently available in local mode only. Request your demonstration through Telegram here.',
 )}

def enrich(lang, c):
    c.update(COPY[lang])
    c.update(RELEASE[lang])
    for index, answer in c['faqUpdates'].items():
        c['faq'][index][1] = answer

def message(c, lang, count=1):
    # Localized presentation of actual notify_admin fields; not a delivered message.
    n=c['notificationLabels']
    amount=f'{45000*count:,}' if lang=='en' else f'{45000*count:,}'.replace(',',' ')
    currency={'ru':'сум','uz':'so‘m','en':'UZS'}[lang]
    return f"{n['title']}\n\n{c['dish']} × {count}\n\n{n['total']}: {amount} {currency}\n\n{n['customer']}: {n['guest']}\n{n['phone']}: +998 XX XXX XX XX\n{n['address']}: {n['addressValue']}\n{n['source']}: {n['sourceValue']}"

def present(s, lang, c):
    s=s.replace('<h1 id="hero-title">','<h1 id="hero-title" data-hero>')
    s=s.replace('<div class="hero-copy">','<div class="hero-copy"><p class="brand-promise">'+e(c['brand'])+'</p>')
    s=s.replace('<ul class="hero-benefits">','<p class="risk-note">'+e(c['risk'])+'</p><ul class="hero-benefits">')
    # Hide no unknown savings behind large empty figures; keep the measured commission.
    s=re.sub(r'<div class="result-row"><dt>[^<]*</dt><dd><output id="money-[34]">.*?</div>','',s)
    s=s.replace('href="#demo">'+e(c['how'])+' ↘','href="#contacts">'+e(c['calcCTA'])+' ↘')
    s=s.replace('<label for="scenario-plan">','<p class="calc-follow">'+e(c['calcFollow'])+'</p><details class="calc-terms"><summary>'+e(c['planLabel'])+'</summary><label for="scenario-plan">')
    s=s.replace(e(c['calcNote'])+'</p></div><div id="time-results"',e(c['calcNote'])+'</p></details></div><div id="time-results"')
    s=s.replace('<div id="money-results">','<div id="money-results" aria-live="polite" aria-atomic="true">')
    s=s.replace('<div id="time-results" hidden>','<div id="time-results" aria-live="polite" aria-atomic="true" hidden>')
    # First state is a useful preview rather than an empty handset.
    preview=f'<div id="demo-preview"><img src="assets/demo-burger.webp" width="640" height="360" loading="lazy" alt="{e(c["dish"])}"><h3>{e(c["preview"])}</h3><p>{e(c["previewText"])}</p></div>'
    s=s.replace('<button id="demo-open"',preview+'<button id="demo-open"')
    s=s.replace('<div id="demo-notification" hidden>','<div id="demo-notification" hidden><pre class="telegram-message" id="demo-message"></pre>')
    s=s.replace('<a class="btn btn-primary" href="#contacts">'+e(c['personal']),'<p class="imagine">'+e(c['imagine'])+'</p><a class="btn btn-primary" href="#contacts">'+e(c['personal']))
    telegram=f'''<section class="dark-section" id="telegram"><div class="container telegram-layout"><div><p class="eyebrow">TELEGRAM / QADAMUP</p><h2>{e(c['telegramTitle'])}</h2><p class="lead">{e(c['telegramText'])}</p><p class="demo-disclosure">{e(c['simulation'])}</p><a class="btn btn-primary" href="#demo">{e(c['demo'])} ↗</a></div><figure class="telegram-window"><div class="telegram-bar"><span class="telegram-avatar" aria-hidden="true">Q</span><span>QadamUp<br><small>{e(c['notification'])}</small></span></div><pre class="telegram-message" id="telegram-sample">{e(message(c,lang))}</pre><figcaption>{e(c['simulation'])}</figcaption></figure></div></section>'''
    s=re.sub(r'<section class="dark-section" id="telegram">.*?</section>',lambda _:telegram,s,flags=re.S)
    s=re.sub(r'<section class="section container feature-split".*?</section>','',s,flags=re.S)
    features=f'''<section class="features-section" id="features" aria-labelledby="features-title"><div class="container features-benefits"><h2 id="features-title">{e(c['featuresTitle'])}</h2><div class="features-grid">{''.join('<article class="feature"><span class="feature-number">0'+str(i+1)+'</span><h3>'+e(t)+'</h3><p>'+e(b)+'</p></article>' for i,(t,b) in enumerate(c['features']))}</div><details class="expansion"><summary>{e(c['expansionTitle'])}</summary><p>{e(c['expansion'])}</p></details></div></section>'''
    s=re.sub(r'<section class="features-section".*?</section>',lambda _:features,s,flags=re.S)
    pricing=f'''<section class="pricing-section" id="pricing"><div class="container"><p class="eyebrow">QADAMUP / 03</p><h2>{e(c['pricingTitle'])}</h2><div class="setup-banner"><strong>{e(c['setup'])}</strong><span>{e(c['recurring'])}</span></div><div class="plans">{''.join(f'<article class="plan"><p class="eyebrow">0{i+1}</p><h3>{e(t)}</h3><p>{e(b)}</p><a class="btn btn-primary" data-event="pricing_cta_click" href="#contacts">{e(c["pricingCTA"])}</a></article>' for i,(t,b) in enumerate(zip(c['plans'],c['planBodies'])))}</div><div class="pricing-terms"><p>{e(c['included'])}</p><p>{e(c['separate'])}</p><p>{e(c['planNote'])}</p></div></div></section>'''
    s=re.sub(r'<section class="pricing-section".*?</section>',lambda _:pricing,s,flags=re.S)
    # Distinguish the commercial models without inventing different feature sets.
    for i,tag in enumerate(c['planTags']):
        s=s.replace(f'<p class="eyebrow">0{i+1}</p><h3>',f'<p class="eyebrow">{e(tag)}</p><h3>')
    s=s.replace(e(c['planNote'])+'</p></div></div></section>',e(c['commercialRules'])+'</p></div></div></section>')
    trust=f'<aside class="trust-proof container" id="trust"><h2>{e(c["trustTitle"])}</h2><ul>'+''.join(f'<li><a href="{href}">{e(label)} ↗</a></li>' for label,href in c['trustItems'])+f'</ul><a class="owner-contact" href="https://t.me/hacker_ronin" target="_blank" rel="noopener noreferrer">{e(c["owner"])} ↗</a></aside>'
    s=s.replace('<section class="section container" id="start">',trust+'<section class="section container" id="start">')
    if c.get('contactMode')=='telegram':
        url='https://t.me/hacker_ronin?text='+quote(c['draft'],safe='')
        fallback=f'<div class="contact-fallback"><p>{e(c["contactText"])}</p><a id="lead-telegram" class="btn btn-primary" data-event="telegram_contact_click" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(c["contactCTA"])} ↗</a><details><summary>{e(c["draftLabel"])}</summary><p class="message-draft">{e(c["draft"])}</p></details><p class="fine-print">{e(c["localOnly"])}</p></div>'
        s=re.sub(r'<form id="lead-form">.*?</form>',lambda _:fallback,s,flags=re.S)
    return s
