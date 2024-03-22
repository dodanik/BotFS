from datetime import datetime

from sqlalchemy import select, update
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