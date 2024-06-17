import asyncio

import aiogram
from aiogram import F, Router, types, Bot, exceptions
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import FSInputFile, WebAppInfo
import aiosqlite
from datetime import datetime

from database.db_dump import insert_users_from_dict, delete_database
from database.list_users import add_admins_on, get_chat_id_number, get_users_chat_on_id, get_admins_on, edit_hour_time, \
    get_hour_send_post, edit_list_last_post_id, get_list_last_post_id, clear_list_last_post_id, \
    edit_list_vip_last_post_id, get_list_vip_last_post_id, clear_list_vip_last_post_id
from database.models import PostRu, PostEn, PostKz, PostCustomRu, PostCustomEn, PostCustomKz
from database.orm_query import orm_add_post, orm_get_users, orm_get_post, orm_delete_post, get_users_by_bonus_type, \
    orm_add_post_custom
from filters.chat_types import IsAdmin, ChatTypesFilter, my_admins_list_remove, my_admins_list_add, get_my_admins_list, \
    IsAdminSuper

from kb.keyboard import admin_kb, admin_kb_cancel, send_post_kb, add_post_kb, check_add_post_kb, send_post_kb_region, \
    del_post_kb, delete_send_post_kb_mow_region, send_post_kb_vip, post_deletion_confirmation, admin_super_kb, \
    admin_kb_cancel_sup

admin_super = Router()
admin_super.message.filter(ChatTypesFilter(['private']), IsAdminSuper())


@admin_super.message(Command('adminSuper'))
async def adminhello(message: types.Message):
    await add_admins_on(message.chat.id)
    await message.answer("Hello Admin Super)))", reply_markup=admin_super_kb.as_markup(
            resize_keyboard=True))


@admin_super.message(StateFilter('*'), Command("cancelSup"))
@admin_super.message(StateFilter('*'), F.text.casefold() == "cancelSup")
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancel", reply_markup=admin_super_kb.as_markup(
            resize_keyboard=True))



class AddPostCustom(StatesGroup):
    region = State()
    description = State()
    link = State()
    image = State()
    type = State()
    button = State()
    check = State()


class RemovePostCustom(StatesGroup):
    id = State()
    region = State()



@admin_super.message(StateFilter(None), F.text == "Add post Custom")
async def add_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select a region for your post:", reply_markup=add_post_kb.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(AddPostCustom.region)


@admin_super.message(AddPostCustom.region, F.text)
async def add_post_region(message: types.Message, state: FSMContext):
    if message.text == 'Post RU':
        await state.update_data(region='ru')
    elif message.text == 'Post EN':
        await state.update_data(region='en')
    elif message.text == 'Post KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Enter post description:", reply_markup=admin_kb_cancel_sup.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(AddPostCustom.description)


@admin_super.message(AddPostCustom.description, F.text)
async def add_text(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the link for the post:", reply_markup=admin_kb_cancel_sup.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPostCustom.link)



@admin_super.message(AddPostCustom.link, F.text)
async def add_link(message: types.Message, state: FSMContext):
    await state.update_data(link=await parse_links_async(message.text))
    await message.answer("Enter the name of the button:", reply_markup=admin_kb_cancel_sup.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPostCustom.button)


@admin_super.message(AddPostCustom.button, F.text)
async def add_button_post(message: types.Message, state: FSMContext):
    await state.update_data(button=await parse_links_async(message.text))
    await message.answer("Upload an image for your post:", reply_markup=admin_kb_cancel_sup.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPostCustom.image)


@admin_super.message(AddPostCustom.image)
async def add_image(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(image=message.photo[-1].file_id)
        await state.update_data(type='photo')
    elif message.content_type == ContentType.VIDEO:
        await state.update_data(image=message.video.file_id)
        await state.update_data(type='video')
    elif message.content_type == ContentType.ANIMATION:
        await state.update_data(image=message.animation.file_id)
        await state.update_data(type='animation')

    data = await state.get_data()

    # Ответ пользователю с кнопками проверки поста
    await message.answer("You Post:", reply_markup=check_add_post_kb.as_markup(resize_keyboard=True))

    # Создание инлайн клавиатуры с кнопками
    inline_keyboard = []
    if isinstance(data.get('link'), list) and len(data['link']) > 0:
        for i in range(len(data['link'])):
            button = types.InlineKeyboardButton(
                text=data['button'][i] if isinstance(data.get('button'), list) and i < len(
                    data['button']) else f'Button {i + 1}',
                web_app=WebAppInfo(url=data['link'][i])
            )
            inline_keyboard.append(button)

    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

    # Отправка сообщения в зависимости от типа контента
    if data['type'] == 'photo':
        await bot.send_photo(message.chat.id, data['image'], caption=data.get('description', ''),
                             reply_markup=reply_markup)
    elif data['type'] == 'video':
        await bot.send_video(message.chat.id, data['image'], caption=data.get('description', ''),
                             reply_markup=reply_markup)
    elif data['type'] == 'animation':
        await bot.send_animation(message.chat.id, data['image'], caption=data.get('description', ''),
                                 reply_markup=reply_markup)

    # Установка состояния для проверки поста
    await state.set_state(AddPostCustom.check)


@admin_super.message(AddPostCustom.check)
async def add_post_db(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    try:
        if data['region'] == 'ru':
            await orm_add_post_custom(session, PostCustomRu, data)
        if data['region'] == 'en':
            await orm_add_post_custom(session, PostCustomEn, data)
        if data['region'] == 'kk':
            await orm_add_post_custom(session, PostCustomKz, data)
        await state.clear()
        await message.answer("Post added!", reply_markup=admin_super_kb.as_markup(
            resize_keyboard=True))
    except Exception as e:
        await message.answer(
            f"ERROR: \n{str(e)}\n Contact the programmer, he wants money again", reply_markup=admin_super_kb.as_markup(resize_keyboard=True))
        await state.clear()


async def parse_links_async(links_str):
    """
    Асинхронная функция для разбивки строки на массив строк по запятым с пробелами по бокам.

    :param links_str: str - строка с ссылками, разделенными запятыми с пробелами по бокам
    :return: list - список ссылок
    """
    # Удаляем внешние кавычки, если они есть
    links_str = links_str.strip('\'"')

    # Разбиваем строку на список по ', '
    links_list = [link.strip() for link in links_str.split(', ')]

    return links_list












@admin_super.message(StateFilter(None), F.text == "Delete post Custom")
async def remove_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select the language of the region the posts you want to delete:", reply_markup=del_post_kb.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(RemovePostCustom.region)



@admin_super.message(RemovePostCustom.region, F.text)
async def remove_post_button(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text == 'Del post RU':
        await state.update_data(region='ru')
        data = await orm_get_post(session, PostCustomRu)
    elif message.text == 'Del post EN':
        await state.update_data(region='en')
        data = await orm_get_post(session, PostCustomEn)
    elif message.text == 'Del post KZ':
        await state.update_data(region='kk')
        data = await orm_get_post(session, PostCustomKz)
    else:
        data = None

    if data:
        for post in data:
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
                await bot.send_photo(
                    message.chat.id, post.image,
                    caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            elif post.type == 'video':
                await bot.send_video(
                    message.chat.id, post.image,
                    caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            elif post.type == 'animation':
                await bot.send_animation(
                    message.chat.id, post.image,
                    caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )

            await asyncio.sleep(1/3)

        await message.answer(
            "Enter the ID of the post you want to delete:",
            reply_markup=admin_kb_cancel_sup.as_markup(resize_keyboard=True)
        )
        await state.set_state(RemovePostCustom.id)
    else:
        await message.answer(
            "There are no posts for this language yet Admin super.",
            reply_markup=del_post_kb.as_markup(resize_keyboard=True)
        )
        await state.set_state(RemovePostCustom.region)



@admin_super.message(RemovePostCustom.id, F.text)
async def remove_post_button(message: types.Message, state: FSMContext, session: AsyncSession):
    data_region = await state.get_data()
    try:
        post_id = int(message.text)
        if data_region['region'] == 'ru':
            data = await orm_delete_post(session, PostCustomRu, post_id)
        elif data_region['region'] == 'en':
            data = await orm_delete_post(session, PostCustomEn, post_id)
        elif data_region['region'] == 'kk':
            data = await orm_delete_post(session, PostCustomKz, post_id)
        else:
            data = None
        if data:
            await message.answer("Post deleted!", reply_markup=admin_super_kb.as_markup(
                resize_keyboard=True))
            await state.clear()
        else:
            raise Exception()
    except Exception as e:
        await message.answer(
            "A post with this ID does NOT exist in the database!!!", reply_markup=admin_super_kb.as_markup(resize_keyboard=True))
        await state.clear()