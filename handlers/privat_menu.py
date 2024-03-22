

from aiogram import types, F, Router, Bot
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from database.list_users import get_botlang, save_botlang, write_to_local_data_user_contact, remove_admins_on, \
    edit_chat_id_number, add_to_list_users_id_message
from filters.chat_types import my_list_chat_id_add, ChatTypesFilter
from func.functions import set_web_app_button_text, update_user_datatime
from handlers.messagues import search_user, create_chat
from kb.keyboard import create_keyboard, chat_kb, deposit_pack_callback_kb, sticker_pack_callback_kb, \
    register_callback_kb, mirror_callback_kb, download_app_callback_kb, menu_callback_kb, change_menu_lang_callback_kb, \
    change_lang_callback_kb, chat_with_support_callback_kb, download_link_button, sticker_pack_link_button, \
    mirror_link_button

menu_router = Router()
menu_router.message.filter(ChatTypesFilter(['private']))

@menu_router.message(StateFilter(None), (F.text.lower() == '📨 chat with support') | (F.text.lower() == '📨 чат з підтримкою') | (F.text.lower() == '📨 чат с сапортом') | (F.text.lower() == "📨 qo'llab-quvvatlash bilan suhbatlashing") | (F.text.lower() == "📨 bate-papo de suporte") | (F.text.lower() == "📨 қолдау арқылы сөйлесу"))
async def chathllo(message: types.Message, session: AsyncSession):
    botlang = await get_botlang()
    await my_list_chat_id_add(message.from_user.id)
    await message.answer(f'{await chat_with_support_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=await chat_kb(botlang[message.from_user.id]))
    await search_user(message)
    await create_chat(message)
    await write_to_local_data_user_contact()
    await add_to_list_users_id_message(message.chat.id, [message.message_id])
    await update_user_datatime(session, message.from_user.id)


@menu_router.message((F.text.lower() == '💢 меню') | (F.text.lower() == '💢 menu') | (F.text.lower() == '💢 menyu') | (F.text.lower() == '💢 cardápio') | (F.text.lower() == '💢 мәзір'))
async def pushmenu(message: types.Message, bot: Bot, session: AsyncSession):
    botlang = await get_botlang()
    await message.answer(f'{await menu_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'menu_kb', 2, 2, 2,
                                                      2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])
    await update_user_datatime(session, message.from_user.id)



@menu_router.message((F.text.lower() == '🇬🇧 english') | (F.text.lower() == '🇷🇺 русский') | (F.text.lower() == '🇺🇦 українська') | (F.text.lower() == "🇺🇿 o'zbek") | (F.text.lower() == '🇵🇹 português') | (F.text.lower() == "🇰🇿 қазақ"))
async def setlanguage(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    if message.text == '🇬🇧 English':
        botlang[message.from_user.id] = 'en'
        await edit_chat_id_number(message.chat.id, 'en')
    elif message.text == '🇷🇺 Русский':
        botlang[message.from_user.id] = 'ru'
        await edit_chat_id_number(message.chat.id, 'ru')
    elif message.text == '🇺🇦 Українська':
        botlang[message.from_user.id] = 'uk'
        await edit_chat_id_number(message.chat.id, 'uk')
    elif message.text == "🇺🇿 O'zbek":
        botlang[message.from_user.id] = 'uz'
        await edit_chat_id_number(message.chat.id, 'uz')
    elif message.text == "🇵🇹 Português":
        botlang[message.from_user.id] = 'pt'
        await edit_chat_id_number(message.chat.id, 'pt')
    elif message.text == "🇰🇿 Қазақ":
        botlang[message.from_user.id] = 'kk'
        await edit_chat_id_number(message.chat.id, 'kk')
    await message.answer(f'{await change_lang_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'language_kb', 1, 1, 1,
                                                      1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await set_web_app_button_text(botlang[message.from_user.id], message.chat.id, bot)
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])
    await save_botlang(botlang)


@menu_router.message((F.text.lower() == '↩️ на попередню сторінку') | (F.text.lower() == '↩️ back') | (F.text.lower() == '↩️ назад') | (F.text.lower() == '↩️ orqaga') | (F.text.lower() == '↩️ para a página anterior') | (F.text.lower() == '↩️ артқа'))
async def pushmenu(message: types.Message, bot: Bot, session: AsyncSession):
    botlang = await get_botlang()
    await message.answer(f'{await menu_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id + 1])
    await update_user_datatime(session, message.from_user.id)


@menu_router.message((F.text.lower() == '🌐 language') | (F.text.lower() == '🌐 мова') | (F.text.lower() == '🌐 язык') | (F.text.lower() == '🌐 til') | (F.text.lower() == '🌐 linguagem') | (F.text.lower() == '🌐 тіл'))
async def language(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await change_menu_lang_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'language_kb', 1, 1, 1,
                                                      1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])




@menu_router.message(
    (F.text.lower() == '↩️ назад в меню') | (F.text.lower() == '↩️ back to menu') | (F.text.lower() == '↩️ повернутися в меню') | (F.text.lower() == 'back to menu') | (F.text.lower() == '↩️ menyuga qaytish') | (F.text.lower() == '↩️ мәзірге оралу') | (F.text.lower() == '↩️ voltar ao menu'))
async def backtomenu(message: types.Message, bot: Bot, session: AsyncSession):
    botlang = await get_botlang()
    await remove_admins_on(message.chat.id)
    await message.answer(f'{await menu_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'menu_kb', 2, 2, 2,
                                                      2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])
    await update_user_datatime(session, message.from_user.id)



@menu_router.message((F.text.lower() == '📱 приложение') | (F.text.lower() == '📱 application') | (F.text.lower() == '📱 додаток') | (F.text.lower() == '📱 ilova') | (F.text.lower() == '📱 aplicativo') | (F.text.lower() == '📱 қолдану'))
async def downloadapp(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await download_app_callback_kb(botlang[message.from_user.id])} <b><a href="https://app.appsflyer.com/org.bet2fun.client-CustomPustom?pid=FromSite&c=%5C%3Cbtag%3E&tag%3Cbtag%3E&af_r=https://www.bkre22.com/downloads/androidclient/releases_android/bet2fun/site/bet2fun.apk">{await download_link_button(botlang[message.from_user.id])}</a></b>',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'downloadapp_kb', 1,
                                                      1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'), parse_mode="HTML")
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])


@menu_router.message((F.text.lower() == '🔗 зеркало') | (F.text.lower() == '🔗 mirror') | (F.text.lower() == '🔗 дзеркало') | (F.text.lower() == '🔗 oyna') | (F.text.lower() == '🔗 espelho') | (F.text.lower() == '🔗 айна'))
async def mirror(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await mirror_callback_kb(botlang[message.from_user.id])} <b><a href="https://bet2fun.me">{await mirror_link_button(botlang[message.from_user.id])}</a></b>\nhttps://bet2fun.me',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'mirror_kb', 1, 1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'), parse_mode="HTML")
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])


@menu_router.message((F.text.lower() == '🎯 регистрация') | (F.text.lower() == '🎯 registration') | (F.text.lower() == '🎯 реєстрація') | (F.text.lower() == '🎯 roʻyxatdan oʻtish') | (F.text.lower() == '🎯 cadastro') | (F.text.lower() == '🎯 тіркеу'))
async def register(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await register_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'register_kb', 1,
                                                      1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])


@menu_router.message((F.text.lower() == '🎁 стикер пак') | (F.text.lower() == '🎁 sticker pack') | (F.text.lower() == '🎁 стікер пак') | (F.text.lower() == "🎁 stikerlar to'plami") | (F.text.lower() == '🎁 pacote de adesivos') | (F.text.lower() == "🎁 стикерлер жинағы"))
async def stik(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await sticker_pack_callback_kb(botlang[message.from_user.id])} <b><a href="https://t.me/addstickers/BET2FUN">{await sticker_pack_link_button(botlang[message.from_user.id])}</a></b>',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'stikers_kb', 1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'), parse_mode="HTML")
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])


@menu_router.message((F.text.lower() == '💵 депозит') | (F.text.lower() == '💵 deposit') | (F.text.lower() == '💵 депозит') | (F.text.lower() == '💵 depozit') | (F.text.lower() == '💵 depósito') | (F.text.lower() == '💵 депозит'))
async def depisit(message: types.Message, bot: Bot):
    botlang = await get_botlang()
    await message.answer(f'{await deposit_pack_callback_kb(botlang[message.from_user.id])}',
                         reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'deposit_kb', 1, 1).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await add_to_list_users_id_message(message.chat.id, [message.message_id, message.message_id+1])
