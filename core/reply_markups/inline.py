from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from core.strings import LANGUAGE_MAPPING
from core.reply_markups.callbacks.language_choice import language_callback


available_languages = InlineKeyboardMarkup()
available_languages.add(
    *list(
        InlineKeyboardButton(
            lang_name, callback_data=language_callback.new(user_locale=lang)
        ) for lang, lang_name in LANGUAGE_MAPPING.items()
    )
)


__all__ = [
    'available_languages'
]
