import logging

from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types, Dispatcher
from core.database.db_worker import get_user
from core.configs.locales import DEFAULT_USER_LOCALE, LANGUAGES
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
        super_locale = await super().get_user_locale(action, args)

        if user.locale is not None:  # if user set his locale
            return user.locale
        else:
            if super_locale in LANGUAGES:
                return super_locale
            if tg_user.locale in LANGUAGES:
                return tg_user.locale
            else:  # else, return default
                return DEFAULT_USER_LOCALE
