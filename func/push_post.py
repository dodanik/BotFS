import asyncio
import random

from aiogram import exceptions
from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import WebAppInfo, FSInputFile
from sqlalchemy import select, func, text

from database.engine import session_maker
from database.list_users import get_count_region, get_hour_send_post, get_chat_id_number, get_users_chat_on_id, \
    get_admins_on, edit_count_region, del_chat_id_number, get_count_custom_region, edit_count_custom_region, \
    get_promocode_sports, get_promocode_casino, \
    get_user_neactive_5_days_send_post_list, get_user_neactive_2_days_send_post_list, \
    add_user_neactive_2_days_send_post_list, add_user_neactive_5_days_send_post_list, get_link_mirror
from database.models import PostRu, PostEn, PostKz, PostCustomKz, PostCustomEn, PostCustomRu
from database.orm_query import orm_get_post, orm_get_inactive_users
from dotenv import find_dotenv, load_dotenv

from posts_neactive.neactive_data import get_posts_with_freebet_code, get_posts_with_promo_code, get_posts_without_promo

load_dotenv(find_dotenv())





async def is_table_empty(table_name):
    async with session_maker() as session:
        result = await session.execute(select(func.count()).select_from(text(table_name)))
        count = result.scalar()
        return count == 0







async def pushmessages_ru(bot):
    count = await get_count_region('ru')
    while True:
        hour = await get_hour_send_post()
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
            login_kb = types.InlineKeyboardButton(text="Играть", web_app=WebAppInfo(url=await get_link_mirror()))
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'ru']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post RU")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot, login_kb)
                    count += 1
                    await edit_count_region(count, 'ru')



async def pushmessages_en(bot):
    count = await get_count_region('en')
    while True:
        hour = await get_hour_send_post()
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
            login_kb = types.InlineKeyboardButton(text="Play", web_app=WebAppInfo(url=await get_link_mirror()))
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'en']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post EN")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot, login_kb)
                    count += 1
                    await edit_count_region(count, 'en')




async def pushmessages_kz(bot):
    count = await get_count_region('kz')
    while True:
        hour = await get_hour_send_post()
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
            login_kb = types.InlineKeyboardButton(text="Ойнау",web_app=WebAppInfo(url=await get_link_mirror()))
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'kk']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post KZ")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_post(key, post, bot, login_kb)
                    count += 1
                    await edit_count_region(count, 'kz')





async def pushmessages_custom_ru(bot):
    count = await get_count_custom_region('ru')
    while True:
        time_until_execution = await time_post_random(5)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_custom_ru'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(3600)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostCustomRu)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'ru']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post Custom RU")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_custom_post(key, post, bot)
                    count += 1
                    await edit_count_custom_region(count, 'ru')



async def pushmessages_custom_en(bot):
    count = await get_count_custom_region('en')
    while True:
        time_until_execution = await time_post_random(5)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_custom_en'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostCustomEn)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'en']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post Custom EN")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_custom_post(key, post, bot)
                    count += 1
                    await edit_count_custom_region(count, 'en')




async def pushmessages_custom_kz(bot):
    count = await get_count_custom_region('kz')
    while True:
        time_until_execution = await time_post_random(5)
        await asyncio.sleep(time_until_execution)
        if await is_table_empty('post_custom_kz'):
            print("Таблица пуста, пропускаем обработку сообщений")
            await asyncio.sleep(1000)
            continue
        else:
            async with session_maker() as session:
                all_posts = await orm_get_post(session, PostCustomKz)
                if len(all_posts) <= count:
                    count = 0
            post = all_posts[count]
            chat_id_number = await get_chat_id_number()
            if chat_id_number:
                chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == 'kk']
                if chat_id_set_region:
                    for key in chat_id_set_region:
                        print("Post Custom KZ")
                        users_chat_ids = await get_users_chat_on_id()
                        admins_list_id_on = await get_admins_on()
                        if key not in users_chat_ids and key not in admins_list_id_on:
                            await send_push_custom_post(key, post, bot)
                    count += 1
                    await edit_count_custom_region(count, 'kz')





async def send_post_to_inactive_users_5_days(bot):
    is_sports_day = True
    while True:
        # Рассчитываем время до следующего выполнения
        time_until_execution = await time_post_random(1)
        await asyncio.sleep(time_until_execution)

        if is_sports_day:
            # Генерируем новый промокод для спорта
            promo_code = await get_promocode_sports()
            posts = await get_posts_with_freebet_code(promo_code)
        else:
            # Генерируем новый промокод для казино
            promo_code = await get_promocode_casino()
            posts = await get_posts_with_promo_code(promo_code)

        # Получаем список пользователей, которые были неактивны 5 полных дня
        async with session_maker() as session:
            inactive_users = await orm_get_inactive_users(session, 5)

        chat_id_number = await get_chat_id_number()
        user_neactive_send_post_list = await get_user_neactive_5_days_send_post_list()
        if chat_id_number:
            for user_id in inactive_users:
                if user_id not in user_neactive_send_post_list:
                    region = chat_id_number.get(user_id)
                    if region and region in posts:
                        post_data = posts[region]
                        post_data['type'] = 'photo'  # Устанавливаем тип контента
                        try:
                            await send_push_post_neactive(user_id, post_data, bot)
                            await add_user_neactive_5_days_send_post_list(user_id)
                        except exceptions.TelegramForbiddenError as e:
                            print(f"Пользователь заблокировал бота: {e}")
                        except Exception as e:
                            print(f"Произошла ошибка при отправке сообщения: {e}")

        # Переключаем день
        is_sports_day = not is_sports_day



async def send_post_to_inactive_users_2_days(bot):
    while True:
        # Рассчитываем время до следующего выполнения
        time_until_execution = await time_post_random(1)
        await asyncio.sleep(time_until_execution)

        # Генерируем посты без промокодов
        posts = await get_posts_without_promo()

        # Получаем список пользователей, которые были неактивны 2 полных дня
        async with session_maker() as session:
            inactive_users = await orm_get_inactive_users(session, 2)

        chat_id_number = await get_chat_id_number()
        user_neactive_send_post_list = await get_user_neactive_2_days_send_post_list()
        if chat_id_number:
            for user_id in inactive_users:
                if user_id not in user_neactive_send_post_list:
                    region = chat_id_number.get(user_id)
                    if region and region in posts:
                        post_data = posts[region]
                        post_data['type'] = 'photo'  # Устанавливаем тип контента
                        try:
                            await send_push_post_neactive(user_id, post_data, bot)
                            await add_user_neactive_2_days_send_post_list(user_id)
                        except exceptions.TelegramForbiddenError as e:
                            print(f"Пользователь заблокировал бота: {e}")
                        except Exception as e:
                            print(f"Произошла ошибка при отправке сообщения: {e}")








async def time_post(hour):
    now = datetime.now()
    scheduled_time = now.replace(hour=hour, minute=37, second=0, microsecond=0)
    if now > scheduled_time:
        scheduled_time += timedelta(days=1)
    time_until_execution = (scheduled_time - now).total_seconds()
    return time_until_execution


async def time_post_random(days):
    now = datetime.now()
    next_execution_day = now + timedelta(days=days)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    scheduled_time = next_execution_day.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0)
    time_until_execution = (scheduled_time - now).total_seconds()
    return time_until_execution

async def send_push_post(key, post, bot, login_btn):
    try:
        if post.type == 'photo':
            await bot.send_photo(key, post.image, caption=post.description,
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                     text=f"{post.button}", web_app=WebAppInfo(url=post.link)), login_btn]]))
        if post.type == 'video':
            await bot.send_video(key, post.image, caption=post.description,
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                     text=f"{post.button}", web_app=WebAppInfo(url=post.link)), login_btn]]))
        if post.type == 'animation':
            await bot.send_animation(key, post.image, caption=post.description,
                                     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=f"{post.button}",web_app=WebAppInfo(url=post.link)), login_btn]]))
    except exceptions.TelegramForbiddenError as e:
        await del_chat_id_number(key)
        print(f"Пользователь заблокировал бота: {e}")

    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")


async def send_push_custom_post(key, post, bot):
    try:
        # Создание инлайн клавиатуры с кнопками
        inline_keyboard = []
        if isinstance(post.link, list) and len(post.link) > 0:
            for i in range(len(post.link)):
                button = types.InlineKeyboardButton(
                    text=post.button[i] if isinstance(post.button, list) and i < len(post.button) else f'Button {i + 1}',
                    web_app=WebAppInfo(url=post.link[i])
                )
                inline_keyboard.append(button)

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

        # Отправка сообщения в зависимости от типа контента
        if post.type == 'photo':
            await bot.send_photo(key, post.image, caption=post.description, reply_markup=reply_markup)
        elif post.type == 'video':
            await bot.send_video(key, post.image, caption=post.description, reply_markup=reply_markup)
        elif post.type == 'animation':
            await bot.send_animation(key, post.image, caption=post.description, reply_markup=reply_markup)

    except exceptions.TelegramForbiddenError as e:
        await del_chat_id_number(key)
        print(f"Пользователь заблокировал бота: {e}")
    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")




async def send_push_post_neactive(key, post, bot):
    try:
        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
            text=post['button'], web_app=WebAppInfo(url=post['link']))]])

        if post['type'] == 'photo':
            photo = FSInputFile(post['image'])
            await bot.send_photo(key, photo, caption=post['description'], reply_markup=reply_markup)
        elif post['type'] == 'video':
            video = FSInputFile(post['image'])
            await bot.send_video(key, video, caption=post['description'], reply_markup=reply_markup)
        elif post['type'] == 'animation':
            animation = FSInputFile(post['image'])
            await bot.send_animation(key, animation, caption=post['description'], reply_markup=reply_markup)
    except exceptions.TelegramForbiddenError as e:
        print(f"Пользователь заблокировал бота: {e}")
    except Exception as e:
        print(f"Произошла ошибка при отправке сообщения: {e}")