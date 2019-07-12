from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackDialog(StatesGroup):
    enter_feedback = State()
