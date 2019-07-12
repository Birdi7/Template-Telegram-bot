from aiogram.dispatcher.filters.state import State, StatesGroup


class MailingEveryoneDialog(StatesGroup):
    enter_message = State()
