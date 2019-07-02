import asyncio
import logging

import uvloop
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import TelegramAPIError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Optional

from core import mDecorators, config, db_models
from core.mMiddlewares import mLoggingMiddleware, mUpdateUserMiddleware
from core.states import FeedbackDialog, SendToEveryoneDialog
from core import texts

logging.basicConfig(format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
                    level=logging.DEBUG, datefmt="%d-%m-%y %H:%M:%S")

logging.getLogger('aiogram').setLevel(logging.INFO)

uvloop.install()
loop = asyncio.get_event_loop()
bot = Bot(config.BOT_TOKEN, loop=loop)

scheduler = AsyncIOScheduler()
# todo add persistent storage if you plan to save smth important in the scheduler
scheduler.start()

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(mLoggingMiddleware())
dp.middleware.setup(mUpdateUserMiddleware())


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda msg: msg.text.lower() == 'cancel', state='*')
async def cancel_handler(msg: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if raw_state is None:
        return None
    await state.finish()
    await bot.send_message(msg.from_user.id, 'Cancelled')


@dp.message_handler(commands=['start'], state='*')
async def start_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, f"Hi from start!")


@dp.message_handler(commands=['help'], state='*')
async def help_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, f"hi from help")


@dp.message_handler(commands=['feedback'], state='*')
async def feedback_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, texts.feedback_command)
    await FeedbackDialog.first()


@dp.message_handler(state=FeedbackDialog.enter_feedback)
async def enter_feedback_handler(msg: types.Message, state: FSMContext):
    await msg.reply(texts.got)
    await state.finish()

    for admin in config.admin_ids:
        try:
            await bot.send_message(admin, f"[@{msg.from_user.username} ID: {msg.from_user.id} MESSAGE_ID: {msg.message_id}] пишет:\n{msg.text}")
        except:
            pass


@mDecorators.admin
@dp.message_handler(lambda msg: msg.reply_to_message is not None)
async def feedback_response_handler(msg: types.Message):
    txt = msg.reply_to_message.text
    user_info = txt[txt.find('['): txt.find(']')][1:]
    chat_id = int(user_info[user_info.find('ID:')+len('ID:')+1:user_info.find('MESSAGE_ID')])
    msg_id = int(user_info[user_info.find('MESSAGE_ID:')+len('MESSAGE_ID:')+1:])

    try:
        await bot.send_message(chat_id, f'Разработчик ответил следующее:\n{msg.text}', reply_to_message_id=msg_id)
    except Exception:
        pass


@mDecorators.admin
@dp.message_handler(commands=['send_to_everyone'])
async def send_to_everyone_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Отправьте сообщение')
    await SendToEveryoneDialog.first()


@dp.message_handler(state=SendToEveryoneDialog.enter_message)
async def enter_send_to_everyone_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Получено')
    scheduler.add_job(send_to_everyone, args=[msg.text])


async def send_to_everyone(txt):
    for u in db_models.User.objects():
        try:
            await bot.send_message(u.chat_id, txt)
        except TelegramAPIError:
            pass
        await asyncio.sleep(.5)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
