
import aiofiles
import ujson
from aiogram.types import FSInputFile



with open("data_users_language.json", "r") as jsonlng:
    botlang_json = ujson.load(jsonlng)



with open("users_contact.json", "r") as file:
    users_contact = ujson.load(file)
with open("chat_id_number.json", "r") as file_chat_id_number:
    chat_id_number_json = ujson.load(file_chat_id_number)




users_chat_on_id = {}
users_chat_on_id_invert = {}
admins_on = []
users_chat_history = {}
chat_id_number = {}
hour_time = 12
list_users_update = {}
list_users_id_message = {}


botlang = {}
for key, value in botlang_json.items():
    botlang[int(key)] = value


for key, value in chat_id_number_json.items():
    chat_id_number[int(key)] = value


async def get_list_users_id_message():
    global list_users_id_message
    return list_users_id_message


async def add_to_list_users_id_message(chat_id, list_id):
    global list_users_id_message
    for mess_id in list_id:
        if chat_id not in list_users_id_message:
            list_users_id_message[chat_id] = []
        list_users_id_message[chat_id].append(mess_id)


async def remove_to_list_users_id_message(chat_id, list_id):
    global list_users_id_message

    for mess_id in list_id:
        list_users_id_message[chat_id].remove(mess_id)


async def user_get_update(user_id):
    global list_users_update
    return list_users_update[user_id]

async def user_set_update(user_id, datatime):
    global list_users_update
    list_users_update[user_id] = datatime


async def get_hour_send_post():
    global hour_time
    return hour_time

async def edit_hour_time(time):
    global hour_time
    hour_time = time

async def get_chat_id_number():
    global chat_id_number
    return chat_id_number


async def get_chat_id_number_user(chat_id):
    global chat_id_number
    return chat_id_number[chat_id]


async def save_chat_id_number(data):
    global chat_id_number
    chat_id_number = data


async def del_chat_id_number(chat_id):
    global chat_id_number
    del chat_id_number[chat_id]


async def edit_chat_id_number(chat_id, lang):
    global chat_id_number
    chat_id_number[chat_id] = lang



async def get_admins_on():
    global admins_on
    return admins_on


async def add_admins_on(id):
    global admins_on
    admins_on.append(id)


async def remove_admins_on(id):
    if id in admins_on:
        admins_on.remove(id)


async def save_botlang(data):
    global botlang
    botlang = data


async def get_botlang():
    global botlang
    return botlang


async def save_local_chat_id_number():
    global chat_id_number
    with open("chat_id_number.json", "w") as chat_id_number_file:
        ujson.dump(botlang, chat_id_number_file)


async def save_local_botlang():
    global botlang
    with open("botlang.json", "w") as botlang_file:
        ujson.dump(botlang, botlang_file)


async def set_botlang(data):
    async with aiofiles.open("data_users_language.json", "w") as json_file:
        await json_file.write(ujson.dumps(data))


async def get_users_contact():
    global users_contact
    return users_contact


async def get_user_contact(user_id):
    global users_contact
    return users_contact[user_id]


async def save_new_user_contact(user_id, id_contact):
    global users_contact
    users_contact[user_id] = id_contact


async def write_to_local_data_user_contact():
    async with aiofiles.open("users_contact.json", "w") as json_file:
        await json_file.write(ujson.dumps(users_contact))

async def get_users_chat_on_id():
    global users_chat_on_id
    return users_chat_on_id


async def get_users_chat_on_id_invert():
    global users_chat_on_id_invert
    return users_chat_on_id_invert


async def add_user_chat_on_id(user_chat_id, id_chat):
    global users_chat_on_id
    global users_chat_on_id_invert
    users_chat_on_id[user_chat_id] = id_chat
    users_chat_on_id_invert[id_chat] = user_chat_id


async def get_user_number_chat_hp(user_chat_id):
    global users_chat_on_id
    return users_chat_on_id[user_chat_id]


async def get_user_number_chat_invert(chat_id_hp):
    global users_chat_on_id_invert
    return users_chat_on_id[chat_id_hp]


async def remove_user_chat_on_id(user_chat_id):
    global users_chat_on_id
    global users_chat_on_id_invert
    keys_to_remove = []
    del users_chat_on_id[user_chat_id]
    for key, value in users_chat_on_id_invert.items():
        if value == user_chat_id:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del users_chat_on_id_invert[key]


async def get_history_chat(chat_id):
    global users_chat_history
    return users_chat_history.get(chat_id, False)


async def add_to_history_chat(chat_id, number_messague):
    global users_chat_history
    if chat_id in users_chat_history:
        users_chat_history[chat_id].append(number_messague)
    else:
        users_chat_history[chat_id] = [number_messague]

async def remove_to_history_chat(chat_id):
    global users_chat_history
    try:
        del users_chat_history[chat_id]
    except KeyError:
        print(f"Ключ {chat_id} отсутствует в словаре.")

