import asyncio

from aiogram import F, Router, types, Bot, exceptions
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputFile, FSInputFile, WebAppInfo
import aiosqlite
from datetime import datetime

from database.db_dump import insert_users_from_dict, delete_database
from database.list_users import add_admins_on, get_chat_id_number, get_users_chat_on_id, get_admins_on, edit_hour_time, \
    get_hour_send_post
from database.models import PostUa, PostRu, PostPt, PostEn, PostKz, PostUz
from database.orm_query import orm_add_post, orm_get_users, orm_get_post, orm_delete_post
from filters.chat_types import IsAdmin, ChatTypesFilter, my_admins_list_remove, my_admins_list_add, get_my_admins_list

from kb.keyboard import admin_kb, admin_kb_cancel, send_post_kb, add_post_kb, check_add_post_kb, send_post_kb_region, \
    del_post_kb, edit_time_post_kb

admin_router = Router()
admin_router.message.filter(ChatTypesFilter(['private']), IsAdmin())


@admin_router.message(Command('admin'))
async def adminhello(message: types.Message):
    await add_admins_on(message.chat.id)
    await message.answer("Hello Admin)))", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))


@admin_router.message(StateFilter('*'), Command("cancel"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "cancel")
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Cancel", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))


class AddAdmin(StatesGroup):
    user_id = State()
    user_name = State()

class DeleteAdmin(StatesGroup):
    user_id = State()
    user_name = State()


class AddPost(StatesGroup):
    region = State()
    description = State()
    link = State()
    image = State()
    type = State()
    button = State()
    check = State()


class EditTimePost(StatesGroup):
    time = State()
    region = State()


class RemovePost(StatesGroup):
    id = State()
    region = State()


class SendPost(StatesGroup):
    description = State()
    link = State()
    image = State()
    button = State()
    send = State()
    region = State()


@admin_router.message(StateFilter(None), F.text == "Add admin")
async def add_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Enter the ID of the Administrator you want to ADD, VERY IMPORTANT WITHOUT SPACES AND ONLY NUMBERS", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(AddAdmin.user_id)


@admin_router.message(AddAdmin.user_id, F.text)
async def add_text(message: types.Message, state: FSMContext):
    await message.answer("Admin ADDED!", reply_markup=admin_kb.as_markup(
        resize_keyboard=True))
    await my_admins_list_add(int(message.text))
    await state.clear()








@admin_router.message(StateFilter(None), F.text == "Delete admin")
async def add_post(message: types.Message, state: FSMContext):
    admin_list = await get_my_admins_list()
    await message.answer(
        f"Enter the ID of the Administrator you want to DELETE, VERY IMPORTANT WITHOUT SPACES AND ONLY NUMBERS\n List of admins:\n {admin_list}", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(DeleteAdmin.user_id)


@admin_router.message(DeleteAdmin.user_id, F.text)
async def add_text(message: types.Message, state: FSMContext):
    if message.from_user.id != int(message.text):
        await state.update_data(user_id=message.text)
        remove_admin_list = await my_admins_list_remove(int(message.text))
        admin_list = await get_my_admins_list()
        if remove_admin_list:
            await message.answer(f"Admin REMOVED!\n List of admins:\n {admin_list}", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
        else:
            await message.answer(f"Administrator with this ID was not found\n List of admins:\n {admin_list}", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
    else:
        await message.answer("YOU CAN'T DELETE YOURSELF)))",
                             reply_markup=admin_kb.as_markup(
                                 resize_keyboard=True))
    await state.clear()











@admin_router.message(StateFilter(None), F.text == "Edit post sending times")
async def edit_time_post(message: types.Message, state: FSMContext):
    await message.answer('Select the region for which you want to change the fasting time:', reply_markup=edit_time_post_kb.as_markup(
            resize_keyboard=True), parse_mode="HTML"
    )
    await state.set_state(EditTimePost.region)



@admin_router.message(EditTimePost.region, (F.text == "Edit time post UA") | (F.text == "Edit time post RU") | (F.text == "Edit time post EN") | (F.text == "Edit time post PT") | (F.text == "Edit time post UZ") | (F.text == "Edit time post KZ"))
async def edit_time_post(message: types.Message, state: FSMContext):
    if message.text == 'Edit time post UA':
        await state.update_data(region='ua')
    elif message.text == 'Edit time post RU':
        await state.update_data(region='ru')
    elif message.text == 'Edit time post EN':
        await state.update_data(region='en')
    elif message.text == 'Edit time post PT':
        await state.update_data(region='pt')
    elif message.text == 'Edit time post UZ':
        await state.update_data(region='uz')
    elif message.text == 'Edit time post KZ':
        await state.update_data(region='kz')
    data_region = await state.get_data()
    await message.answer(
        f'The time is currently set to <b>{await get_hour_send_post(data_region["region"])}</b> \n<i>Enter the time of day\nat which posts will be sent:\n<b>Server time now:{datetime.now()}</b>\n<u>Enter only hours \n(for example: 3 or 16)</u></i>', reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True), parse_mode="HTML"
    )
    await state.set_state(EditTimePost.time)


@admin_router.message(EditTimePost.time, F.text)
async def edit_time(message: types.Message, state: FSMContext):
    try:
        int_number = int(message.text)
        if int_number > 23:
            raise ValueError()
        data_region = await state.get_data()
        if data_region['region'] == 'ua':
            await edit_hour_time(int_number, data_region['region'])
        elif data_region['region'] == 'ru':
            await edit_hour_time(int_number, data_region['region'])
        elif data_region['region'] == 'pt':
            await edit_hour_time(int_number, data_region['region'])
        elif data_region['region'] == 'en':
            await edit_hour_time(int_number, data_region['region'])
        elif data_region['region'] == 'kz':
            await edit_hour_time(int_number, data_region['region'])
        elif data_region['region'] == 'uz':
            await edit_hour_time(int_number, data_region['region'])

        await message.answer("Posting times have been changed!!", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))
    except ValueError:
        await message.answer("You entered the wrong time!!!", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))
    await state.clear()













@admin_router.message(StateFilter(None), F.text == "Delete post")
async def remove_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select the language of the region the posts you want to delete:", reply_markup=del_post_kb.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(RemovePost.region)



@admin_router.message(RemovePost.region, F.text)
async def remove_post_button(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if message.text == 'Del post UA':
        await state.update_data(region='uk')
        data = await orm_get_post(session, PostUa)
    elif message.text == 'Del post RU':
        await state.update_data(region='ru')
        data = await orm_get_post(session, PostRu)
    elif message.text == 'Del post EN':
        await state.update_data(region='en')
        data = await orm_get_post(session, PostEn)
    elif message.text == 'Del post PT':
        await state.update_data(region='pt')
        data = await orm_get_post(session, PostPt)
    elif message.text == 'Del post UZ':
        await state.update_data(region='uz')
        data = await orm_get_post(session, PostUz)
    elif message.text == 'Del post KZ':
        await state.update_data(region='kk')
        data = await orm_get_post(session, PostKz)
    else:
        data = None
    if data:
        for post in data:
            if post.type == 'photo':
                await bot.send_photo(message.chat.id, post.image,
                                     caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                                     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                         [types.InlineKeyboardButton(text=f"{post.button}",
                                                                     web_app=WebAppInfo(url=post.link))]]),
                                     parse_mode="HTML")
            if post.type == 'video':
                await bot.send_video(message.chat.id, post.image,
                                     caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                                     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                         [types.InlineKeyboardButton(text=f"{post.button}",
                                                                     web_app=WebAppInfo(url=post.link))]]),
                                     parse_mode="HTML")
            if post.type == 'animation':
                await bot.send_animation(message.chat.id, post.image,
                                     caption=f"<b>Post ID - {post.id}</b> \n{post.description}",
                                     reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                         [types.InlineKeyboardButton(text=f"{post.button}",
                                                                     web_app=WebAppInfo(url=post.link))]]),
                                     parse_mode="HTML")

            await asyncio.sleep(1/3)

        await message.answer(
            "Enter the ID of the post you want to delete:", reply_markup=admin_kb_cancel.as_markup(
                resize_keyboard=True)
        )
        await state.set_state(RemovePost.id)
    else:
        await message.answer(
            "There are no posts for this language yet.", reply_markup=del_post_kb.as_markup(
                resize_keyboard=True)
        )
        await state.set_state(RemovePost.region)



@admin_router.message(RemovePost.id, F.text)
async def remove_post_button(message: types.Message, state: FSMContext, session: AsyncSession):
    data_region = await state.get_data()
    try:
        post_id = int(message.text)
        if data_region['region'] == 'uk':
            data = await orm_delete_post(session, PostUa, post_id)
        elif data_region['region'] == 'ru':
            data = await orm_delete_post(session, PostRu, post_id)
        elif data_region['region'] == 'pt':
            data = await orm_delete_post(session, PostPt, post_id)
        elif data_region['region'] == 'en':
            data = await orm_delete_post(session, PostEn, post_id)
        elif data_region['region'] == 'kk':
            data = await orm_delete_post(session, PostKz, post_id)
        elif data_region['region'] == 'uz':
            data = await orm_delete_post(session, PostUz, post_id)
        else:
            data = None
        if data:
            await message.answer("Post deleted!", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
            await state.clear()
        else:
            raise Exception()
    except Exception as e:
        await message.answer(
            "A post with this ID does NOT exist in the database!!!", reply_markup=admin_kb.as_markup(resize_keyboard=True))
        await state.clear()












@admin_router.message(StateFilter(None), F.text == "List of users")
async def add_post(message: types.Message, session: AsyncSession, bot: Bot):
    await message.answer(
        "List of users:", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))
    users_list = await orm_get_users(session)
    for users in users_list:
        if users.username:
            await bot.send_message(message.chat.id, f"@{users.username} \nregistered in the bot {users.created} \nlast update {users.updated}")
        else:
            if users.firstname:
                await bot.send_message(message.chat.id, f"{users.firstname} \nregistered in the bot {users.created} \nlast update {users.updated}")
            else:
                await bot.send_message(message.chat.id, f"{users.lastname} \nregistered in the bot {users.created} \nlast update {users.updated}")




@admin_router.message(StateFilter(None), F.text == "Get Database FILE")
async def add_post(message: types.Message, session: AsyncSession,  bot: Bot):
    users_dict = await orm_get_users(session)
    await message.answer(
        "Here is your database:", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))
    async with aiosqlite.connect('data_dump_fs.db') as conn:
        await insert_users_from_dict(conn, users_dict)
    await bot.send_document(message.chat.id, FSInputFile("data_dump_fs.db"))
    await delete_database()











@admin_router.message(StateFilter(None), F.text == "Add post")
async def add_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select a region for your post:", reply_markup=add_post_kb.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(AddPost.region)


@admin_router.message(AddPost.region, F.text)
async def add_post_region(message: types.Message, state: FSMContext):
    if message.text == 'Post UA':
        await state.update_data(region='uk')
    elif message.text == 'Post RU':
        await state.update_data(region='ru')
    elif message.text == 'Post EN':
        await state.update_data(region='en')
    elif message.text == 'Post PT':
        await state.update_data(region='pt')
    elif message.text == 'Post UZ':
        await state.update_data(region='uz')
    elif message.text == 'Post KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Enter post description:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(AddPost.description)


@admin_router.message(AddPost.description, F.text)
async def add_text(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the link for the post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPost.link)


@admin_router.message(AddPost.link, F.text)
async def add_link(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Enter the name of the button:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPost.button)


@admin_router.message(AddPost.button, F.text)
async def add_button_post(message: types.Message, state: FSMContext):
    await state.update_data(button=message.text)
    await message.answer("Upload an image for your post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(AddPost.image)


@admin_router.message(AddPost.image)
async def add_image(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(image=message.photo[-1].file_id)
        await state.update_data(type='photo')
    if message.content_type == ContentType.VIDEO:
        await state.update_data(image=message.video.file_id)
        await state.update_data(type='video')
    if message.content_type == ContentType.ANIMATION:
        await state.update_data(image=message.animation.file_id)
        await state.update_data(type='animation')
    data = await state.get_data()
    await message.answer("You Post:", reply_markup=check_add_post_kb.as_markup(
        resize_keyboard=True))
    if data['type'] == 'photo':
        await bot.send_photo(message.chat.id, data['image'], caption=data['description'],
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                 text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    if data['type'] == 'video':
        await bot.send_video(message.chat.id, data['image'], caption=data['description'],
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                 text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    if data['type'] == 'animation':
        await bot.send_animation(message.chat.id, data['image'], caption=data['description'],
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                     text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    await state.set_state(AddPost.check)


@admin_router.message(AddPost.check)
async def add_post_db(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    try:
        if data['region'] == 'uk':
            await orm_add_post(session, PostUa, data)
        if data['region'] == 'ru':
            await orm_add_post(session, PostRu, data)
        if data['region'] == 'pt':
            await orm_add_post(session, PostPt, data)
        if data['region'] == 'en':
            await orm_add_post(session, PostEn, data)
        if data['region'] == 'kk':
            await orm_add_post(session, PostKz, data)
        if data['region'] == 'uz':
            await orm_add_post(session, PostUz, data)
        await state.clear()
        await message.answer("Post added!", reply_markup=admin_kb.as_markup(
            resize_keyboard=True))
    except Exception as e:
        await message.answer(
            f"ERROR: \n{str(e)}\n Contact the programmer, he wants money again", reply_markup=admin_kb.as_markup(resize_keyboard=True))
        await state.clear()











@admin_router.message(StateFilter(None), F.text == "Send post NOW")
async def send_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select a region for your post:", reply_markup=send_post_kb_region.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(SendPost.region)


@admin_router.message(SendPost.region, F.text)
async def send_pos_region(message: types.Message, state: FSMContext):
    if message.text == 'Send UA':
        await state.update_data(region='uk')
    elif message.text == 'Send RU':
        await state.update_data(region='ru')
    elif message.text == 'Send EN':
        await state.update_data(region='en')
    elif message.text == 'Send PT':
        await state.update_data(region='pt')
    elif message.text == 'Send UZ':
        await state.update_data(region='uz')
    elif message.text == 'Send KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Enter post description:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(SendPost.description)


@admin_router.message(SendPost.description, F.text)
async def add_text_send(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the link for the post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPost.link)


@admin_router.message(SendPost.link, F.text)
async def add_link_send(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Enter the name of the button:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPost.button)


@admin_router.message(SendPost.button, F.text)
async def add_button_send(message: types.Message, state: FSMContext):
    await state.update_data(button=message.text)
    await message.answer("Upload an image for your post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPost.image)


@admin_router.message(SendPost.image)
async def add_image_send(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == ContentType.PHOTO:
        await state.update_data(image=message.photo[-1].file_id)
        await state.update_data(type='photo')
    if message.content_type == ContentType.VIDEO:
        await state.update_data(image=message.video.file_id)
        await state.update_data(type='video')
    if message.content_type == ContentType.ANIMATION:
        await state.update_data(image=message.animation.file_id)
        await state.update_data(type='animation')
    data = await state.get_data()
    await message.answer("You Post:", reply_markup=send_post_kb.as_markup(
            resize_keyboard=True))
    if data['type'] == 'photo':
        await bot.send_photo(message.chat.id, data['image'], caption=data['description'],
                                                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    if data['type'] == 'video':
        await bot.send_video(message.chat.id, data['image'], caption=data['description'],
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                 text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    if data['type'] == 'animation':
        await bot.send_animation(message.chat.id, data['image'], caption=data['description'],
                             reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
                                 text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
    await state.set_state(SendPost.send)


@admin_router.message(SendPost.send, F.text == "Send")
async def post_send_now(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    chat_id_number = await get_chat_id_number()
    if chat_id_number:
        chat_id_set_region = [key for key, value in chat_id_number.copy().items() if value == data['region']]
        if chat_id_set_region:
            await message.answer("Post send!", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
            for key in chat_id_set_region:
                print("Post")
                users_chat_ids = await get_users_chat_on_id()
                admins_list_id_on = await get_admins_on()
                if key not in users_chat_ids and key not in admins_list_id_on:
                    try:
                        if data['type'] == 'photo':
                            await bot.send_photo(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=data['button'],web_app=WebAppInfo(url=data['link']))]]))
                        if data['type'] == 'video':
                            await bot.send_video(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(
                                                     inline_keyboard=[[types.InlineKeyboardButton(
                                                         text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                        if data['type'] == 'animation':
                            await bot.send_animation(key, data['image'], caption=data['description'],
                                                     reply_markup=types.InlineKeyboardMarkup(
                                                         inline_keyboard=[[types.InlineKeyboardButton(
                                                             text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                    except exceptions.TelegramForbiddenError as e:
                        print(f"Пользователь заблокировал бота: {e}")

                    except Exception as e:
                        print(f"Произошла ошибка при отправке сообщения: {e}")
        else:
            await message.answer("We don't have users who speak this language yet(", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
    await state.clear()

