from aiogram import executor, Bot, Dispatcher, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

import time

from inline_kb import url_inst, question_answer, data_question_answer
from reply_kb import *
from sqlite import *
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# SAVE USERS
class ProfileStatesGroup(StatesGroup):
    name = State()
    phone_number = State()


async def on_startup(_):
    await bot.send_message(chat_id=5951238761, text="Бот запущен!")
    await bot.send_message(chat_id=1903059288, text="Мал Бот проснулся!")
    await start_db()


@dp.message_handler(Text('Прервать отправку🚫'), state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Вы прервали отправку заявку❌',
                         reply_markup=get_main())


@dp.message_handler(commands=['start'])
async def cmd_pars(message: types.Message):
    await message.answer(text=start_text,
                         reply_markup=get_start())
    print(message)
    await message.delete()


@dp.message_handler(commands=['get_users'])
async def cmd_get_users(message: types.Message):
    try:
        await message.answer(text=get_users())
        await message.delete()
    except:
        await message.answer(text='Нет запросов')

@dp.message_handler(Text('Конфиденциальность📖'))
async def cmd_conf(message: types.Message):
    await message.answer(text=conf_text,
                         reply_markup=get_back())


@dp.message_handler(Text('Главная'))
async def cmd_main_menu(message: types.Message):
    await message.answer(text='Вы в главном меню',
                         reply_markup=get_main())


@dp.message_handler(Text(('Продолжить▶️', 'Частые вопросы❓🤔', 'Instagram📷')))
async def cmd_request(message: types.Message):
    if message.text == 'Продолжить▶️':
        await message.answer(text=send_request_text,
                             reply_markup=get_main())
    elif message.text == 'Instagram📷':
        await message.answer(text='Подпишитесь на нашу страницу\n'
                                  'Будем благодарны!',
                             reply_markup=url_inst())
    elif message.text == 'Частые вопросы❓🤔':
        await message.answer(text='Часто задаваемые вопросы:',
                             reply_markup=question_answer())
        await message.answer(text='По остальным вопросам обращаться наставникам.☺️✅')


# SEND INFO USER
@dp.message_handler(Text('Отправить запрос📨'))
async def cmd_send_info(message: types.Message):
    if message.from_user.id in check_user():
        await message.answer('Вы уже отправили запрос\nДождитесь ответа от менеджера🕙')
    else:
        await message.reply(text="Давай тогда отправим заявку,\nи мы с вами свяжемся📞\nНазовите свое имя?",
                            reply_markup=save_cancel())
        await ProfileStatesGroup.name.set()


# VALIDATOR NAME
@dp.message_handler(lambda message: not 15 > len(message.text), content_types='text', state=ProfileStatesGroup.name)
async def check_name(message: types.Message):
    await message.reply(text='Слишком длинное')


# SAVE NAME
@dp.message_handler(state=ProfileStatesGroup.name)
async def save_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer(text='Отправьте ваш номер телефона📱\n'+
                              'Номер должен начинаться с +996')
    await ProfileStatesGroup.next()


# VALIDATOR +996
@dp.message_handler(lambda message: not message.text.startswith('+996'), state=ProfileStatesGroup.phone_number)
async def check_number(message: types.Message):
    await message.reply(text='Номер должен начинаться с +996')


# VALIDATOR 13 number
@dp.message_handler(lambda message: not len(message.text) == 13, state=ProfileStatesGroup.phone_number)
async def check_number_len(message: types.Message):
    await message.reply(text='Заполните номер полностью(13 строк )')


# SAVE PHONE NUMBER
@dp.message_handler(state=ProfileStatesGroup.phone_number)
async def save_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
        await state.finish()

    text_for_user = f"Ваши данные сохраненны!📩\nИмя: {data['name']}\n📞: {data['phone_number']}\n"
    await bot.send_message(chat_id=message.from_user.id, text=text_for_user,
                           reply_markup=get_main())

    # TIME NOW
    time_now = time.strftime('%Y/%m/%d %H:%M')
    # SAVE DATABASE
    await save_user(message.from_user.id, data['name'], data['phone_number'], time_now)

    text = f"Имя: {data['name']}\nНомер: {data['phone_number']}\nID: {message.from_user.id}"
    await bot.send_message(chat_id=5951238761, text=text)
    await bot.send_message(chat_id=1903059288, text=text)


@dp.callback_query_handler()
async def callback_answer(callback: types.CallbackQuery):
    for key, value in data_question_answer.items():
            if callback.data == f'question_{key}':
                await callback.message.answer(text=value['answer'])
                await callback.answer(text='')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

