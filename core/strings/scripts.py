"""
Scripts which are somehow connected to locales
"""
from aiogram import Dispatcher
from core.configs.locales import LOCALES_DIR, I18N_DOMAIN
from core.utils.middlewares.aclmiddleware import ACLMiddleware

i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)


def on_startup(dp: Dispatcher):
    """
    Inits localization for the dispatcher
    """
    dp.middleware.setup(i18n)


LANGUAGE_MAPPING = {
    'ru': 'Русский',
    'en': 'Английский'
}
