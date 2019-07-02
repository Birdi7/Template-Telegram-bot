import asyncio

from core.db_models import instance, User
from motor import motor_asyncio


async def update_user(chat_id, **kwargs):
    """
        Обновление информации о пользователе
    """
    user = await User.find_one({"chat_id": chat_id})

    if not user:
        user = User(chat_id=chat_id, **kwargs)
        await user.commit()
    else:
        user.update(**kwargs)
        await user.commit()


client = motor_asyncio.AsyncIOMotorClient(host="mongodb+srv://birdi7:A0DdtfvGpLn3yha4@cluster0-aqa0h.gcp.mongodb.net/test?retryWrites=true&w=majority")
instance.init(client.test_db)

asyncio.get_event_loop().create_task(User.ensure_indexes())
