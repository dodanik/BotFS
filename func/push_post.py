import asyncio
from aiogram import exceptions
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import WebAppInfo
from sqlalchemy import select, func, text

from database.engine import session_maker
from database.list_users import get_count_region, get_hour_send_post, get_chat_id_number, get_users_chat_on_id, \
    get_admins_on, edit_count_region, del_chat_id_number
from database.models import PostUa, PostRu, PostEn, PostPt, PostUz, PostKz
from database.orm_query import orm_get_post
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

async def is_table_empty(table_name):
    async with session_maker() as session:
        result = await session.execute(select(func.count()).select_from(text(table_name)))
        count = result.scalar()
        return count == 0






async def pushmessages_ua(bot):
    count = await get_count_region('ua')
    while True:
        hour = await get_hour_send_post('ua')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_ua'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(3600)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostUa)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'uk']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post UA")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'ua')


async def pushmessages_ru(bot):
    count = await get_count_region('ru')
    while True:
        hour = await get_hour_send_post('ru')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_ru'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(3600)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostRu)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'ru']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post RU")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'ru')



async def pushmessages_en(bot):
    count = await get_count_region('en')
    while True:
        hour = await get_hour_send_post('en')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_en'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostEn)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'en']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post EN")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'en')


async def pushmessages_pt(bot):
    count = await get_count_region('pt')
    while True:
        hour = await get_hour_send_post('pt')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_pt'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostPt)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'pt']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post PT")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'pt')



async def pushmessages_uz(bot):
    count = await get_count_region('uz')
    while True:
        hour = await get_hour_send_post('uz')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_uz'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostUz)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'uz']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post UZ")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'uz')


async def pushmessages_kz(bot):
    count = await get_count_region('kz')
    while True:
        hour = await get_hour_send_post('kz')
        time_until_execution = await time_post(hour)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_kz'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostKz)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'kk']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post KZ")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot)
                    count += 1
                    await edit_count_region(count, 'kz')


async def time_post(hour):
    now = datetime.now()
    scheduled_time = now.replace(hour=hour, minute=51, second=0, microsecond=0)
    if now > scheduled_time:
        scheduled_time += timedelta(days=1)
    time_until_execution = (scheduled_time - now).total_seconds()
    return time_until_execution


async def send_push_post(key, post, bot):
    try:
        if post.type == 'photo':
            await bot.send_photo(key, post.image, caption=post.description,
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                     text=f"{post.button}", web_app=WebAppInfo(url=post.link))]]))
        if post.type == 'video':
            await bot.send_video(key, post.image, caption=post.description,
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                     text=f"{post.button}", web_app=WebAppInfo(url=post.link))]]))
        if post.type == 'animation':
            await bot.send_animation(key, post.image, caption=post.description,
                                     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=f"{post.button}",web_app=WebAppInfo(url=post.link))]]))
    except exceptions.TelegramForbiddenError as e:
        await del_chat_id_number(key)
        print(f"Пользователь заблокировал бота: {e}")

    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")
