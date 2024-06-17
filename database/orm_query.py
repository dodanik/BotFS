from datetime import datetime, timedelta

from sqlalchemy import select, update, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


from database.models import Users


async def orm_add_post(session: AsyncSession, class_table, data: dict):
    obj = class_table(
        description=data['description'],
        link=data['link'],
        image=data['image'],
        type=data['type'],
        button=data['button']
    )
    session.add(obj)
    await session.commit()


async def orm_add_post_custom(session: AsyncSession, class_table, data: dict):
    obj = class_table(
        description=data['description'],
        link=data['link'],
        image=data['image'],
        type=data['type'],
        button=data['button']
    )
    session.add(obj)
    await session.commit()


async def orm_delete_post(session: AsyncSession, class_table, post_id: int):
    post = await session.get(class_table, post_id)
    if post:
        await session.delete(post)
        await session.commit()
        return True
    else:
        return False


async def orm_get_post(session: AsyncSession, class_table):
    try:
        query = select(class_table)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")








async def orm_add_users(session: AsyncSession, data: dict):
    obj = Users(
        userid=data['userid'],
        chatid=data['chatid'],
        language=data['language'],
    )
    if 'username' in data:
        obj.username = data['username']
    if 'firstname' in data:
        obj.firstname = data['firstname']
    if 'lastname' in data:
        obj.lastname = data['lastname']
    session.add(obj)
    await session.commit()


async def check_user_exists(session: AsyncSession, userid):
    query = select(Users).where(Users.userid == userid)
    result = await session.execute(query)
    user = result.fetchone()
    if user:
        return False
    else:
        return True


async def orm_get_users(session: AsyncSession):
    try:
        query = select(Users)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")


async def orm_get_inactive_users(session: AsyncSession, days: int):
    try:
        # Рассчитываем дату, до которой пользователи считаются неактивными
        inactive_date = datetime.now() - timedelta(days=days)

        # Создаем запрос для получения всех неактивных пользователей
        query = select(Users.chatid).where(Users.updated < inactive_date)

        # Выполняем запрос
        result = await session.execute(query)

        # Возвращаем массив chatid
        return [row.chatid for row in result.scalars().all()]
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return []


async def update_user_time(session: AsyncSession, user_id: int):
    try:
        current_time = datetime.now()
        stmt = (
            update(Users)
            .where(Users.userid == user_id)
            .values(updated=current_time)
        )
        await session.execute(stmt)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Произошла ошибка при обновлении времени пользователя: {e}")
        return False


async def update_user_phonenumber(session: AsyncSession, user_id: int, new_phonenumber: str):
    try:
        stmt = (
            update(Users)
            .where(Users.userid == user_id)
            .values(phonenumber=new_phonenumber, updated=datetime.now())
        )
        await session.execute(stmt)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Произошла ошибка при обновлении номера телефона пользователя: {e}")
        return False


async def update_user_bonuses(session: AsyncSession, user_id: int, bonus_type: str = ''):
    try:
        # Установка значений в зависимости от типа бонуса
        if bonus_type == 'bonus_casino':
            bonussport = False
            bonuscasino = True
        elif bonus_type == 'bonus_sport':
            bonussport = True
            bonuscasino = False
        else:
            bonussport = False
            bonuscasino = False

        stmt = (
            update(Users)
            .where(Users.userid == user_id)
            .values(bonussport=bonussport, bonuscasino=bonuscasino, updated=datetime.now())
        )
        await session.execute(stmt)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Произошла ошибка при обновлении бонусов пользователя: {e}")
        return False


async def get_users_by_bonus_type(session: AsyncSession, bonus_type: str):
    try:
        if bonus_type == 'sports':
            query = select(Users.chatid).where(Users.bonussport == True)
        elif bonus_type == 'casino':
            query = select(Users.chatid).where(Users.bonuscasino == True)
        elif bonus_type == 'all':
            query = select(Users.chatid).where(or_(Users.bonussport == True, Users.bonuscasino == True))
        else:
            raise ValueError("Invalid bonus_type provided")

        result = await session.execute(query)
        return [row[0] for row in result.fetchall()]
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return []