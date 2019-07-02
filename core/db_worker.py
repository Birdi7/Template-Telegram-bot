from core.db_models import instance, User
from motor import motor_asyncio


async def update_user_by_chat_id(chat_id, first_name, last_name, username):
    """
        Обновление информации о пользователе
    """
    raise NotImplementedError
    # user = User.find(chat_id=chat_id)
    # if
    # try:
    #     us = User.objects.get(chat_id=chat_id)
    # except DoesNotExist:
    #     us = User(chat_id=chat_id)
    #
    # us.first_name = first_name
    # us.last_name = last_name
    # us.username = username
    #
    # try:
    #     us.save()
    # except Exception:
    #     pass


def update_user_by_message(msg):
    update_user_by_chat_id(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username)


client = motor_asyncio.AsyncIOMotorClient()
instance.init(client.test_db)