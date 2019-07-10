import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import TelegramAPIError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Optional
from loguru import logger

from utils import decorators, texts, middlewares
from database.models import user_model
from utils.states import feedback, MailingEveryoneDialog
from configs import telegram
from database import db_worker as db

logging.basicConfig(format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d at %H:%M:%S")

logger.remove()
logger.add("./logs/debug_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.DEBUG,
           colorize=False)

logger.add("./logs/info_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.INFO,
           colorize=False)

logger.add("./logs/warn_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.WARNING,
           colorize=False)
logger.add(sys.stderr, format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}", level=logging.INFO,
           colorize=False)

logging.getLogger('aiogram').setLevel(logging.INFO)

loop = asyncio.get_event_loop() # todo replace with uvloop
bot = Bot(telegram.BOT_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)

scheduler = AsyncIOScheduler()
# todo add persistent storage if you plan to save smth important in the scheduler
scheduler.start()

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda msg: msg.text.lower() == 'cancel', state='*')
async def cancel_handler(msg: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if raw_state is None:
        return None
    await state.finish()
    await bot.send_message(msg.from_user.id, 'Cancelled')


@decorators.admin
@dp.message_handler(state='*', commands=['drop'])
async def drop_command_handler(msg: types.Message):
    await db.drop_db()
    await bot.send_message(msg.from_user.id, '<b>DB dropped</b>\n /start')


@dp.message_handler(commands=['start'], state='*')
async def start_command_handler(msg: types.Message):
    await db.update_user(chat_id=msg.from_user.id,
                         username=msg.from_user.username,
                         first_name=msg.from_user.first_name,
                         last_name=msg.from_user.last_name)
    await bot.send_message(msg.chat.id, f"Hi from start!")


@dp.message_handler(commands=['help'], state='*')
async def help_command_handler(msg: types.Message):
    user = await db.get_user(chat_id=msg.from_user.id)
    await bot.send_message(msg.chat.id, f"hi from help, {user.first_name}")


@dp.message_handler(commands=['feedback'], state='*')
async def feedback_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, texts.feedback_command)
    await feedback.first()


@dp.message_handler(state=feedback.enter_feedback)
async def enter_feedback_handler(msg: types.Message, state: FSMContext):
    await msg.reply(texts.got)
    await state.finish()

    for admin in telegram.ADMIN_IDS:
        try:
            await bot.send_message(admin,
                                   f"[@{msg.from_user.username} ID: {msg.from_user.id} MESSAGE_ID: {msg.message_id}] пишет:\n{msg.text}")
        except:
            pass


@decorators.admin
@dp.message_handler(lambda msg: msg.reply_to_message is not None)
async def feedback_response_handler(msg: types.Message):
    txt = msg.reply_to_message.text
    user_info = txt[txt.find('['): txt.find(']')][1:]
    chat_id = int(user_info[user_info.find('ID:') + len('ID:') + 1:user_info.find('MESSAGE_ID')])
    msg_id = int(user_info[user_info.find('MESSAGE_ID:') + len('MESSAGE_ID:') + 1:])

    try:
        await bot.send_message(chat_id, f'Разработчик ответил следующее:\n{msg.text}', reply_to_message_id=msg_id)
    except Exception:
        pass


@decorators.admin
@dp.message_handler(commands=['send_to_everyone'])
async def send_to_everyone_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Отправьте сообщение')
    await MailingEveryoneDialog.first()


@dp.message_handler(state=MailingEveryoneDialog.enter_message)
async def enter_send_to_everyone_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Получено')
    scheduler.add_job(send_to_everyone, args=[msg.text])


async def send_to_everyone(txt):
    for u in user_model.User.objects():
        try:
            await bot.send_message(u.chat_id, txt)
        except TelegramAPIError:
            pass
        await asyncio.sleep(.5)


if __name__ == '__main__':
    middlewares.on_startup(dp)
    executor.start_polling(dp)
