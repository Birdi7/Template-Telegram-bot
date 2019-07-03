"""
In every method, use MODEL.collection methods
"""


import asyncio

from motor import motor_asyncio

from .models.user_model import instance, User
from configs import database


async def update_user(chat_id, **kwargs):
    """
        Обновление информации о пользователе
    """
    await User.collection.update_one({"chat_id": chat_id}, {"$set": kwargs}, upsert=True)


client = motor_asyncio.AsyncIOMotorClient(host=database.HOST_URL)
instance.init(client[database.DB_NAME])

asyncio.get_event_loop().create_task(User.ensure_indexes())
