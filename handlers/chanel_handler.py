from aiogram import Router, types, F, Bot, exceptions

from database.list_users import get_chat_id_number, get_users_chat_on_id, get_admins_on
from filters.chat_types import ChatTypesFilter

channel_handler = Router()
channel_handler.message.filter(ChatTypesFilter(['channel']))

id_chanel = -1001815801356

@channel_handler.channel_post(F.chat.id == id_chanel)
async def channel_post_handler(channel_post: types.Message, bot: Bot):
    chat_id_number = await get_chat_id_number()
    if chat_id_number:
        for key in chat_id_number.copy():
            users_chat_ids = await get_users_chat_on_id()
            admins_list_id_on = await get_admins_on()
            if key not in users_chat_ids.copy() and key not in admins_list_id_on.copy():
                try:
                    await bot.forward_message(key, id_chanel, channel_post.message_id)
                except exceptions.TelegramForbiddenError as e:
                    print(f"Пользователь заблокировал бота: {e}")

                except Exception as e:
                    print(f"Произошла ошибка при отправке сообщения: {e}")