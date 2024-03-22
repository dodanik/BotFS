import asyncio
from datetime import datetime, timedelta

import ujson
import os
import aiohttp
from sqlalchemy import func, select, text

from sqlalchemy.ext.asyncio import AsyncSession

from database.list_users import get_botlang, set_botlang, save_botlang, get_users_chat_on_id, get_user_number_chat_hp, \
    get_history_chat, add_to_history_chat, remove_admins_on, get_admins_on, write_to_local_data_user_contact, \
    get_chat_id_number, edit_chat_id_number, del_chat_id_number, get_hour_send_post, user_get_update, user_set_update, \
    save_local_botlang, save_local_chat_id_number, get_count_region, edit_count_region, get_list_users_id_message, \
    remove_to_list_users_id_message
from database.models import PostUa
from database.orm_query import orm_get_post, orm_add_users, check_user_exists, update_user_time, orm_get_users
from filters.chat_types import my_list_chat_id_add, get_my_admins_list
from func.functions import set_web_app_button_text, send_message_chat, delete_message

from handlers.messagues import search_user, get_headers, create_chat
from middlewares.db import DataBaseSession

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import MenuButtonType, ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import FSInputFile, MenuButtonWebApp, WebAppInfo, BotCommandScopeAllPrivateChats
from aiogram import exceptions

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker
from func.push_post import pushmessages_ua, pushmessages_ru, pushmessages_en, pushmessages_pt, \
    pushmessages_uz, pushmessages_kz

from kb import keyboard
from kb.keyboard import create_keyboard, chat_kb
from handlers.admin import admin_router
from handlers.chat import chat_router
from handlers.privat_menu import menu_router
from handlers.chanel_handler import channel_handler

# Загрузка данных из JSON-файлов
with open("config.json", "r") as filetoken:
    token = ujson.load(filetoken)

TOKEN = token.get('BOT_TOKEN')
bot = Bot(TOKEN)

dp = Dispatcher()

dp.include_router(channel_handler)
dp.include_router(chat_router)
dp.include_router(admin_router)
dp.include_router(menu_router)


photofirst = FSInputFile('img/firstslider.jpg', 'rb')



@dp.message(CommandStart())
async def command_start(message: types.Message, session: AsyncSession):
    global bot
    botlang = await get_botlang()
    if message.chat.id not in await get_chat_id_number():
        await edit_chat_id_number(message.chat.id, message.from_user.language_code)

    if message.from_user.id not in botlang:
        botlang[message.from_user.id] = message.from_user.language_code

    if botlang[message.from_user.id] == 'ru':
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀Играть🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f'Рады видеть Вас,  {message.from_user.first_name}!\n' '🚀Безумное предложение для тебя!💥\n' 'Не пропусти выгодное предложение 100% бонус на первый депозит в казино ДО 100 ЕВРО!\n' 'Делай ставки и выигрывай🏆💯',
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥Врывайся в Игру!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Добро пожаловать!'))

    elif botlang[message.from_user.id] == 'uk':
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀Грати🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f'Раді Вас бачити,  {message.from_user.first_name}!\n' '🚀Шалена пропозиція для тебе!💥\n' 'Не пропусти вигідну пропозицію 100% бонус на перший депозит на спорт ДО 3000 UAH!\n' 'Роби ставки та вигравай🏆💯',
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥ШВИДШЕ ТИЦЯЙ ГРАТИ!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Раді Вас вітати!!'))

    elif botlang[message.from_user.id] == 'uz':
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀O'ynang🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f"Sizni ko'rganimdan xursandman, {message.from_user.first_name}!\n🚀Siz uchun aqldan ozgan taklif!\n💥Foydali taklifni o'tkazib yubormang, 3000 UAH gacha bo'lgan sport turlari bo'yicha birinchi depozit uchun 100% bonus! \nTiking va yutib oling.🏆💯",
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥TEZ O'YNASHGA UYINING!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Sizni kutib olishdan xursandmiz!!'))

    elif botlang[message.from_user.id] == 'pt':
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀Jogar🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f"Estamos felizes em ver você, {message.from_user.first_name}!\n🚀Oferta maluca para você!\n💥Não perca a lucrativa oferta de bônus de 100% no seu primeiro depósito no cassino ATÉ 100 EUROS! \nFaça suas apostas e ganhe🏆💯",
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥Entre no jogo!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Bem-vindo!'))

    elif botlang[message.from_user.id] == 'kk':
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀Ойнау🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f'Біз сізді көргенімізге қуаныштымыз, {message.from_user.first_name}!\n🚀Сізге арналған керемет ұсыныс!\n💥100 ЕВРОҒА ДЕЙІН казинодағы алғашқы салымыңыз бойынша 100% бонустың тиімді ұсынысын жіберіп алмаңыз! \nҰтыс тігулеріңізді қойыңыз және ұтып алыңыз🏆💯',
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥Ойынға қатысыңыз!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Қош келдіңіз!'))

    else:
        botlang[message.from_user.id] = 'en'
        inline_kb = types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="🚀Play🚀", web_app=WebAppInfo(
                url='https://lxzsdfgw.xyz/L?tag=d_3222083m_2393c_&site=3222083&ad=2393&r=slots'))]])
        await message.answer_photo(photofirst,
                                   caption=f"We're glad to see you,  {message.from_user.first_name}!\n🚀Unbelievable offer for you!💥\nDon't miss the opportunity of 100% bonus on the first deposit at the casino UP TO 3000 UAH!\nPlace your bets and win🏆💯",
                                   parse_mode='html',
                                   reply_markup=inline_kb)
        await message.answer(text="💥Click and PLAY!!!💥",
                             reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'start_kb', 2).as_markup(
                                 resize_keyboard=True,
                                 input_field_placeholder='Welcome!'))
    if message.from_user.username:
        if message.from_user.first_name:
            if message.from_user.last_name:
                if await check_user_exists(session, message.from_user.id):
                    await orm_add_users(session, {'userid': message.from_user.id, 'username': message.from_user.username,
                                                  'firstname': message.from_user.first_name, 'lastname': message.from_user.last_name, 'language': message.from_user.language_code})
                    await user_set_update(message.from_user.id, datetime.now())
                else:
                    await update_user_time(session, message.from_user.id)
                    await user_set_update(message.from_user.id, datetime.now())
            else:
                if await check_user_exists(session, message.from_user.id):
                    await orm_add_users(session, {'userid': message.from_user.id, 'username': message.from_user.username,
                                                  'firstname': message.from_user.first_name, 'language': message.from_user.language_code})
                    await user_set_update(message.from_user.id, datetime.now())
                else:
                    await update_user_time(session, message.from_user.id)
                    await user_set_update(message.from_user.id, datetime.now())
        elif message.from_user.last_name:
            if await check_user_exists(session, message.from_user.id):
                await orm_add_users(session, {'userid': message.from_user.id, 'username': message.from_user.username,
                                              'lastname': message.from_user.last_name,
                                              'language': message.from_user.language_code})
                await user_set_update(message.from_user.id, datetime.now())
            else:
                await update_user_time(session, message.from_user.id)
                await user_set_update(message.from_user.id, datetime.now())
        else:
            if await check_user_exists(session, message.from_user.id):
                await orm_add_users(session, {'userid': message.from_user.id, 'username': message.from_user.username,
                                              'language': message.from_user.language_code})
                await user_set_update(message.from_user.id, datetime.now())
            else:
                await update_user_time(session, message.from_user.id)
                await user_set_update(message.from_user.id, datetime.now())
    else:
        if message.from_user.first_name:
            if message.from_user.last_name:
                if await check_user_exists(session, message.from_user.id):
                    await orm_add_users(session, {'userid': message.from_user.id,
                                                  'firstname': message.from_user.first_name, 'lastname': message.from_user.last_name, 'language': message.from_user.language_code})
                    await user_set_update(message.from_user.id, datetime.now())
                else:
                    await update_user_time(session, message.from_user.id)
                    await user_set_update(message.from_user.id, datetime.now())
            else:
                if await check_user_exists(session, message.from_user.id):
                    await orm_add_users(session, {'userid': message.from_user.id,
                                                  'firstname': message.from_user.first_name, 'language': message.from_user.language_code})
                    await user_set_update(message.from_user.id, datetime.now())
                else:
                    await update_user_time(session, message.from_user.id)
                    await user_set_update(message.from_user.id, datetime.now())

        elif message.from_user.last_name:
            if await check_user_exists(session, message.from_user.id):
                await orm_add_users(session, {'userid': message.from_user.id,
                                              'lastname': message.from_user.last_name,
                                              'language': message.from_user.language_code})
                await user_set_update(message.from_user.id, datetime.now())
            else:
                await update_user_time(session, message.from_user.id)
                await user_set_update(message.from_user.id, datetime.now())
    await set_web_app_button_text(botlang[message.from_user.id], message.chat.id, bot)
    await set_botlang(botlang)












async def get_data_update_users():
    async with session_maker() as session:
        for users in await orm_get_users(session):
            await user_set_update(users.userid, users.updated)

async def save_global_data():
    while True:
        now = datetime.now()
        scheduled_time = now.replace(hour=5, minute=0, second=0, microsecond=0)
        if now > scheduled_time:
            scheduled_time += timedelta(days=1)
        time_until_execution = (scheduled_time - now).total_seconds()
        await asyncio.sleep(time_until_execution)
        await save_local_botlang()
        await save_local_chat_id_number()

async def main():
    global bot
    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await get_data_update_users()
    post_ua = pushmessages_ua(bot)
    post_ru = pushmessages_ru(bot)
    post_en = pushmessages_en(bot)
    post_pt = pushmessages_pt(bot)
    post_uz = pushmessages_uz(bot)
    post_kz = pushmessages_kz(bot)
    send_message = send_message_chat(bot)
    dell_mes = delete_message(bot)
    save_global = save_global_data()
    asyncio.create_task(post_ua)
    asyncio.create_task(post_ru)
    asyncio.create_task(post_en)
    asyncio.create_task(post_pt)
    asyncio.create_task(post_uz)
    asyncio.create_task(post_kz)
    asyncio.create_task(send_message)
    asyncio.create_task(dell_mes)
    asyncio.create_task(save_global)
    await bot.set_my_commands(commands=[], scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

