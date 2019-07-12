from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware

from core.database.db_worker import update_user


class UpdateUserMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await update_user(chat_id=message.from_user.id,
                          first_name=message.from_user.first_name,
                          last_name=message.from_user.last_name,
                          username=message.from_user.username)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message and callback_query.message.from_user:
            await update_user(chat_id=callback_query.from_user.id,
                              first_name=callback_query.from_user.first_name,
                              last_name=callback_query.from_user.last_name,
                              username=callback_query.from_user.username)


def on_startup(dp: Dispatcher):
    dp.middleware.setup(UpdateUserMiddleware())
