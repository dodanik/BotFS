from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.list_users import get_botlang, remove_user_chat_on_id, remove_to_history_chat, get_history_chat
from filters.chat_types import ChatTypesFilter, OnChat, my_list_chat_id_remove
from aiogram.enums.parse_mode import ParseMode

from handlers.messagues import update_status_chat, create_message
from kb.keyboard import chat_kb, create_keyboard, chatmessage_callback_kb

chat_router = Router()
chat_router.message.filter(ChatTypesFilter(['private']), OnChat())




@chat_router.message(StateFilter(None), (F.text.lower() == '❌ завершить чат') | (F.text.lower() == '❌ завершити чат') | (F.text.lower() == '❌ chat end'))
async def chatmessage(message: types.Message, bot: Bot):
    await my_list_chat_id_remove(message.chat.id)
    message_exists = await get_history_chat(message.chat.id)
    if message_exists:
        await update_status_chat(message.chat.id)
        await remove_to_history_chat(message.chat.id)
    botlang = await get_botlang()
    await message.answer(f'{await chatmessage_callback_kb(botlang[message.from_user.id])}', reply_markup=create_keyboard(f'{botlang[message.from_user.id]}', 'menu_kb', 2, 2, 2,2).as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Welcome!'))
    await remove_user_chat_on_id(message.chat.id)


@chat_router.message(StateFilter(None), F.text)
async def chatmessage(message: types.Message):
    await create_message(message.chat.id, message.text)
