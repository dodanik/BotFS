
import aiofiles
import ujson
from aiogram.types import FSInputFile

with open('mirror_link.txt', 'r') as fileMirror_link:
    mirror_link = fileMirror_link.read()

with open('promocodeSports.txt', 'r') as filePromocodeSports:
    promocodeSports = filePromocodeSports.read()

with open('promocodeCasino.txt', 'r') as filePromocodeCasino:
    promocodeCasino = filePromocodeCasino.read()


with open("data_users_language.json", "r") as jsonlng:
    botlang_json = ujson.load(jsonlng)



with open("users_contact.json", "r") as file:
    users_contact = ujson.load(file)

with open("chat_id_number.json", "r") as file_chat_id_number:
    chat_id_number_json = ujson.load(file_chat_id_number)

try:
    with open("user_vip_list.json", "r") as user_vip_list_file:
        user_vip_list = ujson.load(user_vip_list_file)
except (FileNotFoundError, ValueError):
    user_vip_list = []


try:
    with open("user_neactive_2_days_send_post_list.json", "r") as user_neactive_2_days_send_post_list_file:
        user_neactive_2_days_send_post_list = ujson.load(user_neactive_2_days_send_post_list_file)
except (FileNotFoundError, ValueError):
    user_neactive_2_days_send_post_list = []


try:
    with open("user_neactive_5_days_send_post_list.json", "r") as user_neactive_5_days_send_post_list_file:
        user_neactive_5_days_send_post_list = ujson.load(user_neactive_5_days_send_post_list_file)
except (FileNotFoundError, ValueError):
    user_neactive_5_days_send_post_list = []





users_chat_on_id = {}
users_chat_on_id_invert = {}
admins_on = []
users_chat_history = {}
chat_id_number = {}
list_users_update = {}
list_users_id_message = {}

list_last_post_id_ru = {}
list_last_post_id_en = {}
list_last_post_id_kz = {}

list_last_vip_post_id_ru = {}
list_last_vip_post_id_en = {}
list_last_vip_post_id_kz = {}



hour_time = 10

count_ua = 0
count_ru = 0
count_en = 0
count_pt = 0
count_kz = 0
count_uz = 0

count_custom_kz = 0
count_custom_ru = 0
count_custom_en = 0





botlang = {}
for key, value in botlang_json.items():
    botlang[int(key)] = value


for key, value in chat_id_number_json.items():
    chat_id_number[int(key)] = value


async def get_link_mirror():
    global mirror_link
    return mirror_link


async def set_link_mirror(link):
    global mirror_link
    mirror_link = link
    with open('mirror_link.txt', 'w') as fileMirror:
        fileMirror.write(mirror_link)



def get_user_vip_list():
    global user_vip_list
    return user_vip_list


async def add_user_vip_list(user_id: int):
    global user_vip_list
    # Добавление нового объекта в список
    user_vip_list.append(user_id)


async def save_user_vip_list():
    global user_vip_list
    # Запись обновленного словаря в файл
    with open("user_vip_list.json", "w") as user_vip_list_file_w:
        ujson.dump(user_vip_list, user_vip_list_file_w, indent=4)


async def get_user_neactive_2_days_send_post_list():
    global user_neactive_2_days_send_post_list
    return user_neactive_2_days_send_post_list

async def add_user_neactive_2_days_send_post_list(user_id: int):
    global user_neactive_2_days_send_post_list
    # Добавление нового объекта в список
    user_neactive_2_days_send_post_list.append(user_id)



async def get_user_neactive_5_days_send_post_list():
    global user_neactive_5_days_send_post_list
    return user_neactive_5_days_send_post_list

async def add_user_neactive_5_days_send_post_list(user_id: int):
    global user_neactive_5_days_send_post_list
    # Добавление нового объекта в список
    user_neactive_5_days_send_post_list.append(user_id)



async def save_neactive_list():
    global user_neactive_2_days_send_post_list
    global user_neactive_5_days_send_post_list

    # Запись обновленного словаря в файл
    with open("global user_neactive_5_days_send_post_list.json", "w") as user_neactive_5_days_send_post_list_file_w:
        ujson.dump(user_neactive_5_days_send_post_list, user_neactive_5_days_send_post_list_file_w, indent=4)

    with open("global user_neactive_2_days_send_post_list.json", "w") as user_neactive_2_days_send_post_list_file_w:
        ujson.dump(user_neactive_2_days_send_post_list, user_neactive_2_days_send_post_list_file_w, indent=4)



async def get_promocode_sports():
    global promocodeSports
    return promocodeSports

async def get_promocode_casino():
    global promocodeCasino
    return promocodeCasino


async def set_promocode_sports(new_promocode):
    global promocodeSports
    promocodeSports = new_promocode
    with open('promocodeSports.txt', 'w') as filePromocodeSports:
        filePromocodeSports.write(promocodeSports)

async def set_promocode_casino(new_promocode):
    global promocodeCasino
    promocodeCasino = new_promocode
    with open('promocodeCasino.txt', 'w') as filePromocodeCasino:
        filePromocodeCasino.write(promocodeCasino)


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


async def get_list_last_post_id(region):
    global list_last_post_id_ru
    global list_last_post_id_en
    global list_last_post_id_kz
    if region == 'ru':
        return list_last_post_id_ru
    if region == 'en':
        return list_last_post_id_en
    if region == 'kk':
        return list_last_post_id_kz


async def edit_list_last_post_id(chat_id, msg_id, region):
    global list_last_post_id_ru
    global list_last_post_id_en
    global list_last_post_id_kz
    if region == 'ru':
        list_last_post_id_ru[chat_id] = msg_id
    if region == 'en':
        list_last_post_id_en[chat_id] = msg_id
    if region == 'kk':
        list_last_post_id_kz[chat_id] = msg_id


async def clear_list_last_post_id(region):
    global list_last_post_id_ru
    global list_last_post_id_en
    global list_last_post_id_kz
    if region == 'ru':
        list_last_post_id_ru = {}
    if region == 'en':
        list_last_post_id_en = {}
    if region == 'kk':
        list_last_post_id_kz = {}



async def get_list_vip_last_post_id(region):
    global list_last_vip_post_id_ru
    global list_last_vip_post_id_en
    global list_last_vip_post_id_kz
    if region == 'ru':
        return list_last_vip_post_id_ru
    if region == 'en':
        return list_last_vip_post_id_en
    if region == 'kk':
        return list_last_vip_post_id_kz


async def edit_list_vip_last_post_id(chat_id, msg_id, region):
    global list_last_vip_post_id_ru
    global list_last_vip_post_id_en
    global list_last_vip_post_id_kz
    if region == 'ru':
        list_last_vip_post_id_ru[chat_id] = msg_id
    if region == 'en':
        list_last_vip_post_id_en[chat_id] = msg_id
    if region == 'kk':
        list_last_vip_post_id_kz[chat_id] = msg_id


async def clear_list_vip_last_post_id(region):
    global list_last_vip_post_id_ru
    global list_last_vip_post_id_en
    global list_last_vip_post_id_kz
    if region == 'ru':
        list_last_vip_post_id_ru = {}
    if region == 'en':
        list_last_vip_post_id_en = {}
    if region == 'kk':
        list_last_vip_post_id_kz = {}




async def get_count_region(region):
    if region == 'ua':
        return count_ua
    if region == 'ru':
        return count_ru
    if region == 'en':
        return count_en
    if region == 'pt':
        return count_pt
    if region == 'uz':
        return count_uz
    if region == 'kz':
        return count_kz


async def edit_count_region(count, region):
    global count_ua
    global count_ru
    global count_en
    global count_pt
    global count_kz
    global count_uz
    if region == 'ua':
        count_ua = count
    if region == 'ru':
        count_ru = count
    if region == 'en':
        count_en = count
    if region == 'pt':
        count_pt = count
    if region == 'uz':
        count_uz = count
    if region == 'kz':
        count_kz = count



async def get_count_custom_region(region):
    if region == 'ru':
        return count_custom_ru
    if region == 'en':
        return count_custom_en
    if region == 'kz':
        return count_custom_kz


async def edit_count_custom_region(count, region):
    global count_custom_ru
    global count_custom_en
    global count_custom_kz
    if region == 'ru':
        count_custom_ru = count
    if region == 'en':
        count_custom_en = count
    if region == 'kz':
        count_custom_kz = count


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

    # Проверка на наличие user_chat_id в словаре users_chat_on_id и удаление, если существует
    if user_chat_id in users_chat_on_id:
        del users_chat_on_id[user_chat_id]

    # Создаем список ключей для удаления
    keys_to_remove = []

    # Проходим по всем элементам словаря users_chat_on_id_invert
    for key, value in users_chat_on_id_invert.items():
        # Если значение равно user_chat_id, добавляем ключ в список для удаления
        if value == user_chat_id:
            keys_to_remove.append(key)

    # Удаляем все ключи из списка keys_to_remove из словаря users_chat_on_id_invert
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
    if chat_id in users_chat_history:
        del users_chat_history[chat_id]



