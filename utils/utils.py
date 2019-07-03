from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def create_button(text):
    return KeyboardButton(text=text)


def create_keyboard(*buttons, row_width=3, one_time_keyboard=True):
    nk = ReplyKeyboardMarkup(one_time_keyboard=True,
                             row_width=row_width,
                             resize_keyboard=True)
    nk.add(*buttons)
    return nk


def create_inline_callback_button(text, callback_data):
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def create_inline_keyboard(*buttons, row_width=3):
    nk = InlineKeyboardMarkup(row_width=row_width)
    nk.add(buttons)
    return nk
