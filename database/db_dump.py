import os


async def insert_users_from_dict(conn, users_dict):
    # Создание таблицы, если она еще не существует
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY,
            chatid INTEGER NOT NULL,
            username TEXT,
            firstname TEXT,
            lastname TEXT,
            language TEXT NOT NULL,
            phonenumber TEXT,
            bonussport BOOLEAN,
            bonuscasino BOOLEAN,
            created TEXT NOT NULL,
            updated TEXT NOT NULL
        )
    ''')

    sql_query = '''
        INSERT INTO users (userid, chatid, username, firstname, lastname, language, phonenumber, bonussport, bonuscasino, created, updated) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Проход по каждому элементу словаря и вставка его в базу данных
    for user in users_dict:
        userid = user.userid
        chatid = user.chatid
        username = user.username
        firstname = user.firstname
        lastname = user.lastname
        language = user.language
        phonenumber = user.phonenumber
        bonussport = user.bonussport
        bonuscasino = user.bonuscasino
        created = user.created
        updated = user.updated

        # Выполнение SQL-запроса
        await conn.execute(sql_query, (userid, chatid, username, firstname, lastname, language, phonenumber, bonussport, bonuscasino, created, updated))

    # Подтверждение изменений
    await conn.commit()

async def delete_database():
    try:
        os.remove("data_dump_fs.db")
        print("База данных data_dump_fs.db успешно удалена.")
    except FileNotFoundError:
        print("База данных data_dump.db не существует.")
    except Exception as e:
        print(f"Произошла ошибка при удалении базы данных data_dump_fs.db: {e}")