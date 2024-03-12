import ujson
from aiogram.filters import Filter
from aiogram import Bot, types

with open("admin_list.json", "r") as file:
    admins = ujson.load(file)

my_onchat_list: list[int] = []
my_admins_list: list[int] = admins


async def my_admins_list_add(id):
    global my_admins_list
    my_admins_list.append(id)
    await save_my_admins_list()


async def my_admins_list_remove(id):
    global my_admins_list
    if id in my_admins_list:
        my_admins_list.remove(id)
        await save_my_admins_list()
        return True
    else:
        return False


async def get_my_admins_list():
    global my_admins_list
    return my_admins_list


async def save_my_admins_list():
    global my_admins_list
    with open("admin_list.json", "w") as json_file:
        ujson.dump(my_admins_list, json_file)


async def my_list_chat_id_add(id):
    global my_onchat_list
    my_onchat_list.append(id)



async def my_list_chat_id_remove(id):
    global my_onchat_list
    my_onchat_list.remove(id)




class ChatTypesFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        global my_admins_list
        return message.from_user.id in my_admins_list


class OnChat(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        global my_onchat_list
        return message.from_user.id in my_onchat_list
