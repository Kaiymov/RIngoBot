from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import logging
from config import TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')
Bot.set_current(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(format='%(name)s :: %(levelname)-8s :: %(message)s',
                    level=logging.INFO)


