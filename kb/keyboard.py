import orjson
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.list_users import get_user_vip_list, get_promocode_sports, get_promocode_casino

with open("kb/language.json", "rb") as json:
    lengData = orjson.loads(json.read())

with open("kb/languageVip.json", "rb") as jsonVip:
    lengDataVip = orjson.loads(jsonVip.read())


def create_keyboard(language, keyboard_name, userId=False, *adjust_params):
    user_vip_list = get_user_vip_list()
    # Загрузка данных из файла JSON
    if userId and userId in user_vip_list:
        data = lengDataVip
    else:
        data = lengData



    # Получаем данные для клавиатуры из JSON файла
    keyboard_data = data.get(language, {}).get(keyboard_name, {})

    # Создаем объект клавиатуры ReplyKeyboardBuilder
    keyboard_builder = ReplyKeyboardBuilder()

    # Добавляем кнопки в клавиатуру на основе данных из JSON файла
    for button_text, button_info in keyboard_data.items():
        # Проверяем, является ли кнопка веб-приложением
        if isinstance(button_info, dict) and "web_app" in button_info:
            web_app_info = button_info["web_app"]
            keyboard_button = KeyboardButton(text=button_info["text"], web_app=WebAppInfo(url=web_app_info["url"]))
        else:
            # Получаем текст кнопки из JSON
            keyboard_button = KeyboardButton(text=button_info)

        # Добавляем кнопку в клавиатуру
        keyboard_builder.add(keyboard_button)

    # Настройка размера клавиатуры
    if adjust_params:
        keyboard_builder.adjust(*adjust_params)

    # Возвращаем объект клавиатуры

    return keyboard_builder


admin_kb = ReplyKeyboardBuilder()
admin_kb.add(
    KeyboardButton(text='Send post NOW'),
    KeyboardButton(text='Delete last post'),
    KeyboardButton(text='Send post VIP'),
    KeyboardButton(text='Delete last VIP post'),
    KeyboardButton(text='Add post'),
    KeyboardButton(text='Delete post'),
    KeyboardButton(text='Add admin'),
    KeyboardButton(text='Delete admin'),
    KeyboardButton(text='List of users'),
    KeyboardButton(text='Get Database FILE'),
    KeyboardButton(text='Edit link Mirror'),
    KeyboardButton(text='Edit Promo Code'),
    KeyboardButton(text='Edit post sending times'),
    KeyboardButton(text='Back to menu')
)
admin_kb.adjust(2, 2, 2, 2, 2, 2, 1, 1)


add_post_kb = ReplyKeyboardBuilder()
add_post_kb.add(
    KeyboardButton(text='Post RU'),
    KeyboardButton(text='Post EN'),
    KeyboardButton(text='Post KZ'),
    KeyboardButton(text='Cancel')
)
add_post_kb.adjust(1, 1, 1, 1)


del_post_kb = ReplyKeyboardBuilder()
del_post_kb.add(
    KeyboardButton(text='Del post RU'),
    KeyboardButton(text='Del post EN'),
    KeyboardButton(text='Del post KZ'),
    KeyboardButton(text='Cancel')
)
del_post_kb.adjust(1, 1, 1, 1)


send_post_kb_region = ReplyKeyboardBuilder()
send_post_kb_region.add(
    KeyboardButton(text='Send RU'),
    KeyboardButton(text='Send EN'),
    KeyboardButton(text='Send KZ'),
    KeyboardButton(text='Cancel')
)
send_post_kb_region.adjust(1, 1, 1, 1)

delete_send_post_kb_mow_region = ReplyKeyboardBuilder()
delete_send_post_kb_mow_region.add(
    KeyboardButton(text='Delete RU'),
    KeyboardButton(text='Delete EN'),
    KeyboardButton(text='Delete KZ'),
    KeyboardButton(text='Cancel')
)
delete_send_post_kb_mow_region.adjust(1, 1, 1, 1)






send_post_kb_vip = ReplyKeyboardBuilder()
send_post_kb_vip.add(
    KeyboardButton(text='Send Users Bonus Sports'),
    KeyboardButton(text='Send Users Bonus Casino'),
    KeyboardButton(text='Send Users VIP All'),
    KeyboardButton(text='Cancel')
)
send_post_kb_vip.adjust(1, 1, 1, 1)


post_deletion_confirmation = ReplyKeyboardBuilder()
post_deletion_confirmation.add(
    KeyboardButton(text='Yes'),
    KeyboardButton(text='No'),
    KeyboardButton(text='Cancel')
)
post_deletion_confirmation.adjust(2, 1)



edit_promo_code = ReplyKeyboardBuilder()
edit_promo_code.add(
    KeyboardButton(text='Edit FREEBET'),
    KeyboardButton(text='Edit FREESPINS'),
    KeyboardButton(text='Cancel')
)
edit_promo_code.adjust(2, 1)



admin_kb_cancel = ReplyKeyboardBuilder()
admin_kb_cancel.add(KeyboardButton(text='Cancel'))

admin_kb_cancel_sup = ReplyKeyboardBuilder()
admin_kb_cancel_sup.add(KeyboardButton(text='CancelSup'))

send_post_kb = ReplyKeyboardBuilder()
send_post_kb.add(KeyboardButton(text='Send'), KeyboardButton(text='Cancel'))
send_post_kb.adjust(1, 1)


check_add_post_kb = ReplyKeyboardBuilder()
check_add_post_kb.add(KeyboardButton(text='Add Post'), KeyboardButton(text='Cancel'))
check_add_post_kb.adjust(1, 1)


admin_super_kb = ReplyKeyboardBuilder()
admin_super_kb.add(
    KeyboardButton(text='Add post Custom'),
    KeyboardButton(text='Delete post Custom'),
    KeyboardButton(text='Back to menu')
)
admin_super_kb.adjust(2, 2, 2, 2, 2, 1, 1)







async def chat_kb(lang):
    chat_kb_lang = ReplyKeyboardBuilder()
    if lang == "ru":
        return chat_kb_lang.add(KeyboardButton(text='❌ Завершить чат')).as_markup(
                             resize_keyboard=True)
    elif lang == "uk":
        return chat_kb_lang.add(KeyboardButton(text='❌ Завершити чат')).as_markup(
                             resize_keyboard=True)
    elif lang == "uz":
        return chat_kb_lang.add(KeyboardButton(text='❌ Suhbat oxiri')).as_markup(
                             resize_keyboard=True)
    elif lang == "pt":
        return chat_kb_lang.add(KeyboardButton(text='❌ Fim de papo')).as_markup(
                             resize_keyboard=True)
    elif lang == "kk":
        return chat_kb_lang.add(KeyboardButton(text='❌ Чатты аяқтау')).as_markup(
                             resize_keyboard=True)
    else:
        return chat_kb_lang.add(KeyboardButton(text='❌ Chat End')).as_markup(
                             resize_keyboard=True)



async def chat_with_support_callback_kb(lang):
    if lang == "ru":
        return "Здравствуйте!\nДобро пожаловать в Чат!\nЧем мы можем Вам помочь?"
    elif lang == "uk":
        return "Доброго дня!\nЛаскаво просимо в Чат!\nЧим ми можемо Вам допомогти?"
    elif lang == "pt":
        return "Olá! \nBem-vindo ao Chat! \nComo podemos ajudá-lo?"
    elif lang == "kk":
        return "Сәлем! \nЧатқа қош келдіңіз! \nБіз сізге қалай көмектесе аламыз?"
    elif lang == "uz":
        return "Xayrli kun!\nChatga xush kelibsiz!\nSizga qanday yordam bera olamiz?"
    else:
        return "Hello!!\nWelcome to Chat!\nHow can we help you?"

async def menu_callback_kb(lang):
    if lang == "ru":
        return "Вот меню:"
    elif lang == "uz":
        return "Mana menyu:"
    elif lang == "pt":
        return "Aqui está o menu:"
    elif lang == "kk":
        return "Міне мәзір:"
    elif lang == "uk":
        return "Ось меню:"
    else:
        return "Menu:"

async def change_lang_callback_kb(lang):
    if lang == "ru":
        return "Язык успешно изменен"
    elif lang == "uk":
        return "Мову успішно змінено"
    elif lang == "pt":
        return "Idioma alterado com sucesso"
    elif lang == "kk":
        return "Тіл сәтті өзгертілді"
    elif lang == "uz":
        return "Til muvaffaqiyatli o'zgartirildi"
    else:
        return "Language changed successfully"



async def change_menu_lang_callback_kb(lang):
    if lang == "ru":
        return "Выбери язык:"
    elif lang == "uk":
        return "Вибери мову:"
    elif lang == "pt":
        return "Selecione o idioma:"
    elif lang == "kk":
        return "Тілді таңдаңыз:"
    elif lang == "uz":
        return "Til tanlang:"
    else:
        return "Select language:"


async def download_app_callback_kb(lang):
    if lang == "ru":
        return "Скачать приложение на Android:"
    elif lang == "uk":
        return "Завантажити додаток на Android:"
    elif lang == "pt":
        return "Baixe o aplicativo no Android:"
    elif lang == "kk":
        return "Қолданбаны Android жүйесіне жүктеп алыңыз:"
    elif lang == "uz":
        return "Android uchun ilovani yuklab oling:"
    else:
        return "Download the application on Android:"



async def mirror_callback_kb(lang):
    if lang == "ru":
        return "Актуальное зеркало:"
    elif lang == "uk":
        return "Актуальне дзеркало:"
    elif lang == "pt":
        return "Espelho atual:"
    elif lang == "kk":
        return "Ағымдағы айна:"
    elif lang == "uz":
        return "Haqiqiy oyna:"
    else:
        return "Current mirror:"


async def register_callback_kb(lang):
    if lang == "ru":
        return "Скорее спеши зарегистрироваться"
    elif lang == "uk":
        return "Швидше поспішай зареєструватися"
    elif lang == "pt":
        return "Apresse-se e registre-se"
    elif lang == "kk":
        return "Асығыңыз және тіркеліңіз"
    elif lang == "uz":
        return "Ro'yxatdan o'tishga shoshiling"
    else:
        return "Hurry up and register"


async def sticker_pack_callback_kb(lang):
    if lang == "ru":
        return "Забирай стикер пак от FANSPORT"
    elif lang == "uk":
        return "Забирай стікер пак від FANSPORT"
    elif lang == "pt":
        return "Obtenha um pacote de adesivos do FANSPORT"
    elif lang == "kk":
        return "FANSPORT сайтынан стикерлер жинағын алыңыз"
    elif lang == "uz":
        return "FANSPORT-dan stikerlar to'plamini oling"
    else:
        return "Get a sticker pack from FANSPORT"


async def vip_activate_kb(lang):
    if lang == "ru":
        return "Активируя VIP, ты получешь доступ к эксклюзивным рассылкам промокодов и других интересных персональных бонусов!!!\nДля активации поделись номером телефона и выбери бонус"
    elif lang == "uk":
        return "Роби депозит та погнали грати!"
    elif lang == "pt":
        return "Faça um depósito e vamos jogar!!"
    elif lang == "kk":
        return "VIP белсендіру арқылы сіз промо-кодтардың эксклюзивті жөнелтілімдеріне және басқа да қызықты жеке бонустарға қол жеткізе аласыз!\nІске қосу үшін телефон нөміріңізді бөлісіп, бонус таңдаңыз"
    elif lang == "uz":
        return "Depozit qo'ying va o'ynashni boshlang!"
    else:
        return "By activating VIP, you will get access to exclusive mailings of promotional codes and other interesting personal bonuses!!!\nTo activate, share your phone number and choose a bonus"


async def chatmessage_callback_kb(lang):
    if lang == "ru":
        return "Благодарим Вас за обращение!"
    elif lang == "uk":
        return "Дякуємо Вам за звернення!"
    elif lang == "pt":
        return "Obrigado por nos contatar!"
    elif lang == "kk":
        return "Бізбен хабарласқаныңызға рахмет!"
    elif lang == "uz":
        return "Iltimosingiz uchun rahmat!"
    else:
        return "Thank you for contacting us!"


async def download_link_button(lang):
    if lang == "ru":
        return "ЗАГРУЗИТЬ"
    elif lang == "uk":
        return "ЗАВАНТАЖИТИ"
    elif lang == "pt":
        return "DOWNLOAD"
    elif lang == "kk":
        return "ЖҮКТЕП АЛУ"
    elif lang == "uz":
        return "YUKLAB OLISH"
    else:
        return "DOWNLOAD"


async def sticker_pack_link_button(lang):
    if lang == "ru":
        return "ЗАБРАТЬ"
    elif lang == "uk":
        return "ЗАБРАТИ"
    elif lang == "pt":
        return "PEGAR"
    elif lang == "kk":
        return "АЛУ"
    elif lang == "uz":
        return "OLING"
    else:
        return "PICK UP"

async def mirror_link_button(lang):
    if lang == "ru":
        return "ПЕРЕЙТИ"
    elif lang == "uk":
        return "ПЕРЕЙТИ"
    elif lang == "pt":
        return "SIGA O LINK"
    elif lang == "kk":
        return "АШЫҚ СІЛТЕМЕ"
    elif lang == "uz":
        return "HAVOLAGA"
    else:
        return "FOLLOW LINK"


async def chat_close_server_message(lang):
    if lang == "ru":
        return "ЧАТ ЗАВЕРШЕН ОПЕРАТОРОМ"
    elif lang == "uk":
        return "ЧАТ БУЛО ЗАВЕРШЕНО ОПЕРАТОРОМ"
    elif lang == "pt":
        return "CHAT TERMINADO PELO OPERADOR"
    elif lang == "kk":
        return "ЧАТ ОПЕРАТОР АЯҚТАСТЫРДЫ"
    elif lang == "uz":
        return "CHAT OPERATOR TOMONIDAN TUGADI"
    else:
        return "CHAT ENDED BY OPERATOR"



messages_activate_vip = {
    'en': {
        'choose_option': 'Choose a bonus:',
        'share_phone': 'Share your phone number',
        'bonus_casino': 'Bonuses for casino',
        'bonus_sport': 'Bonuses for sports',
        'activate_vip': 'Activate VIP',
        'thanks_for_phone': 'Thank you for sharing your phone number.',
        'bonus_chosen': 'You have chosen a bonus.',
        'vip_activated': 'VIP activated.',
        'complete_all_steps': 'Please select a bonus before activating VIP',
        'refuse': 'Refuse VIP 🫤'
    },
    'ru': {
        'choose_option': 'Выберите бонус:',
        'share_phone': 'Поделиться номером телефона',
        'bonus_casino': 'Бонусы на казино',
        'bonus_sport': 'Бонусы на спорт',
        'activate_vip': 'Активировать VIP',
        'thanks_for_phone': 'Спасибо за предоставление номера телефона.',
        'bonus_chosen': 'Вы выбрали бонус.',
        'vip_activated': 'VIP активирован.',
        'complete_all_steps': 'Пожалуйста,выберите бонус перед активацией VIP.',
        'refuse': 'Отказаться от VIP 🫤'
    },
    'kk': {
        'choose_option': 'Бонус таңдаңыз:',
        'share_phone': 'Телефон нөміріңізбен бөлісіңіз',
        'bonus_casino': 'Казино үшін бонустар',
        'bonus_sport': 'Спорт үшін бонустар',
        'activate_vip': 'VIP белсендіру',
        'thanks_for_phone': 'Телефон нөміріңізбен бөліскеніңіз үшін рахмет.',
        'bonus_chosen': 'Сіз бонус таңдадыңыз.',
        'vip_activated': 'VIP белсендірілді.',
        'complete_all_steps': 'VIP белсендіру алдында бонус таңдаңыз',
        'refuse': 'VIP-тен бас тарту 🫤'
    }
}


async def keyboard_vip_activate(lang, chosen_bonus=None):
    bonus_casino_text = messages_activate_vip[lang]['bonus_casino']
    bonus_sport_text = messages_activate_vip[lang]['bonus_sport']

    if chosen_bonus == 'bonus_casino':
        bonus_casino_text += ' ✅'
    elif chosen_bonus == 'bonus_sport':
        bonus_sport_text += ' ✅'

    buttons = [
        [InlineKeyboardButton(text=bonus_casino_text, callback_data='bonus_casino'),
         InlineKeyboardButton(text=bonus_sport_text, callback_data='bonus_sport')],
        [InlineKeyboardButton(text=messages_activate_vip[lang]['activate_vip'], callback_data='activate_vip')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_contact_request_keyboard(lang):
    buttons = [
        [KeyboardButton(text=messages_activate_vip[lang]['share_phone'], request_contact=True)],
        [KeyboardButton(text=messages_activate_vip[lang]['refuse'])]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def create_contact_request_keyboard_cancel(lang):
    buttons = [
        [KeyboardButton(text=messages_activate_vip[lang]['refuse'])]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)








registration_kb = {
    "kk": {
        "casino": {
            "text": "Казино Бонусы",
            "url": "https://promo.fan-sport.tech/kz-casino-rg/?tag=d_3493582m_86084c_&promocode={promocode}"
        },
        "sport": {
            "text": "Бонус Спорты",
            "url": "https://promo.fan-sport.tech/kz-sport-rg/?tag=d_3493582m_87267c_&promocode={promocode}"
        },
        "back": "↩️ Артқа"
    },
    "en": {
        "casino": {
            "text": "Casino Bonus",
            "url": "https://promo.fan-sport.tech/kz-casino-rg/?tag=d_3493582m_86084c_&promocode={promocode}"
        },
        "sport": {
            "text": "Bonus Sports",
            "url": "https://promo.fan-sport.tech/kz-sport-rg/?tag=d_3493582m_87267c_&promocode={promocode}"
        },
        "back": "↩️ Back"
    },
    "ru": {
        "casino": {
            "text": "Бонус на Казино",
            "url": "https://promo.fan-sport.tech/kz-casino-rg/?tag=d_3493582m_86084c_&promocode={promocode}"
        },
        "sport": {
            "text": "Бонус на Спорт",
            "url": "https://promo.fan-sport.tech/kz-sport-rg/?tag=d_3493582m_87267c_&promocode={promocode}"
        },
        "back": "↩️ Назад"
    }
}


async def create_registration_keyboard(lang):
    promocode_sports = await get_promocode_sports()
    promocode_casino = await get_promocode_casino()

    buttons = [
        [
            KeyboardButton(text=registration_kb[lang]['casino']['text'],
                           web_app=WebAppInfo(url=registration_kb[lang]['casino']['url'].format(promocode=promocode_casino))),
            KeyboardButton(text=registration_kb[lang]['sport']['text'],
                           web_app=WebAppInfo(url=registration_kb[lang]['sport']['url'].format(promocode=promocode_sports)))
        ],
        [KeyboardButton(text=registration_kb[lang]['back'])]
    ]

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)