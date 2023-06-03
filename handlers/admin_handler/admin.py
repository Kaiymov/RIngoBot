from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageTextIsEmpty

import html
import requests
import pytz
from datetime import datetime

from db.sqlite import DB
from data import ADMIN
from dispatcher import dp

from .custom_func import get_time_request

from .inline_kb import (paginate, send_message_users, yes_no_user, send_users_modify)
from keyboard.reply_kb import cancel_kb, admin_table

db = DB()
date_time = {}


# DELETE USER STATE
class DeleteUserStateGroup(StatesGroup):
    user_id = State()


class SendMessageAllUsers(StatesGroup):
    text = State()
    photo = State()
    inline_text = State()
    inline_url = State()
    inline_reqest_text = State()
    timeout = State()


@dp.message_handler(Text('Все 🚻'), chat_id=ADMIN)
async def cmd_get_users(message: types.Message):
    page_number = 1
    users = db.get_users_paginate(page_number)
    await message.delete()

    try:
        await message.answer(text=users, reply_markup=await paginate(page_number))
        await message.answer(text='АДМИНКА!', reply_markup=admin_table())
    except MessageTextIsEmpty:
        await message.answer(text='Нет запросов')


@dp.message_handler(Text('Удалить 🗑'), chat_id=ADMIN)
async def cmd_delete_user(message: types.Message):
    await message.delete()
    await message.answer(text='Укажите <b>ID</b> для удаления👇', reply_markup=cancel_kb())
    await DeleteUserStateGroup.user_id.set()


@dp.message_handler(Text('Рассылка 📨'), chat_id=ADMIN)
async def cmd_send_all(message: types.Message):
    await message.delete()
    await message.answer(text='Текст для сообщени🔤', reply_markup=cancel_kb())
    await SendMessageAllUsers.text.set()


# SEND MESSAGE------------------------------------------------------------
@dp.message_handler(state=SendMessageAllUsers.text, content_types=['text'])
async def send_text(message: types.Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        data['text'] = text
        photo = data.get('img')

    if photo:
        await message.answer_photo(photo=photo, caption=data['text'], reply_markup=await send_message_users(state))
    elif not photo:
        await message.answer(text=text, reply_markup=await send_message_users(state))


@dp.message_handler(state=SendMessageAllUsers.photo, content_types=['photo'])
async def send_img(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        data['img'] = message.photo[0].file_id

    await message.delete()
    await message.answer_photo(photo=data['img'], caption=data['text'],
                               reply_markup=await send_message_users(state))


@dp.message_handler(state=SendMessageAllUsers.inline_text, content_types=['text'])
async def clb_add_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['inline_text'] = message.text

    text = 'Теперь привязка ссылки🔗'
    await message.answer(text=text)
    await SendMessageAllUsers.inline_url.set()


@dp.message_handler(state=SendMessageAllUsers.inline_url, content_types=['text'])
async def clb_add_text(message: types.Message, state: FSMContext):
    try:
        requests.get(message.text)
        async with state.proxy() as data:
            data['inline_url'] = message.text
            photo = data.get('img')

        text = "Выберете какую кнопку добавить⬇️"
        await message.answer(text='Кнопка с ссылкой сохранена✅')
        if photo:
            await message.answer_photo(photo=photo, caption=text,
                                       reply_markup=await send_users_modify(state))
        elif not photo:
            await message.answer(text=text, reply_markup=await send_users_modify(state),
                                 disable_web_page_preview=True)

    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        cleaned_text = html.escape(message.text)
        await message.reply(f'<s>{cleaned_text}</s>\n'
                            'Ссылка должна начинаться c <b>(https://, http://)</b>\n'
                            '<b>Повторите ещё!</b>')


@dp.message_handler(state=SendMessageAllUsers.inline_reqest_text, content_types=['text'])
async def clb_add_request_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['inline_request_text'] = message.text

    await message.answer(text=f"Дата пример🗓({datetime.now(tz=pytz.timezone('Asia/Bishkek')).strftime('%d/%m/%Y')})\n"
                              f"\nДолжно выше указанного\n")
    await SendMessageAllUsers.timeout.set()


@dp.message_handler(state=SendMessageAllUsers.timeout, content_types=['text'])
async def clb_add_request_text(message: types.Message, state: FSMContext):
    try:
        time_deadline = await get_time_request(message.text)
        if time_deadline.days >= 0:
            async with state.proxy() as data:
                photo = data.get('img')
                data['inline_request_time'] = message.text
            date_time['timeout'] = message.text

            await message.answer(text='Кнопка запроса сохранена✅')

            text = 'Выберете какую кнопку добавить⬇️'
            if photo:
                await message.answer_photo(photo=photo, caption=text,
                                           reply_markup=await send_users_modify(state))
            elif not photo:
                await message.answer(text=text,
                                     reply_markup=await send_users_modify(state))
        else:
            await message.reply(text=f"Не должен быть ниже или равен\n"
                                     f"{datetime.now(tz=pytz.timezone('Asia/Bishkek')).strftime('%d/%m/%Y')}")

    except ValueError:
        await message.reply(text=f'<u>Неправильна раставлена дата!</u>\n\n<s>{message.text}</s>\n'
                                 f'<b>Повторите заново!</b>')


# DELETE USER-------------------------------------------------------
@dp.message_handler(state=DeleteUserStateGroup.user_id)
async def state_delete_user(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        collumn_id = int(message.text)
        if db.get_user_id(collumn_id):
            async with state.proxy() as data:
                data['id'] = collumn_id

            user_info = db.get_user_id(collumn_id)
            await message.answer(text=f'Вы уверены что хотите удалить?\n\n'
                                      f'{user_info}', reply_markup=yes_no_user())
        else:
            await message.reply('Нет в списке', reply_markup=cancel_kb())
    else:
        await message.reply(text='Должно состоять из цифр!')
