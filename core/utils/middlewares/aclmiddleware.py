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
        if user.locale is not None:  # if user set his locale
            logging.info(f"returning user.locale={user.locale}")
            return user.locale
        else:
            if tg_user.locale in LANGUAGES:  # take his clients locale if it exist
                logging.info(f"returning tg_user.locale={tg_user.locale}")
                return tg_user.locale
            else:  # else, return default
                logging.info(f"returning DEFAULT_USER_LOCALE={DEFAULT_USER_LOCALE}")
                return DEFAULT_USER_LOCALE


