import aiohttp
import ujson


from database.list_users import get_user_contact, save_new_user_contact, get_users_contact, add_user_chat_on_id, \
    get_user_number_chat_hp, add_to_history_chat

with open("config_HP.json", "r") as filetoken:
    token_api = ujson.load(filetoken)

TOKEN_API = token_api.get('HELPCRUNCH_API')

headers = {'Authorization': f'Bearer {TOKEN_API}'}


async def get_headers():
    global headers
    return headers


async def search_user(message):
    user_contact = await get_users_contact()
    if str(message.from_user.id) not in user_contact:
        from_user_id = "user_" + str(message.from_user.id)
        create_contact = {
            "name": message.from_user.first_name,
            "userId": from_user_id,
            "locale": message.from_user.language_code,
            "createdFrom": "telegram",
            "tags": [
                {
                    "name": "TG110",
                    "color": "#008304"
                }
            ]
        }
        url_creat_contact = 'https://api.helpcrunch.com/v1/customers'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url_creat_contact, json=create_contact, headers=headers) as response:
                    if response.status == 201:
                        json_response = await response.json()
                        user_id = json_response.get('id')
                        await save_new_user_contact(str(message.from_user.id), user_id)
                        print("Create Contact")
                    elif response.status == 400:
                        error_response = await response.json()
                        print(error_response)
                        raise ValueError(f"Ошибка 400: {error_response['errors'][0]['message']} ошибка туу")
                    elif response.status == 401:
                        error_response = await response.json()
                        raise ValueError(f"Ошибка 401: {error_response['errors'][0]['message']}")
                    elif response.status == 404:
                        error_response = await response.json()
                        raise ValueError(f"Ошибка 404: {error_response['errors'][0]['message']}")
                    elif response.status == 429:
                        error_response = await response.json()
                        raise ValueError(f"Ошибка 429: {error_response['errors'][0]['message']}")
                    else:
                        raise ValueError(f"Непредвиденный статус код: {response.status}")

            except aiohttp.ClientError as e:
                print(f"Ошибка соединения создания контакта: {e}")
                return None
    else:
        print("Создание пропущено")


async def create_chat(message):
    await get_users_contact()
    number_contact = await get_user_contact(str(message.from_user.id))
    chat_data = {
            "customer": number_contact,
            "application": 35
    }
    url_crate_chat = 'https://api.helpcrunch.com/v1/chats'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url_crate_chat, json=chat_data, headers=headers) as response:
                if response.status == 201:
                    json_response = await response.json()
                    user_chat_id = json_response.get('id')
                    await add_user_chat_on_id(message.chat.id, user_chat_id)
                    print("Creat chat DONE")
                elif response.status == 400:
                    error_response = await response.json()
                    print(error_response)
                    raise ValueError(f"Ошибка 400: {error_response['errors'][0]['message']} создание чата")
                elif response.status == 401:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 401: {error_response['errors'][0]['message']}")
                elif response.status == 404:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 404: {error_response['errors'][0]['message']}")
                elif response.status == 429:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 429: {error_response['errors'][0]['message']}")
                else:
                    raise ValueError(f"Непредвиденный статус код: {response.status}")

        except aiohttp.ClientError as e:
            print(f"Ошибка соединения создания чата: {e}")
            return None


async def create_message(user_chat_id, text):
    user_chat_hp_number = await get_user_number_chat_hp(user_chat_id)
    url_create_message = 'https://api.helpcrunch.com/v1/messages'
    send_message = {
                        "chat": user_chat_hp_number,
                        "text": text,
                        "type": "message"
                    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url_create_message, json=send_message, headers=headers) as response:
                if response.status == 201:
                    json_response = await response.json()
                    await add_to_history_chat(user_chat_id, json_response['id'])
                    print("message send" f'{json_response}')
                elif response.status == 400:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 400: {error_response['errors'][0]['message']}")
                elif response.status == 401:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 401: {error_response['errors'][0]['message']}")
                elif response.status == 404:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 404: {error_response['errors'][0]['message']}")
                elif response.status == 429:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 429: {error_response['errors'][0]['message']}")
                else:
                    raise ValueError(f"Непредвиденный статус код: {response.status}")

        except aiohttp.ClientError as e:
            print(f"Ошибка соединения отправки сообщения: {e}")
            return None


async def update_status_chat(chat_id):
    user_chat_hp_number = await get_user_number_chat_hp(chat_id)
    url_create_message = 'https://api.helpcrunch.com/v1/chats/status'
    send_status = {
                      "id": user_chat_hp_number,
                      "status": "closed"
                }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(url_create_message, json=send_status, headers=headers) as response:
                if response.status == 200:
                    print('Status UPDATE')
                elif response.status == 400:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 400: {error_response['errors'][0]['message']}")
                elif response.status == 401:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 401: {error_response['errors'][0]['message']}")
                elif response.status == 404:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 404: {error_response['errors'][0]['message']}")
                elif response.status == 429:
                    error_response = await response.json()
                    raise ValueError(f"Ошибка 429: {error_response['errors'][0]['message']}")
                else:
                    raise ValueError(f"Непредвиденный статус код: {response.status}")

        except aiohttp.ClientError as e:
            print(f"Ошибка соединения обновления статуса чата: {e}")
            return None