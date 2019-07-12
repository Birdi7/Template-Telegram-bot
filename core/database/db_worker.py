import asyncio

from motor import motor_asyncio

from .models.user_model import instance, User
from core.configs import (
    database
)


async def update_user(chat_id, **kwargs):
    """
        Обновление информации о пользователе
    """
    user = await User.find_one({"chat_id": chat_id})

    if user is None:
        new_user = User(chat_id=chat_id, **kwargs)
        await new_user.commit()
    else:
        setattr(user, 'chat_id', chat_id)
        for k, v in kwargs.items():
            setattr(user, k, v)


async def get_user(chat_id):
    """
        Получуние информации о пользователе
    """
    return await User.find_one({"chat_id": chat_id})


async def drop_db():
    """
        Дроп базы данных
    """
    await User.collection.drop()


client = motor_asyncio.AsyncIOMotorClient(host=database.HOST_URL)
instance.init(client[database.DB_NAME])

asyncio.get_event_loop().create_task(User.ensure_indexes())
