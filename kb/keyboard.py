import orjson
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

with open("kb/language.json", "rb") as json:
    data = orjson.loads(json.read())


def create_keyboard(language, keyboard_name, *adjust_params):
    # Загрузка данных из файла JSON
    global data

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
    KeyboardButton(text='Add post'),
    KeyboardButton(text='Delete post'),
    KeyboardButton(text='Add admin'),
    KeyboardButton(text='Delete admin'),
    KeyboardButton(text='List of users'),
    KeyboardButton(text='Get Database FILE'),
    KeyboardButton(text='Edit post sending times'),
    KeyboardButton(text='Back to menu')
)
admin_kb.adjust(1, 2, 2, 2, 1, 1)

admin_kb_cancel = ReplyKeyboardBuilder()
admin_kb_cancel.add(KeyboardButton(text='Cancel'))

send_post_kb = ReplyKeyboardBuilder()
send_post_kb.add(KeyboardButton(text='Send'), KeyboardButton(text='Cancel'))
send_post_kb.adjust(1, 1)



async def chat_kb(lang):
    chat_kb_lang = ReplyKeyboardBuilder()
    if lang == "ru":
        return chat_kb_lang.add(KeyboardButton(text='❌ Завершить чат')).as_markup(
                             resize_keyboard=True)
    elif lang == "uk":
        return chat_kb_lang.add(KeyboardButton(text='❌ Завершити чат')).as_markup(
                             resize_keyboard=True)
    else:
        return chat_kb_lang.add(KeyboardButton(text='❌ Chat End')).as_markup(
                             resize_keyboard=True)



async def chat_with_support_callback_kb(lang):
    if lang == "ru":
        return "Здравствуйте!\nДобро пожаловать в Чат!\nЧем мы можем Вам помочь?"
    elif lang == "uk":
        return "Доброго дня!\nЛаскаво просимо в Чат!\nЧим ми можемо Вам допомогти?"
    else:
        return "Hello!!\nWelcome to Chat!\nHow can we help you?"

async def menu_callback_kb(lang):
    if lang == "ru":
        return "Вот меню:"
    elif lang == "uk":
        return "Ось меню:"
    else:
        return "Menu:"

async def change_lang_callback_kb(lang):
    if lang == "ru":
        return "Язык успешно изменен"
    elif lang == "uk":
        return "Мову успішно змінено"
    else:
        return "Language changed successfully"



async def change_menu_lang_callback_kb(lang):
    if lang == "ru":
        return "Выбери язык:"
    elif lang == "uk":
        return "Вибери мову:"
    else:
        return "Select language:"


async def download_app_callback_kb(lang):
    if lang == "ru":
        return "Скачать приложение на Android:"
    elif lang == "uk":
        return "Завантажити додаток на Android:"
    else:
        return "Download the application on Android:"



async def mirror_callback_kb(lang):
    if lang == "ru":
        return "Актуальное зеркало:"
    elif lang == "uk":
        return "Актуальне дзеркало:"
    else:
        return "Current mirror:"


async def register_callback_kb(lang):
    if lang == "ru":
        return "Скорее спеши зарегистрироваться"
    elif lang == "uk":
        return "Швидше поспішай зареєструватися"
    else:
        return "Hurry up and register"


async def sticker_pack_callback_kb(lang):
    if lang == "ru":
        return "Забирай стикер пак от BET2FUN"
    elif lang == "uk":
        return "Забирай стікер пак від BET2FUN"
    else:
        return "Get a sticker pack from BET2FUN"


async def deposit_pack_callback_kb(lang):
    if lang == "ru":
        return "Делай депозит и погнали играть!!!"
    elif lang == "uk":
        return "Роби депозит та погнали грати!"
    else:
        return "Make a deposit and let's go play!!!"


async def chatmessage_callback_kb(lang):
    if lang == "ru":
        return "Благодарим Вас за обращение!"
    elif lang == "uk":
        return "Дякуємо Вам за звернення!"
    else:
        return "Thank you for contacting us!"


async def download_link_button(lang):
    if lang == "ru":
        return "ЗАГРУЗИТЬ"
    elif lang == "uk":
        return "ЗАВАНТАЖИТИ"
    else:
        return "DOWNLOAD"


async def sticker_pack_link_button(lang):
    if lang == "ru":
        return "ЗАБРАТЬ"
    elif lang == "uk":
        return "ЗАБРАТИ"
    else:
        return "PICK UP"

async def mirror_link_button(lang):
    if lang == "ru":
        return "ПЕРЕЙТИ"
    elif lang == "uk":
        return "ПЕРЕЙТИ"
    else:
        return "FOLLOW LINK"


async def chat_close_server_message(lang):
    if lang == "ru":
        return "ЧАТ ЗАВЕРШЕН ОПЕРАТОРОМ"
    elif lang == "uk":
        return "ЧАТ БУЛО ЗАВЕРШЕНО ОПЕРАТОРОМ"
    else:
        return "CHAT ENDED BY OPERATOR"