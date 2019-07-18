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

from core.utils import decorators
from core.utils.middlewares import (
    update_middleware,
    logger_middleware
)

from core.database.models import user_model
from core.utils.states.feedback import FeedbackDialog
from core.utils.states.mailing_everyone import MailingEveryoneDialog
from core.configs import telegram
from core.database import db_worker as db
from core import strings
from core.configs.consts import LOGS_FOLDER
from core.reply_markups.inline import available_languages as available_languages_markup
from core.reply_markups.callbacks.language_choice import language_callback
from core.strings.scripts import _


logging.basicConfig(format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d at %H:%M:%S")

logger.remove()
logger.add(LOGS_FOLDER / "debug_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.DEBUG,
           colorize=False)

logger.add(LOGS_FOLDER / "info_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.INFO,
           colorize=False)

logger.add(LOGS_FOLDER / "warn_logs.log", format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
           level=logging.WARNING,
           colorize=False)
logger.add(sys.stderr, format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}", level=logging.INFO,
           colorize=False)

logging.getLogger('aiogram').setLevel(logging.INFO)

loop = asyncio.get_event_loop()
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
    await bot.send_message(msg.from_user.id, strings.cancel)


@decorators.admin
@dp.message_handler(state='*', commands=['drop'])
async def drop_command_handler(msg: types.Message):
    await db.drop_db()
    await bot.send_message(msg.from_user.id, strings.drop_cmd)


@dp.message_handler(commands=['start'], state='*')
async def start_command_handler(msg: types.Message):
    logging.info("sending message in response for /start command")
    await bot.send_message(msg.chat.id, strings.start_cmd)


@dp.message_handler(commands=['help'], state='*')
async def help_command_handler(msg: types.Message):
    user = await db.get_user(chat_id=msg.from_user.id)
    await bot.send_message(msg.chat.id, strings.help_cmd.format(name=user.first_name))


@dp.message_handler(commands=['feedback'], state='*')
async def feedback_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, strings.feedback_command)
    await FeedbackDialog.first()


@dp.message_handler(state=FeedbackDialog.enter_feedback)
async def enter_feedback_handler(msg: types.Message, state: FSMContext):
    await msg.reply(strings.got)
    await state.finish()

    for admin in telegram.ADMIN_IDS:
        try:
            await bot.send_message(admin,
                                   f"[@{msg.from_user.username} ID: {msg.from_user.id} MESSAGE_ID: {msg.message_id}]"
                                   f" пишет:\n{msg.text}")
        except TelegramAPIError:
            pass


@dp.message_handler(commands='language')
async def language_cmd_handler(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           text=strings.language_choice,
                           reply_markup=available_languages_markup)


@dp.callback_query_handler(language_callback.filter())
async def language_choice_handler(query: types.CallbackQuery, callback_data: dict):
    await query.answer()
    await db.update_user(query.from_user.id,
                         locale=callback_data['user_locale'])

    from core.strings import i18n
    i18n.ctx_locale.set(callback_data['user_locale'])

    await bot.send_message(query.from_user.id,
                           strings.language_set)


@decorators.admin
@dp.message_handler(lambda msg: msg.reply_to_message is not None)
async def feedback_response_handler(msg: types.Message):
    txt = msg.reply_to_message.text
    user_info = txt[txt.find('['): txt.find(']')][1:]
    chat_id = int(user_info[user_info.find('ID:') + len('ID:') + 1:user_info.find('MESSAGE_ID')])
    msg_id = int(user_info[user_info.find('MESSAGE_ID:') + len('MESSAGE_ID:') + 1:])

    try:
        await bot.send_message(chat_id, strings.feedback_response.format(text=msg.text),
                               reply_to_message_id=msg_id)
    except TelegramAPIError:
        pass


@decorators.admin
@dp.message_handler(commands=['send_to_everyone'])
async def send_to_everyone_command_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, strings.mailing_everyone)
    await MailingEveryoneDialog.first()


@dp.message_handler(state=MailingEveryoneDialog.enter_message)
async def mailing_everyone_handler(msg: types.Message):
    await bot.send_message(msg.chat.id, strings.got)
    scheduler.add_job(send_to_everyone, args=[msg.text])


async def send_to_everyone(txt):
    for u in user_model.User.objects():
        try:
            await bot.send_message(u.chat_id, txt)
        except TelegramAPIError:
            pass
        await asyncio.sleep(.5)


def main():
    logger.info("Compile .po and .mo before running!")

    update_middleware.on_startup(dp)
    logger_middleware.on_startup(dp)
    strings.on_startup(dp)  # enable i18n
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
