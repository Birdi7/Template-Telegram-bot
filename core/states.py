from aiogram.dispatcher.filters.state import State, StatesGroup

class FeedbackDialog(StatesGroup):
    enter_feedback = State()


class SendToEveryoneDialog(StatesGroup):
    enter_message = State()
