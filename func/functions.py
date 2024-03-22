import asyncio
from datetime import datetime, timedelta

import aiogram
import aiohttp
from aiogram import types, exceptions, Bot
from aiogram.enums import MenuButtonType, parse_mode
from aiogram.types import MenuButtonWebApp, WebAppInfo
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.list_users import get_users_chat_on_id, get_history_chat, add_to_history_chat, get_admins_on, \
    get_chat_id_number, remove_user_chat_on_id, user_get_update, user_set_update, get_chat_id_number_user, \
    get_list_users_id_message, remove_to_list_users_id_message, remove_to_history_chat
from database.models import Users
from database.orm_query import orm_get_post, update_user_time
from filters.chat_types import my_list_chat_id_remove
from handlers.messagues import get_headers
from kb.keyboard import create_keyboard, chat_close_server_message


async def set_web_app_button_text(language_code, chatid, bot):
    if language_code:
        if language_code == 'ru':
            button_text = 'Играть'
            url = 'https://fan-sport.com/'
        elif language_code == 'uk':
            button_text = 'Грати'
            url = 'https://fan-sport.com/'
        elif language_code == 'pt':
            button_text = 'Jogar'
            url = 'https://fan-sport.com/'
        elif language_code == 'kk':
            button_text = 'Ойнау'
            url = 'https://fan-sport.com/'
        elif language_code == 'en':
            button_text = 'Play'
            url = 'https://fan-sport.com/'
        else:
            button_text = 'Play'
            url = 'https://fan-sport.com/'  # По умолчанию используем английский язык и стандартный URL

        await bot.set_chat_menu_button(chatid,
                                       menu_button=MenuButtonWebApp(
                                           MenuButtonType=MenuButtonType.WEB_APP,
                                           text=button_text,
                                           web_app=WebAppInfo(url=url)
                                       )
                                       )


# async def deletemessague(chat_id, mess, bot):
#     # mess2 = mess - 1
#     await asyncio.sleep(1 / 2)
#     await bot.delete_messages(chat_id, [mess])


async def send_message_chat(bot):
    headers = await get_headers()

    while True:
        await asyncio.sleep(10)
        chat_ids = await get_users_chat_on_id()
        if isinstance(chat_ids, dict):
            chat_ids = chat_ids.copy()
        if chat_ids:
            for chat_id, chat_id_hp in chat_ids.items():
                url_get_messages = f"https://api.helpcrunch.com/v1/chats/{chat_id_hp}/messages/?limit=10"
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(url_get_messages, headers=headers) as response:
                            if response.status == 200:
                                json_response = await response.json()
                                for item in json_response['data']:
                                    mess = await get_history_chat(chat_id)
                                    if mess:
                                        if item['id'] not in mess:
                                            if item['text'] not in ["chat_status_changed_by_public_api",
                                                                    "chat_auto_assigned", "chat_status_changed", "request_rating", "resolution_time"]:
                                                await bot.send_message(chat_id, item['text'])
                                                await add_to_history_chat(chat_id, item['id'])
                                            elif item['text'] == "chat_status_changed":
                                                url_get_status_chat = f"https://api.helpcrunch.com/v1/chats/{chat_id_hp}"
                                                try:
                                                    async with session.get(url_get_status_chat, headers=headers) as response_status:
                                                        if response_status.status == 200:
                                                            json_response_status = await response_status.json()
                                                            if json_response_status["status"] == "closed":
                                                                await close_chat(bot, chat_id)
                                                            else:
                                                                await add_to_history_chat(chat_id, item['id'])
                                                        else:
                                                            await handle_error(response_status)
                                                except aiohttp.ClientError as e:
                                                    print(f"Ошибка соединения: {e}")

                            else:
                                await handle_error(response)
                    except aiohttp.ClientError as e:
                        print(f"Ошибка соединения: {e}")


async def handle_error(response):
    error_response = await response.json()
    status = response.status
    error_message = error_response['errors'][0]['message']
    error_info = f"Ошибка {status}: {error_message}"
    if status == 400:
        raise ValueError(error_info)
    elif status == 401:
        raise ValueError(error_info)
    elif status == 404:
        raise ValueError(error_info)
    elif status == 429:
        raise ValueError(error_info)
    else:
        raise ValueError(f"Непредвиденный статус код: {status}")


async def update_user_datatime(session, user_id):
    current_time = datetime.now()
    user_datatime_last_update = await user_get_update(user_id)
    if (current_time - user_datatime_last_update) > timedelta(days=1):
        await update_user_time(session, user_id)
        await user_set_update(user_id, current_time)



async def delete_message(bot):
    while True:
        await asyncio.sleep(2)
        data = await get_list_users_id_message()
        if data:
            for key, values in data.copy().items():
                mess_id_del = []
                for value in values[:-1]:
                    mess_id_del.append(value)
                if mess_id_del:
                    try:
                        await bot.delete_messages(key, mess_id_del)
                        await remove_to_list_users_id_message(key, mess_id_del)
                    except aiogram.exceptions.TelegramBadRequest as e:
                        if "message can't be deleted for everyone" in str(e):
                            print(
                                "Received TelegramBadRequest: message can't be deleted for everyone\n Сообщение старше 48 часов!")
                            await remove_to_list_users_id_message(key, mess_id_del)
                        else:
                            error_message = f"An error occurred while deleting messages for chat {key}: {e}"
                            print(error_message)
                    except Exception as ex:
                        error_message = f"An unexpected error occurred: {ex}"
                        print(error_message)
        else:
            continue


async def close_chat(bot, chat_id):
    await bot.send_message(chat_id,
                           f'<b><i>{await chat_close_server_message(await get_chat_id_number_user(chat_id))}</i></b>',reply_markup=create_keyboard(f'{await get_chat_id_number_user(chat_id)}', 'menu_kb', 2, 2, 2,
                                                      2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'),
                           parse_mode="HTML")
    await remove_user_chat_on_id(chat_id)
    await my_list_chat_id_remove(chat_id)
    await remove_to_history_chat(chat_id)