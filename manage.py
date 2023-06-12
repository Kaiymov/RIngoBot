from aiogram import executor

from data import ADMIN
from dispatcher import bot, dp
from db.psql import DataBaseConnect, DB


import handlers
import logging


logging.basicConfig(format='%(name)s :: %(levelname)-8s :: %(message)s',
                    level=logging.INFO)


async def on_startup(_):
    DataBaseConnect().create_db()

    [await bot.send_message(chat_id=admin, text="Бот запущен!") for admin in ADMIN]


async def on_shutdown(_):
    logging.warning('Shutting down..')

    # DB closed
    DB().close_db()

    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown)