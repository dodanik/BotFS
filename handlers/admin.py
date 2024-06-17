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
    edit_list_vip_last_post_id, get_list_vip_last_post_id, clear_list_vip_last_post_id, set_link_mirror, \
    set_promocode_sports, set_promocode_casino, get_promocode_sports, get_promocode_casino, get_link_mirror
from database.models import PostRu, PostEn, PostKz
from database.orm_query import orm_add_post, orm_get_users, orm_get_post, orm_delete_post, get_users_by_bonus_type
from filters.chat_types import IsAdmin, ChatTypesFilter, my_admins_list_remove, my_admins_list_add, get_my_admins_list
from func.functions import set_button_web_app_to_link

from kb.keyboard import admin_kb, admin_kb_cancel, send_post_kb, add_post_kb, check_add_post_kb, send_post_kb_region, \
    del_post_kb, delete_send_post_kb_mow_region, send_post_kb_vip, post_deletion_confirmation, edit_promo_code

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

class DeleteSendPostNow(StatesGroup):
    region = State()
    remove = State()


class DeleteSendVipPost(StatesGroup):
    region = State()
    remove = State()

class SendPostVip(StatesGroup):
    bonus = State()
    description = State()
    link = State()
    image = State()
    button = State()
    send = State()
    region = State()

class EditLinkMirror(StatesGroup):
    link = State()


class EditPromoCode(StatesGroup):
    typecode = State()
    code = State()

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
    await message.answer(
        f'The time is currently set to <b>{await get_hour_send_post()}</b> \n<i>Enter the time of day\nat which posts will be sent:\n<b>Server time now:{datetime.now()}</b>\n<u>Enter only hours \n(for example: 3 or 16)</u></i>',
        reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True), parse_mode="HTML"
    )
    await state.set_state(EditTimePost.time)



@admin_router.message(EditTimePost.time, F.text)
async def edit_time(message: types.Message, state: FSMContext):
    try:
        int_number = int(message.text)
        if int_number > 23:
            raise ValueError()
        else:
            await edit_hour_time(int_number)
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
    if message.text == 'Del post RU':
        await state.update_data(region='ru')
        data = await orm_get_post(session, PostRu)
    elif message.text == 'Del post EN':
        await state.update_data(region='en')
        data = await orm_get_post(session, PostEn)
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
        if data_region['region'] == 'ru':
            data = await orm_delete_post(session, PostRu, post_id)
        elif data_region['region'] == 'en':
            data = await orm_delete_post(session, PostEn, post_id)
        elif data_region['region'] == 'kk':
            data = await orm_delete_post(session, PostKz, post_id)
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
    if message.text == 'Post RU':
        await state.update_data(region='ru')
    elif message.text == 'Post EN':
        await state.update_data(region='en')
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
        if data['region'] == 'ru':
            await orm_add_post(session, PostRu, data)
        if data['region'] == 'en':
            await orm_add_post(session, PostEn, data)
        if data['region'] == 'kk':
            await orm_add_post(session, PostKz, data)
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
    if message.text == 'Send RU':
        await state.update_data(region='ru')
    elif message.text == 'Send EN':
        await state.update_data(region='en')
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
                            msg = await bot.send_photo(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=data['button'],web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_last_post_id(key, msg.message_id, data['region'])
                        if data['type'] == 'video':
                            msg = await bot.send_video(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(
                                                     inline_keyboard=[[types.InlineKeyboardButton(
                                                         text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_last_post_id(key, msg.message_id, data['region'])
                        if data['type'] == 'animation':
                            msg = await bot.send_animation(key, data['image'], caption=data['description'],
                                                     reply_markup=types.InlineKeyboardMarkup(
                                                         inline_keyboard=[[types.InlineKeyboardButton(
                                                             text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_last_post_id(key, msg.message_id, data['region'])
                    except exceptions.TelegramForbiddenError as e:
                        print(f"Пользователь заблокировал бота: {e}")

                    except Exception as e:
                        print(f"Произошла ошибка при отправке сообщения: {e}")
        else:
            await message.answer("We don't have users who speak this language yet(", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
    await state.clear()






@admin_router.message(StateFilter(None), F.text == "Delete last post")
async def delete_send_post_now(message: types.Message, state: FSMContext):
    await message.answer(
        "Select a region for your post:", reply_markup=delete_send_post_kb_mow_region.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(DeleteSendPostNow.region)


@admin_router.message(DeleteSendPostNow.region, F.text)
async def delete_send_pos_now_region(message: types.Message, state: FSMContext):
    if message.text == 'Delete RU':
        await state.update_data(region='ru')
    elif message.text == 'Delete EN':
        await state.update_data(region='en')
    elif message.text == 'Delete KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Are you sure you want to delete your last post?:", reply_markup=post_deletion_confirmation.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(DeleteSendPostNow.remove)




@admin_router.message(DeleteSendPostNow.remove, F.text)
async def dell_last_post(message: types.Message, bot: Bot, state: FSMContext):
    if message.text == 'Yes':
        data = await state.get_data()
        msg = await get_list_last_post_id(data["region"])
        if msg:
            for key, values in msg.copy().items():
                try:
                    await bot.delete_message(key, values)
                    await message.answer(
                        "The last post was successfully deleted.",
                        reply_markup=admin_kb.as_markup(
                            resize_keyboard=True))
                except aiogram.exceptions.TelegramBadRequest as e:
                    if "message can't be deleted for everyone" in str(e):
                        await message.answer(
                            "I have been fasting for more than 48 hours, deletion is impossible",
                            reply_markup=admin_kb.as_markup(
                                resize_keyboard=True))
                        await clear_list_last_post_id(data["region"])
                        break
                    else:
                        error_message = f"An error occurred while deleting messages for chat {key}: {e}"
                        print(error_message)
                except Exception as ex:
                    error_message = f"An unexpected error occurred: {ex}"
                    print(error_message)
            await clear_list_last_post_id(data["region"])
            await state.clear()
        else:
            await message.answer(
                "The post has not yet been published or more than 48 hours have passed since the last post.", reply_markup=admin_kb.as_markup(
                    resize_keyboard=True))
            await state.clear()
    elif message.text == 'No':
        await cancel(message, state)











@admin_router.message(StateFilter(None), F.text == "Send post VIP")
async def send_post_vip(message: types.Message, state: FSMContext):
    await message.answer(
        "Select the bonus type to send:", reply_markup=send_post_kb_vip.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(SendPostVip.bonus)


@admin_router.message(SendPostVip.bonus, F.text)
async def send_pos_vip_bonus(message: types.Message, state: FSMContext):
    if message.text == 'Send Users Bonus Sports':
        await state.update_data(bonus='sports')
    elif message.text == 'Send Users Bonus Casino':
        await state.update_data(bonus='casino')
    elif message.text == 'Send Users VIP All':
        await state.update_data(bonus='all')
    else:
        pass
    await message.answer(
        "Select post region:", reply_markup=send_post_kb_region.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(SendPostVip.region)


@admin_router.message(SendPostVip.region, F.text)
async def send_pos_vip_region(message: types.Message, state: FSMContext):
    if message.text == 'Send RU':
        await state.update_data(region='ru')
    elif message.text == 'Send EN':
        await state.update_data(region='en')
    elif message.text == 'Send KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Enter post description:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(SendPostVip.description)


@admin_router.message(SendPostVip.description, F.text)
async def add_text_send_vip(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter the link for the post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPostVip.link)


@admin_router.message(SendPostVip.link, F.text)
async def add_link_send_vip(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Enter the name of the button:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPostVip.button)


@admin_router.message(SendPostVip.button, F.text)
async def add_button_send_vip(message: types.Message, state: FSMContext):
    await state.update_data(button=message.text)
    await message.answer("Upload an image for your post:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True))
    await state.set_state(SendPostVip.image)


@admin_router.message(SendPostVip.image)
async def add_image_send_vip(message: types.Message, state: FSMContext, bot: Bot):
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
    await state.set_state(SendPostVip.send)


@admin_router.message(SendPostVip.send, F.text == "Send")
async def post_send_vip_now(message: types.Message, state: FSMContext, bot: Bot, session: AsyncSession,):
    data = await state.get_data()
    user_id_number = await get_users_by_bonus_type(session, data['bonus'])
    chat_id_number = await get_chat_id_number()
    if chat_id_number:
        chat_id_set_region = [key for key, value in chat_id_number.items() if value == data['region'] and key in user_id_number]
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
                            msg = await bot.send_photo(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=data['button'],web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_vip_last_post_id(key, msg.message_id, data['region'])
                        if data['type'] == 'video':
                            msg = await bot.send_video(key, data['image'], caption=data['description'],
                                                 reply_markup=types.InlineKeyboardMarkup(
                                                     inline_keyboard=[[types.InlineKeyboardButton(
                                                         text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_vip_last_post_id(key, msg.message_id, data['region'])
                        if data['type'] == 'animation':
                            msg = await bot.send_animation(key, data['image'], caption=data['description'],
                                                     reply_markup=types.InlineKeyboardMarkup(
                                                         inline_keyboard=[[types.InlineKeyboardButton(
                                                             text=data['button'], web_app=WebAppInfo(url=data['link']))]]))
                            await edit_list_vip_last_post_id(key, msg.message_id, data['region'])
                    except exceptions.TelegramForbiddenError as e:
                        print(f"Пользователь заблокировал бота: {e}")

                    except Exception as e:
                        print(f"Произошла ошибка при отправке сообщения: {e}")
        else:
            await message.answer("We don't have users who speak this language yet(", reply_markup=admin_kb.as_markup(
                resize_keyboard=True))
    await state.clear()






@admin_router.message(StateFilter(None), F.text == "Delete last VIP post")
async def delete_send_vip_post(message: types.Message, state: FSMContext):
    await message.answer(
        "Select a region for your post:", reply_markup=delete_send_post_kb_mow_region.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(DeleteSendVipPost.region)


@admin_router.message(DeleteSendVipPost.region, F.text)
async def delete_send_vip_post_region(message: types.Message, state: FSMContext):
    if message.text == 'Delete RU':
        await state.update_data(region='ru')
    elif message.text == 'Delete EN':
        await state.update_data(region='en')
    elif message.text == 'Delete KZ':
        await state.update_data(region='kk')
    await message.answer(
        "Are you sure you want to delete your last post?:", reply_markup=post_deletion_confirmation.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(DeleteSendVipPost.remove)




@admin_router.message(DeleteSendVipPost.remove, F.text)
async def dell_last_vip_post(message: types.Message, bot: Bot, state: FSMContext):
    if message.text == 'Yes':
        data = await state.get_data()
        msg = await get_list_vip_last_post_id(data["region"])
        if msg:
            for key, values in msg.copy().items():
                try:
                    await bot.delete_message(key, values)
                    await message.answer(
                        "The last post was successfully deleted.",
                        reply_markup=admin_kb.as_markup(
                            resize_keyboard=True))
                except aiogram.exceptions.TelegramBadRequest as e:
                    if "message can't be deleted for everyone" in str(e):
                        await message.answer(
                            "I have been fasting for more than 48 hours, deletion is impossible",
                            reply_markup=admin_kb.as_markup(
                                resize_keyboard=True))
                        await clear_list_vip_last_post_id(data["region"])
                        break
                    else:
                        error_message = f"An error occurred while deleting messages for chat {key}: {e}"
                        print(error_message)
                except Exception as ex:
                    error_message = f"An unexpected error occurred: {ex}"
                    print(error_message)
            await clear_list_vip_last_post_id(data["region"])
            await state.clear()
        else:
            await message.answer(
                "The post has not yet been published or more than 48 hours have passed since the last post.", reply_markup=admin_kb.as_markup(
                    resize_keyboard=True))
            await state.clear()
    elif message.text == 'No':
        await cancel(message, state)



@admin_router.message(StateFilter(None), F.text == "Edit link Mirror")
async def edit_link_mirror(message: types.Message, state: FSMContext):
    link = await get_link_mirror()
    await message.answer(
        f"Link now: {link} \nEnter a new link to the mirror:", reply_markup=admin_kb_cancel.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(EditLinkMirror.link)


@admin_router.message(EditLinkMirror.link, F.text)
async def save_link_mirror(message: types.Message, state: FSMContext, bot: Bot,):
    def is_valid_link(text):
        return bool(text) and "https" in text

    if is_valid_link(message.text):
        await set_link_mirror(message.text)
        await message.answer(
            "The link has been successfully changed!", reply_markup=admin_kb.as_markup(
                resize_keyboard=True)
        )
        await set_button_web_app_to_link(bot)
    else:
        await message.answer(
            "Invalid link! Please make sure the link is not empty and contains 'https'.",
            reply_markup=admin_kb.as_markup(
                resize_keyboard=True)
        )
    await state.clear()




@admin_router.message(StateFilter(None), F.text == "Edit Promo Code")
async def edit_promocodes(message: types.Message, state: FSMContext):
    await message.answer(
        "Choose which code you want to change:", reply_markup=edit_promo_code.as_markup(
            resize_keyboard=True)
    )
    await state.set_state(EditPromoCode.typecode)

@admin_router.message(EditPromoCode.typecode, F.text)
async def type_promocodes(message: types.Message, state: FSMContext):
    if message.text == 'Edit FREEBET':
        await state.update_data(typecode='freebet')
        promo = await get_promocode_sports()
        await message.answer(
            f"Promo installed now: {promo}\nEnter a new promo:", reply_markup=admin_kb_cancel.as_markup(
                resize_keyboard=True)
        )
        await state.set_state(EditPromoCode.code)
    elif message.text == 'Edit FREESPINS':
        await state.update_data(typecode='freespins')
        promo = await get_promocode_casino()
        await message.answer(
            f"Promo installed now: {promo}\nEnter a new promo:", reply_markup=admin_kb_cancel.as_markup(
                resize_keyboard=True)
        )
        await state.set_state(EditPromoCode.code)
    else:
        await message.answer(
            "Wrong promo type!", reply_markup=edit_promo_code.as_markup(
                resize_keyboard=True)
        )
        await state.set_state(EditPromoCode.typecode)


@admin_router.message(EditPromoCode.code, F.text)
async def save_promocodes(message: types.Message, state: FSMContext):
    if message.text and message.text.strip():
        data = await state.get_data()
        if data['typecode'] == 'freebet':
            await set_promocode_sports(message.text)
            await message.answer(
                "The promo code freebet has been successfully changed!", reply_markup=admin_kb.as_markup(
                    resize_keyboard=True)
            )
        elif data['typecode'] == 'freespins':
            await set_promocode_casino(message.text)
            await message.answer(
                "The promo code freespins has been successfully changed!", reply_markup=admin_kb.as_markup(
                    resize_keyboard=True)
            )
        await state.clear()
    else:
        await message.answer(
            "Invalid promo code! Please make sure the promo code is not empty.", reply_markup=admin_kb.as_markup(
                resize_keyboard=True)
        )
        await state.clear()