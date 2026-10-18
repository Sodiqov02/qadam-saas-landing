"""Generate three complete static HTML pages. No runtime translation dependency."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = {
'ru': {
'title':'QadamUp — онлайн-заказы для кафе и ресторанов',
'description':'Собственный канал онлайн-заказов для вашего заведения: меню, корзина и управление блюдами. Обсудите подключение QadamUp в Telegram.',
'nav':['Продукт','Расчёт затрат','Условия','Вопросы'], 'contact':'Обсудить подключение', 'skip':'Перейти к содержимому',
'eyebrow':'ОНЛАЙН-ЗАКАЗЫ ДЛЯ КАФЕ И РЕСТОРАНОВ',
'hero':['Ваш ресторан.','Ваши заказы.','Ваши правила.'],
'intro':'Создайте собственный канал онлайн-заказов с удобным меню, корзиной и уведомлениями в Telegram. Вашим гостям не нужно устанавливать отдельное приложение.',
'preview':'Посмотреть интерфейс', 'live':'Живое демо недоступно', 'liveNote':'Публичное демо пока не запущено. Ниже — реальные интерфейсы с тестовыми данными.',
'benefits':['Меню под вашим брендом','Заказы в Telegram','Управление блюдами и ценами'],
'caption':'Реальный интерфейс · демонстрационные данные', 'phoneTag':'МЕНЮ В КАРМАНЕ ГОСТЯ',
'strip':['Для кафе','Для ресторанов','Для чайхан','Для небольших кухонь'],
'problemLabel':'СВОЙ КАНАЛ ПРОДАЖ', 'problemTitle':'Ближе к гостям. Больше контроля.',
'problemText':'Развивайте собственный канал заказов, а не только продажи через посредников. Агрегаторы помогают находить покупателей; QadamUp — принимать прямые заказы от гостей, которые уже знают ваше заведение.',
'comparison':['Через посредника','Через QadamUp'],
'middle':['Комиссия по условиям платформы','Зависимость от стороннего сервиса','Процесс заказа по правилам платформы'],
'direct':['Онлайн-меню вашего заведения','Прямое оформление заказов','Управление собственным каналом продаж'],
'calcLabel':'ПОСЧИТАЕМ ВМЕСТЕ', 'calcTitle':'Сколько стоит ваш текущий канал онлайн-продаж?',
'calcText':'Введите свои данные. Расчёт показывает расходы существующего канала, а не обещанную экономию от перехода.',
'inputs':['Заказов в месяц','Средний чек, сум','Комиссия сервиса, %','Доставка одного заказа, сум','Прочие расходы в месяц, сум'],
'outputs':['Расчётный оборот','Комиссия сервиса','Доставка','Прочие расходы','Итого расходов в месяц'],
'calcNote':'Считаем, что доставка оплачивается заведением для каждого заказа и не включена в комиссию. Прочие расходы — за весь месяц. Себестоимость блюд, налоги и тариф QadamUp в расчёт не входят.',
'calcEmpty':'Заполните поля для расчёта. Если расходов нет, укажите 0.', 'calcError':'Проверьте значения: только неотрицательные числа; заказы — целое число, комиссия — от 0 до 100%.',
'calcCTA':'Получить персональный расчёт', 'currency':'сум', 'nojs':'Для интерактивного расчёта включите JavaScript. Все описания и контакты доступны без него.',
'menuLabel':'01 / ОНЛАЙН-МЕНЮ', 'menuTitle':'Ваше меню всегда под рукой у гостя.',
'menuText':'Фотографии, категории, понятные цены и корзина. Гость выбирает блюда в браузере — без установки приложения.',
'menuPoints':['Фотографии и описания блюд','Категории для удобного выбора','Корзина и оформление заказа'], 'menuCTA':'Рассмотреть меню и корзину',
'menuAlt':'Меню Qadam Demo: категории, фотографии блюд и кнопки добавления в корзину', 'cartAlt':'Корзина Qadam Demo с тестовым блюдом и формой оформления',
'telegramLabel':'02 / ПРИЁМ ЗАКАЗОВ', 'telegramTitle':'Новый заказ — в привычном Telegram.',
'telegramText':'В продукте реализованы уведомления для заведения с деталями заказа. Настройку бота и рабочий сценарий согласуем при подключении.',
'flow':['Гость выбирает блюда','Оформляет заказ','Заведение получает уведомление'],
'telegramNote':'Статическая демонстрация показывает интерфейс: она не отправляет реальные заказы и сообщения в Telegram.',
'adminLabel':'03 / УПРАВЛЕНИЕ', 'adminTitle':'Обновляйте меню без помощи разработчика.',
'adminText':'В административной панели реализованы управление блюдами, ценами, описаниями и категориями. Доступ к панели предоставляется отдельно.',
'adminCaption':'Реальный шаблон админ-панели · изолированные тестовые данные, без подключения к базе',
'adminAlt':'Административная панель Qadam: категории, редактор блюда и список меню с тестовыми данными',
'featuresLabel':'ВОЗМОЖНОСТИ ПЛАТФОРМЫ', 'featuresTitle':'Всё необходимое для заказов — в одной системе',
'featuresText':'От онлайн-меню до оплаты и бронирования. Подберём и настроим возможности под ваше заведение',
'features':[['Онлайн-меню и корзина','Гостю проще выбрать блюда и собрать заказ — без звонков и долгой переписки.'],['Бронирование столиков','Помогите гостям спланировать визит, а команде — подготовиться к их приходу.'],['Онлайн-оплата','Предложите гостям удобный способ оплаты при оформлении заказа.'],['Аналитика заказов','Оценивайте спрос на блюда и динамику заказов, чтобы планировать меню.'],['QR-меню','Откройте гостю быстрый путь к меню — достаточно навести камеру на QR-код.'],['Приём заказов на доставку','Собирайте заказы с адресом и пожеланиями гостя. Доставку организуете вы.']],
'featuresNote':'Состав функций и сроки подключения зависят от выбранного тарифа и необходимых настроек. Подробности уточняются перед запуском',
'featuresCTA':'Обсудить подключение', 'featuresAgreement':'Согласуем состав функций и сроки до оплаты.',
'stepsLabel':'КАК ПОДКЛЮЧИТЬСЯ', 'stepsTitle':'Начать проще, чем кажется.',
'steps':[['Познакомьтесь с интерфейсом','Посмотрите реальные экраны меню и корзины на этой странице.'],['Расскажите о заведении','Напишите владельцу QadamUp в Telegram о вашем меню и процессе заказов.'],['Согласуйте подключение','Обсудим необходимые функции, проверку рабочего сценария и условия.']],
'pricingLabel':'УСЛОВИЯ ПОДКЛЮЧЕНИЯ', 'pricingTitle':'Под масштаб вашего заведения.',
'pricingText':'Небольшая кухня или развивающаяся сеть — обсудим модель оплаты с учётом объёма заказов и необходимых возможностей.',
'plans':[['Небольшое заведение','Простой старт для собственного канала заказов.',['Онлайн-меню','Приём заказов','Подбор доступных условий']],['Растущий бизнес','Обсудим процессы и следующий этап развития.',['Больший объём заказов','Дополнительные возможности','Индивидуальное обсуждение интеграций']]],
'pricingNote':'Это сценарии подключения, а не утверждённые тарифные планы. Стоимость и состав функций согласуются индивидуально.', 'pricingCTA':'Узнать условия в Telegram',
'faqLabel':'ЧАСТЫЕ ВОПРОСЫ', 'faqTitle':'Разберёмся в деталях.',
'faq':[['Нужно ли гостю устанавливать приложение?','Нет. Меню и корзина открываются в браузере.'],['Можно ли редактировать меню самостоятельно?','В продукте есть административная панель для блюд, цен, описаний и категорий. Доступ и настройку обсудим при подключении.'],['Можно ли работать вместе с агрегаторами?','QadamUp можно рассматривать как дополнительный прямой канал заказов. Условия работы с другими платформами вы определяете отдельно.'],['Как заведение получает заказы?','В продукте реализована отправка уведомлений в Telegram. Для работы требуется настройка бота и проверка доставки сообщений. Статическая демонстрация сообщения не отправляет.'],['Как подключить заведение?','Напишите в Telegram владельцу QadamUp. Расскажите о заведении, меню и необходимых функциях — затем согласуем условия и рабочий сценарий.'],['Доступна ли онлайн-оплата?','Пока она не подключена к оформлению заказа. Есть отдельный sandbox-модуль для проверки интеграции; готовую оплату сейчас не предлагаем.'],['Сколько стоит обслуживание?','Утверждённых публичных тарифов пока нет. Стоимость обсуждается индивидуально в Telegram.']],
'finalLabel':'СДЕЛАЙТЕ СЛЕДУЮЩИЙ ШАГ', 'finalTitle':'Ваш следующий заказ может прийти напрямую.',
'finalText':'Познакомьтесь с QadamUp и узнайте, как организовать собственный канал онлайн-заказов для вашего заведения.', 'write':'Написать в Telegram', 'footer':'Собственный канал онлайн-заказов для вашего заведения.', 'back':'Наверх', 'locale':'ru-RU'
},
'uz': {
'title':'QadamUp — kafe va restoranlar uchun onlayn buyurtmalar',
'description':'Muassasangiz uchun o‘z onlayn buyurtma kanalingiz: menyu, savat va taomlarni boshqarish. QadamUp xizmatiga ulanishni Telegram orqali muhokama qiling.',
'nav':['Mahsulot','Xarajatlar','Shartlar','Savollar'], 'contact':'Ulanishni muhokama qilish', 'skip':'Asosiy mazmunga o‘tish',
'eyebrow':'KAFE VA RESTORANLAR UCHUN ONLAYN BUYURTMALAR', 'hero':['Sizning restoraningiz.','Sizning buyurtmalaringiz.','Sizning qoidalaringiz.'],
'intro':'Qulay menyu, savat va Telegram bildirishnomalari yordamida o‘z onlayn buyurtma kanalingizni yarating. Mehmonlaringiz alohida ilova o‘rnatishi shart emas.',
'preview':'Interfeysni ko‘rish', 'live':'Jonli demo hozircha mavjud emas', 'liveNote':'Ommaviy demo hali ishga tushirilmagan. Quyida haqiqiy interfeyslar sinov ma’lumotlari bilan ko‘rsatilgan.',
'benefits':['Brendingizga mos menyu','Buyurtmalar Telegramda','Taomlar va narxlarni boshqarish'], 'caption':'Haqiqiy interfeys · namoyish ma’lumotlari', 'phoneTag':'MENYU MEHMONINGIZ QO‘LIDA',
'strip':['Kafelar uchun','Restoranlar uchun','Choyxonalar uchun','Kichik oshxonalar uchun'],
'problemLabel':'O‘Z SAVDO KANALINGIZ', 'problemTitle':'Mehmonlarga yaqinroq. Boshqaruv o‘z qo‘lingizda.',
'problemText':'Vositachilar orqali savdo bilan birga o‘z buyurtma kanalingizni ham rivojlantiring. Agregatorlar yangi xaridorlarni topishga yordam beradi, QadamUp esa sizni allaqachon biladigan mehmonlardan bevosita buyurtma olish uchun xizmat qiladi.',
'comparison':['Vositachi orqali','QadamUp orqali'], 'middle':['Platforma shartlariga muvofiq komissiya','Tashqi xizmatga bog‘liqlik','Platforma qoidalari asosida buyurtma'], 'direct':['Muassasangizning onlayn menyusi','Bevosita buyurtma berish','O‘z savdo kanalingizni boshqarish'],
'calcLabel':'BIRGA HISOBLAYMIZ', 'calcTitle':'Hozirgi onlayn savdo kanalingiz qancha turadi?',
'calcText':'O‘z ma’lumotlaringizni kiriting. Hisob hozirgi kanalingiz xarajatlarini ko‘rsatadi; QadamUp orqali aniq tejash va’da qilinmaydi.',
'inputs':['Bir oydagi buyurtmalar','O‘rtacha chek, so‘m','Xizmat komissiyasi, %','Bir buyurtma yetkazish narxi, so‘m','Boshqa oylik xarajatlar, so‘m'],
'outputs':['Hisoblangan aylanma','Xizmat komissiyasi','Yetkazib berish','Boshqa xarajatlar','Jami oylik xarajat'],
'calcNote':'Yetkazib berishni har bir buyurtma uchun muassasa to‘laydi va u komissiyaga kirmaydi deb hisoblaymiz. Boshqa xarajatlar bir oy uchun kiritiladi. Taom tannarxi, soliqlar va QadamUp narxi hisobga olinmaydi.',
'calcEmpty':'Hisoblash uchun maydonlarni to‘ldiring. Xarajat bo‘lmasa, 0 kiriting.', 'calcError':'Qiymatlarni tekshiring: manfiy bo‘lmagan sonlar; buyurtmalar butun son, komissiya 0 dan 100% gacha bo‘lishi kerak.',
'calcCTA':'Shaxsiy hisob-kitob olish', 'currency':'so‘m', 'nojs':'Interaktiv hisoblash uchun JavaScriptni yoqing. Tavsiflar va aloqa ma’lumotlari usiz ham ochiladi.',
'menuLabel':'01 / ONLAYN MENYU', 'menuTitle':'Menyuingiz doim mehmoningiz qo‘lida.', 'menuText':'Fotosuratlar, toifalar, tushunarli narxlar va savat. Mehmon taomlarni brauzerda tanlaydi — ilova o‘rnatish shart emas.',
'menuPoints':['Taom fotosuratlari va tavsiflari','Qulay tanlash uchun toifalar','Savat va buyurtmani rasmiylashtirish'], 'menuCTA':'Menyu va savatni ko‘rish', 'menuAlt':'Qadam Demo menyusi: toifalar, taom rasmlari va savatga qo‘shish tugmalari', 'cartAlt':'Sinov taomi va buyurtma shakli bilan Qadam Demo savati',
'telegramLabel':'02 / BUYURTMALARNI QABUL QILISH', 'telegramTitle':'Yangi buyurtma — odatiy Telegramingizda.', 'telegramText':'Mahsulotda muassasaga buyurtma tafsilotlarini yuboradigan bildirishnomalar yaratilgan. Bot sozlamalari va ish jarayoni ulanish paytida kelishiladi.',
'flow':['Mehmon taom tanlaydi','Buyurtmani rasmiylashtiradi','Muassasa bildirishnoma oladi'], 'telegramNote':'Statik namoyish interfeysni ko‘rsatadi: haqiqiy buyurtmalar va Telegram xabarlari yuborilmaydi.',
'adminLabel':'03 / BOSHQARUV', 'adminTitle':'Menyuni dasturchisiz yangilang.', 'adminText':'Boshqaruv panelida taomlar, narxlar, tavsiflar va toifalarni tahrirlash imkoniyati yaratilgan. Panelga kirish alohida taqdim etiladi.', 'adminCaption':'Haqiqiy boshqaruv paneli shabloni · bazaga ulanmagan sinov ma’lumotlari', 'adminAlt':'Qadam boshqaruv paneli: toifalar, taom muharriri va sinov menyusi',
'featuresLabel':'PLATFORMA IMKONIYATLARI', 'featuresTitle':'Buyurtmalar uchun kerakli imkoniyatlar — bir tizimda', 'featuresText':'Onlayn menyudan to‘lov va stol band qilishgacha. Muassasangizga mos imkoniyatlarni tanlab, sozlab beramiz',
'features':[['Onlayn menyu va savat','Mehmon qo‘ng‘iroq yoki uzoq yozishmalarsiz taom tanlab, buyurtma yig‘adi.'],['Stol band qilish','Mehmon tashrifini oldindan rejalashtirsin, jamoangiz esa uni kutib olishga tayyorlansin.'],['Onlayn to‘lov','Mehmonga buyurtma berish paytida qulay to‘lov usulini taklif qiling.'],['Buyurtmalar tahlili','Menyuni rejalashda taomlarga talab va buyurtmalar sonidagi o‘zgarishlarni hisobga oling.'],['QR-menyu','Mehmon kamerani QR-kodga qaratsa, menyuni tez ochishi mumkin.'],['Yetkazib berish uchun buyurtma qabul qilish','Buyurtmani manzil va mehmon izohlari bilan yig‘ing. Yetkazib berishni o‘zingiz tashkil qilasiz.']],
'featuresNote':'Funksiyalar tarkibi va ulanish muddati tanlangan tarif hamda kerakli sozlamalarga bog‘liq. Tafsilotlar ishga tushirishdan oldin kelishiladi',
'featuresCTA':'Ulanishni muhokama qilish', 'featuresAgreement':'Funksiyalar va muddatni to‘lovdan oldin kelishib olamiz.',
'stepsLabel':'QANDAY ULANISH MUMKIN', 'stepsTitle':'Boshlash siz o‘ylagandan oson.', 'steps':[['Interfeys bilan tanishing','Shu sahifada menyu va savatning haqiqiy ekranlarini ko‘ring.'],['Muassasangiz haqida yozing','QadamUp egasiga Telegramda menyu va buyurtma jarayoningiz haqida ayting.'],['Ulanishni kelishib oling','Kerakli funksiyalar, ish jarayonini tekshirish va shartlarni muhokama qilamiz.']],
'pricingLabel':'ULANISH SHARTLARI', 'pricingTitle':'Muassasangiz ko‘lamiga mos.', 'pricingText':'Kichik oshxona yoki rivojlanayotgan tarmoq — buyurtmalar hajmi va kerakli imkoniyatlarga qarab to‘lov shartlarini muhokama qilamiz.',
'plans':[['Kichik muassasa','O‘z buyurtma kanalingizni yo‘lga qo‘yish uchun.',['Onlayn menyu','Buyurtmalarni qabul qilish','Mos shartlarni tanlash']],['Rivojlanayotgan biznes','Jarayonlar va rivojlanishning keyingi bosqichini muhokama qilamiz.',['Ko‘proq buyurtmalar','Qo‘shimcha imkoniyatlar','Integratsiyalarni alohida muhokama qilish']]], 'pricingNote':'Bular tasdiqlangan tariflar emas, ulanish yo‘nalishlaridir. Narx va funksiyalar alohida kelishiladi.', 'pricingCTA':'Telegramda shartlarni bilish',
'faqLabel':'KO‘P SO‘RALADIGAN SAVOLLAR', 'faqTitle':'Tafsilotlarni aniqlashtiramiz.',
'faq':[['Mehmon ilova o‘rnatishi kerakmi?','Yo‘q. Menyu va savat brauzerda ochiladi.'],['Menyuni o‘zim tahrirlay olamanmi?','Mahsulotda taomlar, narxlar, tavsiflar va toifalar uchun boshqaruv paneli bor. Kirish va sozlamalarni ulanishda kelishamiz.'],['Agregatorlar bilan birga ishlatish mumkinmi?','QadamUp qo‘shimcha bevosita buyurtma kanali bo‘lishi mumkin. Boshqa platformalar bilan ishlash shartlarini alohida belgilaysiz.'],['Muassasa buyurtmani qanday oladi?','Mahsulotda Telegram bildirishnomalari yaratilgan. Ishlash uchun botni sozlash va xabarlar yetib borishini tekshirish zarur. Statik namoyish xabar yubormaydi.'],['Muassasani qanday ulash mumkin?','QadamUp egasiga Telegramda yozing. Muassasa, menyu va zarur funksiyalarni ayting — keyin shartlar va ish jarayonini kelishamiz.'],['Onlayn to‘lov mavjudmi?','Hozircha buyurtma jarayoniga ulanmagan. Integratsiyani tekshirish uchun alohida sandbox moduli bor; tayyor onlayn to‘lov hali taklif qilinmaydi.'],['Xizmat qancha turadi?','Tasdiqlangan ommaviy tariflar hozircha yo‘q. Narx Telegramda alohida muhokama qilinadi.']],
'finalLabel':'KEYINGI QADAMNI QO‘YING', 'finalTitle':'Keyingi buyurtmangiz bevosita kelishi mumkin.', 'finalText':'QadamUp bilan tanishing va muassasangiz uchun o‘z onlayn buyurtma kanalingizni qanday yo‘lga qo‘yishni bilib oling.', 'write':'Telegramda yozish', 'footer':'Muassasangiz uchun o‘z onlayn buyurtma kanalingiz.', 'back':'Yuqoriga', 'locale':'uz-UZ'
},
'en': {
'title':'QadamUp — online ordering for cafes and restaurants', 'description':'Your own online ordering channel: a branded menu, cart and menu management. Discuss connecting your restaurant with QadamUp on Telegram.',
'nav':['Product','Cost calculator','Terms','Questions'], 'contact':'Discuss getting started', 'skip':'Skip to content',
'eyebrow':'ONLINE ORDERING FOR CAFES AND RESTAURANTS', 'hero':['Your restaurant.','Your orders.','Your rules.'],
'intro':'Build your own online ordering channel with a convenient menu, cart and Telegram notifications. Your guests do not need to install another app.',
'preview':'Explore the interface', 'live':'Live demo unavailable', 'liveNote':'The public demo is not live yet. Below are real interfaces with test data.',
'benefits':['A menu under your brand','Orders in Telegram','Manage dishes and prices'], 'caption':'Real interface · demonstration data', 'phoneTag':'YOUR MENU, IN THEIR HANDS', 'strip':['For cafes','For restaurants','For teahouses','For small kitchens'],
'problemLabel':'YOUR OWN SALES CHANNEL', 'problemTitle':'Closer to guests. More control.', 'problemText':'Develop your own ordering channel alongside marketplace sales. Aggregators help people discover you; QadamUp helps you take direct orders from guests who already know your restaurant.',
'comparison':['Through a marketplace','Through QadamUp'], 'middle':['Commission under platform terms','Reliance on a third-party service','Ordering under platform rules'], 'direct':['Your restaurant’s online menu','Direct ordering','Control of your own sales channel'],
'calcLabel':'LET’S DO THE MATH', 'calcTitle':'What does your current online sales channel cost?', 'calcText':'Enter your figures. This estimates your existing channel’s expenses, without promising savings from switching.',
'inputs':['Orders per month','Average order, UZS','Service commission, %','Delivery per order, UZS','Other monthly expenses, UZS'], 'outputs':['Estimated turnover','Service commission','Delivery','Other expenses','Total monthly expenses'],
'calcNote':'Assumes your restaurant pays delivery for every order, separately from commission. Other expenses cover the whole month. Food costs, taxes and QadamUp fees are excluded.', 'calcEmpty':'Complete all fields to calculate. Enter 0 if an expense does not apply.', 'calcError':'Check the values: non-negative numbers only; orders must be whole numbers and commission must be between 0 and 100%.',
'calcCTA':'Request a personal estimate', 'currency':'UZS', 'nojs':'Enable JavaScript for the interactive calculation. All descriptions and contact links work without it.',
'menuLabel':'01 / ONLINE MENU', 'menuTitle':'Your menu, always within reach.', 'menuText':'Photos, categories, clear prices and a cart. Guests choose their food in a browser, without installing an app.', 'menuPoints':['Dish photos and descriptions','Categories for easy browsing','Cart and checkout'], 'menuCTA':'Explore menu and cart', 'menuAlt':'Qadam Demo menu with categories, dish photos and add-to-cart buttons', 'cartAlt':'Qadam Demo cart with a test dish and checkout form',
'telegramLabel':'02 / ORDER NOTIFICATIONS', 'telegramTitle':'A new order. Right in Telegram.', 'telegramText':'The product includes notifications with order details for your restaurant. Bot setup and the working flow are agreed during onboarding.', 'flow':['Guest chooses dishes','Places an order','Restaurant receives a notification'], 'telegramNote':'The static demonstration shows the interface. It sends no real orders or Telegram messages.',
'adminLabel':'03 / MENU MANAGEMENT', 'adminTitle':'Update your menu without a developer.', 'adminText':'The admin panel implements dish, price, description and category management. Access to the panel is provided separately.', 'adminCaption':'Actual admin template · isolated test data, no database connection', 'adminAlt':'Qadam admin panel with categories, dish editor and test menu data',
'featuresLabel':'PLATFORM CAPABILITIES', 'featuresTitle':'Everything you need for orders — in one system', 'featuresText':'From online menus to payments and table reservations. We’ll select and configure the right features for your restaurant',
'features':[['Online menu and cart','Make it easier for guests to choose dishes and build an order without calls or long message threads.'],['Table reservations','Help guests plan their visit and give your team time to prepare for their arrival.'],['Online payments','Offer guests a convenient way to pay when placing an order.'],['Order analytics','Understand demand for dishes and changes in order volume to help plan your menu.'],['QR menu','Give guests a quick route to your menu with a scan of a QR code.'],['Delivery order intake','Collect orders with the guest’s address and requests. You arrange the delivery.']],
'featuresNote':'Features and connection timelines depend on your plan and the setup required. Details are agreed before launch',
'featuresCTA':'Discuss getting connected', 'featuresAgreement':'We agree on features and timing before you pay.',
'stepsLabel':'HOW TO GET STARTED', 'stepsTitle':'A simple next step.', 'steps':[['Explore the interface','See real menu and cart screens on this page.'],['Tell us about your restaurant','Message the QadamUp owner on Telegram about your menu and ordering workflow.'],['Agree on setup','Discuss the features you need, workflow verification and terms.']],
'pricingLabel':'GETTING CONNECTED', 'pricingTitle':'Terms that fit your restaurant.', 'pricingText':'A small kitchen or a growing chain — discuss a payment model based on your order volume and the features you need.', 'plans':[['Small restaurant','A straightforward start for your own ordering channel.',['Online menu','Order intake','Discuss suitable terms']],['Growing business','Discuss your operations and the next stage of growth.',['Higher order volume','Additional capabilities','Individual integration discussions']]], 'pricingNote':'These are setup scenarios, not approved pricing plans. Pricing and included features are agreed individually.', 'pricingCTA':'Ask about terms on Telegram',
'faqLabel':'FREQUENTLY ASKED QUESTIONS', 'faqTitle':'Let’s clear things up.',
'faq':[['Do guests need to install an app?','No. The menu and cart open in a browser.'],['Can I edit the menu myself?','The product has an admin panel for dishes, prices, descriptions and categories. Access and setup are discussed during onboarding.'],['Can I use it alongside aggregators?','QadamUp can serve as an additional direct ordering channel. You determine your arrangements with other platforms separately.'],['How does the restaurant receive orders?','The product implements Telegram notifications. A bot must be configured and message delivery verified. The static demonstration sends no messages.'],['How do I connect my restaurant?','Message the QadamUp owner on Telegram. Tell us about your restaurant, menu and required features so we can agree on terms and workflow.'],['Are online payments available?','Not in checkout yet. There is a separate sandbox module for integration testing; ready-to-use online payments are not currently offered.'],['What does the service cost?','There are no approved public prices yet. Pricing is discussed individually on Telegram.']],
'finalLabel':'TAKE THE NEXT STEP', 'finalTitle':'Your next order could come direct.', 'finalText':'Get to know QadamUp and explore how to build your restaurant’s own online ordering channel.', 'write':'Message on Telegram', 'footer':'Your restaurant’s own online ordering channel.', 'back':'Back to top', 'locale':'en-US'
}}

def build(lang, d, *, write=False):
    if write:
        raise ValueError('Historical template is render-only. Run scripts/funnel.py to write current pages.')
    e = escape
    def t(key): return e(d[key])
    def contact(label, ghost=False):
        return f'<a class="btn {"btn-outline" if ghost else "btn-primary"}" href="https://t.me/hacker_ronin" target="_blank" rel="noopener noreferrer">{e(label)} <span aria-hidden="true">↗</span></a>'
    def items(values): return ''.join(f'<li>{e(v)}</li>' for v in values)
    def heading(label, title, text=''):
        return f'<p class="eyebrow">{e(label)}</p><h2>{e(title)}</h2>' + (f'<p class="lead">{e(text)}</p>' if text else '')
    filename = {'ru':'index.html','uz':'uz.html','en':'en.html'}[lang]
    url = 'https://qadamup.uz/' + ('' if lang=='ru' else filename)
    alternates = ''.join(f'<link rel="alternate" hreflang="{lc}" href="https://qadamup.uz/{"" if lc=="ru" else lc+".html"}">' for lc in DATA)
    languages = ''.join(f'<a href="{fn}" lang="{lc}" hreflang="{lc}" {"aria-current=\"page\"" if lc==lang else ""}>{lc.upper()}</a>' for lc,fn in [('ru','index.html'),('uz','uz.html'),('en','en.html')])
    nav = ''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor,label in zip(['product','calculator','pricing','faq'],d['nav']))
    fields = ''.join(f'<label for="{key}">{e(label)}<input id="{key}" name="{key}" type="number" min="0" max="{maximum}" step="{step}" inputmode="{mode}" placeholder="0" required></label>' for key,label,maximum,step,mode in zip(['orders','average','commission','delivery','other'],d['inputs'],[1000000,1000000000,100,1000000000,1000000000000],[1,'0.01','0.01','0.01','0.01'],['numeric','decimal','decimal','decimal','decimal']))
    results = ''.join(f'<div class="result-row {"result-total" if i==4 else ""}"><dt>{e(label)}</dt><dd><output id="result-{key}">—</output></dd></div>' for i,(key,label) in enumerate(zip(['turnover','commission','delivery','other','total'],d['outputs'])))
    feature_icons = [
        '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/>',
        '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 11h18m-13 4 3 3 5-5"/>',
        '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20M6 15h4"/>',
        '<path d="M4 3v17h17M8 15v-4m5 4V7m5 8v-3"/>',
        '<path d="M3 3h6v6H3zM15 3h6v6h-6zM3 15h6v6H3zM15 15h2v2h-2zm6 0v6h-6m2-2h4"/>',
        '<path d="M5 8h14l2 13H3L5 8zm3 0V6a4 4 0 0 1 8 0v2m-8 6h8"/>',
    ]
    features = ''.join(f'<article class="feature"><svg class="feature-icon" viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{icon}</svg><h3>{e(title)}</h3><p>{e(body)}</p></article>' for (title,body),icon in zip(d['features'],feature_icons))
    steps = ''.join(f'<li><span class="step-number">0{i+1}</span><h3>{e(title)}</h3><p>{e(body)}</p></li>' for i,(title,body) in enumerate(d['steps']))
    plans = ''.join(f'<article class="plan"><p class="eyebrow">0{i+1}</p><h3>{e(title)}</h3><p>{e(body)}</p><ul class="check-list">{items(points)}</ul>{contact(d["pricingCTA"],i==0)}</article>' for i,(title,body,points) in enumerate(d['plans']))
    faq = ''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in d['faq'])
    config = json.dumps({k:d[k] for k in ['locale','currency','calcEmpty','calcError']},ensure_ascii=False).replace('<','\\u003c')
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t('title')}</title><meta name="description" content="{t('description')}">
<link rel="canonical" href="{url}">{alternates}<link rel="alternate" hreflang="x-default" href="https://qadamup.uz/">
<meta property="og:type" content="website"><meta property="og:title" content="{t('title')}"><meta property="og:description" content="{t('description')}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://qadamup.uz/assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="theme-color" content="#102D22"><link rel="icon" href="favicon.ico"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css"><script src="main.js" defer></script></head>
<body id="top"><a class="skip-link" href="#main">{t('skip')}</a>
<header class="topbar container"><a class="brand" href="{filename}" aria-label="QadamUp"><span class="brand-mark" aria-hidden="true">q.</span><span>qadam<span class="brand-up">up</span><span class="brand-dot">.</span></span></a><nav class="desktop-nav" aria-label="QadamUp">{nav}</nav><nav class="language-switch" aria-label="RU / UZ / EN">{languages}</nav><a class="header-contact" href="https://t.me/hacker_ronin" target="_blank" rel="noopener noreferrer">Telegram ↗</a></header>
<main id="main">
<section class="hero container" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span class="dot" aria-hidden="true"></span>{t('eyebrow')}</p><h1 id="hero-title">{e(d['hero'][0])}<br>{e(d['hero'][1])}<br><span>{e(d['hero'][2])}</span></h1><p class="lead">{t('intro')}</p><div class="actions"><a class="btn btn-primary" href="#product">{t('preview')} <span aria-hidden="true">↘</span></a>{contact(d['contact'],True)}</div><ul class="hero-benefits">{items(d['benefits'])}</ul><div class="demo-note"><button class="demo-disabled" type="button" disabled aria-describedby="live-note">{t('live')}</button><p id="live-note">{t('liveNote')}</p></div></div>
<figure class="hero-figure"><div class="visual-grid" aria-hidden="true"></div><div class="visual-label">{t('phoneTag')}</div><div class="phone"><div class="phone-speaker" aria-hidden="true"></div><img src="assets/menu.webp" width="390" height="844" alt="{t('menuAlt')}" fetchpriority="high"></div><div class="visual-stamp" aria-hidden="true"><span>Q</span><span>MENU<br>→ CART</span></div><figcaption>{t('caption')}</figcaption></figure></section>
<div class="audience-strip"><div class="container">{''.join('<span>'+e(x)+'</span>' for x in d['strip'])}</div></div>
<section class="section container" id="how">{heading(d['problemLabel'],d['problemTitle'],d['problemText'])}<div class="comparison"><article><p class="comparison-symbol" aria-hidden="true">↗</p><h3>{e(d['comparison'][0])}</h3><ul>{items(d['middle'])}</ul></article><article class="comparison-direct"><p class="comparison-symbol" aria-hidden="true">q.</p><h3>{e(d['comparison'][1])}</h3><ul class="check-list">{items(d['direct'])}</ul></article></div></section>
<section class="calculator-section" id="calculator"><div class="container calculator-layout"><div>{heading(d['calcLabel'],d['calcTitle'],d['calcText'])}<form id="cost-form" novalidate><fieldset><legend class="sr-only">{t('calcTitle')}</legend><div class="fields">{fields}</div></fieldset></form><noscript><p class="notice">{t('nojs')}</p></noscript></div><div class="calculator-result"><p class="eyebrow">{e(d['outputs'][4])}</p><p class="calculator-status" id="calculator-status" aria-live="polite">{t('calcEmpty')}</p><dl>{results}</dl><p class="fine-print">{t('calcNote')}</p>{contact(d['calcCTA'])}</div></div></section>
<section class="section container product-layout" id="product"><div>{heading(d['menuLabel'],d['menuTitle'],d['menuText'])}<ul class="check-list">{items(d['menuPoints'])}</ul><a class="text-link" href="#screens">{t('menuCTA')} <span aria-hidden="true">↘</span></a></div><div class="screens" id="screens"><figure><a href="assets/menu.webp" target="_blank" rel="noopener noreferrer"><img src="assets/menu.webp" width="390" height="844" loading="lazy" alt="{t('menuAlt')}"></a><figcaption>{t('caption')}</figcaption></figure><figure class="cart-screen"><a href="assets/cart.webp" target="_blank" rel="noopener noreferrer"><img src="assets/cart.webp" width="390" height="844" loading="lazy" alt="{t('cartAlt')}"></a><figcaption>{t('caption')}</figcaption></figure></div></section>
<section class="dark-section" id="telegram"><div class="container">{heading(d['telegramLabel'],d['telegramTitle'],d['telegramText'])}<ol class="order-flow">{''.join(f'<li><span class="flow-icon" aria-hidden="true">{icon}</span><span>{e(label)}</span></li>' for icon,label in zip(['01','02','03'],d['flow']))}</ol><p class="dark-note">{t('telegramNote')}</p></div></section>
<section class="section container admin-section" id="management"><div class="admin-head">{heading(d['adminLabel'],d['adminTitle'],d['adminText'])}</div><figure class="admin-figure"><div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>Qadam / Menu management</span></div><a href="assets/admin.webp" target="_blank" rel="noopener noreferrer"><img src="assets/admin.webp" width="1280" height="900" loading="lazy" alt="{t('adminAlt')}"></a><figcaption>{t('adminCaption')}</figcaption></figure></section>
<section class="features-section" id="features" aria-labelledby="features-title"><div class="container features-benefits"><p class="eyebrow">{t('featuresLabel')}</p><h2 id="features-title">{t('featuresTitle')}</h2><p class="lead">{t('featuresText')}.</p><div class="features-grid">{features}</div><div class="features-connect"><a class="btn btn-primary" href="#contacts">{t('featuresCTA')} <span aria-hidden="true">↘</span></a><p>{t('featuresAgreement')}</p></div><p class="features-note">{t('featuresNote')}.</p></div></section>
<section class="section container" id="start">{heading(d['stepsLabel'],d['stepsTitle'])}<ol class="steps">{steps}</ol></section>
<section class="pricing-section" id="pricing"><div class="container">{heading(d['pricingLabel'],d['pricingTitle'],d['pricingText'])}<div class="plans">{plans}</div><p class="fine-print pricing-note">{t('pricingNote')}</p></div></section>
<section class="section container faq-layout" id="faq"><div>{heading(d['faqLabel'],d['faqTitle'])}<a class="text-link" href="https://t.me/hacker_ronin" target="_blank" rel="noopener noreferrer">{t('write')} ↗</a></div><div class="faq-list">{faq}</div></section>
<section class="final-section" id="contacts"><div class="container final-content">{heading(d['finalLabel'],d['finalTitle'],d['finalText'])}<div class="actions">{contact(d['write'])}<a class="btn btn-dark-outline" href="#product">{t('preview')} ↗</a></div></div><div class="final-watermark" aria-hidden="true">qadamup.</div></section>
</main><footer class="container footer"><a class="brand" href="#top">qadam<span class="brand-up">up.</span></a><p>{t('footer')}</p><span>© 2026 QadamUp</span><a href="#top">{t('back')} ↑</a></footer>
<a class="mobile-contact" href="https://t.me/hacker_ronin" target="_blank" rel="noopener noreferrer">{t('write')} ↗</a><script type="application/json" id="page-config">{config}</script></body></html>'''
    return html

if __name__ == '__main__':
    # Keep the familiar entry point, but always publish the current B2B pages.
    from funnel import generate
    generate()
