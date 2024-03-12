import os


async def insert_users_from_dict(conn, users_dict):
    # Создание таблицы, если она еще не существует
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userid INTEGER PRIMARY KEY,
            username TEXT,
            firstname TEXT,
            lastname TEXT,
            language TEXT NOT NULL,
            created TEXT NOT NULL,
            updated TEXT NOT NULL
        )
    ''')

    sql_query = '''
        INSERT INTO users (userid, username, firstname, lastname, language, created, updated) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    # Проход по каждому элементу словаря и вставка его в базу данных
    for user in users_dict:
        userid = user.userid
        username = user.username
        firstname = user.firstname
        lastname = user.lastname
        language = user.language
        created = user.created
        updated = user.updated

        # Выполнение SQL-запроса
        async with conn.execute(sql_query, (userid, username, firstname, lastname, language, created, updated)) as cursor:
            pass

    # Подтверждение изменений
    await conn.commit()


async def delete_database():
    try:
        os.remove("data_dump.db")
        print("База данных data_dump.db успешно удалена.")
    except FileNotFoundError:
        print("База данных data_dump.db не существует.")
    except Exception as e:
        print(f"Произошла ошибка при удалении базы данных data_dump.db: {e}")