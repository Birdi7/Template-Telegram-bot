from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types, Dispatcher
from core.database.db_worker import get_user
from typing import Tuple, Any


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        """
        Load user local from DB
        :param action:
        :param args:
        :return:
        """
        tg_user = types.User.get_current()
        user = await get_user(tg_user.id)
        return user.locale


