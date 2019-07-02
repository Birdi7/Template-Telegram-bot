"""
In every method, use MODEL.collection methods
"""


import asyncio

from motor import motor_asyncio

from core.db_models import instance, User


async def update_user(chat_id, **kwargs):
    """
        Обновление информации о пользователе
    """
    await User.collection.update_one({"chat_id": chat_id}, {"$set": kwargs}, upsert=True)


client = motor_asyncio.AsyncIOMotorClient(host="mongodb+srv://birdi7:A0DdtfvGpLn3yha4@cluster0-aqa0h.gcp.mongodb.net/test_db?retryWrites=true&w=majority")
instance.init(client.test_db)

asyncio.get_event_loop().create_task(User.ensure_indexes())
