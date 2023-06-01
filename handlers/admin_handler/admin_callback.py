from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from db.sqlite import DB

from .admin import SendMessageAllUsers, DeleteUserStateGroup
from dispatcher import dp, bot
from .inline_kb import (callback_send_message, callback_delete_user, callback_unseen, callback_inline_btn,
                        callback_request_btn, paginate, send_users_inline, send_users_inline_btn,
                        send_users_modify, send_message_users)
from keyboard.reply_kb import admin_table
from config import ADMIN
from .custom_func import parse_msg_date, get_time_request

db = DB()


# CALLBACK DELETE USER YES OR NO
@dp.callback_query_handler(callback_delete_user.filter(), state=DeleteUserStateGroup)
async def clb_delete(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['yes_or_no'] == 'yes':
        async with state.proxy() as data:
            user_id = data['id']

        db.delete_user(user_id)

        await state.finish()
        await callback.answer(text='Успешно удален', show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text='АДМИНКА!', reply_markup=admin_table())
    elif callback_data['yes_or_no'] == 'no':
        await state.finish()
        await callback.answer(text='Удаление отменена', show_alert=True)
        await callback.message.delete()
        await callback.message.answer(text='АДМИНКА!', reply_markup=admin_table())


# CALLBACK PAGINATION USERS
@dp.callback_query_handler(callback_unseen.filter())
async def clb_pagination(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['call'] == 'next':
        page_number = int(callback_data['page']) + 1
        users = db.get_users_paginate(page_number)

        await callback.message.edit_text(text=users,
                                         reply_markup=await paginate(page_number), parse_mode='HTML')

    elif callback_data['call'] == 'back':
        page_number = int(callback_data['page']) - 1
        users = db.get_users_paginate(page_number)

        await callback.message.edit_text(text=users,
                                         reply_markup=await paginate(page_number), parse_mode='HTML')

    elif callback_data['call'] == 'close':
        await state.finish()
        await callback.message.delete()

    elif callback_data['call'] == 'pages':
        await callback.answer()


@dp.callback_query_handler(callback_send_message.filter(), state=SendMessageAllUsers)
async def clb_send_add_img(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        text = data.get('text')
        photo = data.get('img')
        inline_text = data.get('inline_text')
        inline_url = data.get('inline_url')
        request_text = data.get('inline_request_text')
        request_time = data.get('inline_request_time')

    if callback_data['msg'] == 'add_photo':
        await callback.message.edit_text(text='Отправьте фото🖼')
        await SendMessageAllUsers.photo.set()

    elif callback_data['msg'] == 'skip':
        inl_url_text = f"Ссылка: <a href='{inline_url}'>{inline_text}</a>\n\n"
        inl_req_text = f"Текст запроса: \"{request_text}\" До: {request_time}\n\n"
        answer_text = (f"{text}\n\n"
                       f"{(inl_url_text if inline_text else '')}"
                       f"{inl_req_text if request_text else ''}"
                       f"Нет ли ошибки в тексте/фото?")

        if not photo:
            await callback.message.edit_text(text=answer_text, reply_markup=send_users_inline(),
                                             disable_web_page_preview=True)
        elif photo:
            await callback.message.edit_caption(caption=answer_text, reply_markup=send_users_inline())

    elif callback_data['msg'] == 'update_img':
        await callback.message.delete()
        await callback.message.answer(text='Отправьте фото🖼 заново🔁')
        await SendMessageAllUsers.photo.set()

    elif callback_data['msg'] == 'update_text':
        await callback.message.delete()
        await callback.message.answer(text='Отправьте текст🔤 заново🔁')
        await SendMessageAllUsers.text.set()

    elif callback_data['msg'] == 'inline_btn':
        if photo:
            await callback.message.edit_caption(caption='Выберете какую кнопку добавить⬇️',
                                                reply_markup=await send_users_modify(state))
        elif not photo:
            await callback.message.edit_text(text='Выберете какую кнопку добавить⬇️',
                                             reply_markup=await send_users_modify(state))

    elif callback_data['msg'] == 'back':
        if not photo:
            await callback.message.edit_text(text=text, reply_markup=await send_message_users(state))
        elif photo:
            await callback.message.edit_caption(caption=text, reply_markup=await send_message_users(state))

    elif callback_data['msg'] == 'cancel':
        await callback.message.delete()
        await callback.message.answer('Рассылка отменена❌', reply_markup=admin_table())
        await state.finish()

    elif callback_data['msg'] == 'send_all':
        users_id = db.get_users_id()
        await callback.message.delete()

        text_msg = (f"{text}\n\n\n"
                    f"{'Действует до: '+request_time if request_text else ''}")

        for user in users_id:
            try:
                if photo and not inline_text and not request_text:
                    await bot.send_photo(chat_id=user, photo=photo, caption=text_msg)
                elif photo and request_text and not inline_text:
                    db.update_res_discount()
                    await bot.send_photo(chat_id=user, photo=photo, caption=text_msg,
                                         reply_markup=await send_users_inline_btn(state))
                elif photo and request_text and inline_text:
                    db.update_res_discount()
                    await bot.send_photo(chat_id=user, photo=photo, caption=text_msg,
                                         reply_markup=await send_users_inline_btn(state))
                elif photo and not request_text and inline_text:
                    await bot.send_photo(chat_id=user, photo=photo, caption=text_msg,
                                         reply_markup=await send_users_inline_btn(state))

                elif text and not request_text and not inline_text:
                    await bot.send_message(chat_id=user, text=text_msg)
                elif text and not request_text and inline_text:
                    await bot.send_message(chat_id=user, text=text_msg,
                                           reply_markup=await send_users_inline_btn(state))
                elif text and request_text and not inline_text:
                    db.update_res_discount()
                    await bot.send_message(chat_id=user, text=text_msg,
                                           reply_markup=await send_users_inline_btn(state))
                elif text and request_text and inline_text:
                    db.update_res_discount()
                    await bot.send_message(chat_id=user, text=text_msg,
                                           reply_markup=await send_users_inline_btn(state))

            except exceptions.BotBlocked:
                pass

            except exceptions.UserDeactivated:
                user_deleted = db.get_user(user)
                await callback.message.answer(f'{user_deleted}\n\nПользоваль деактивировал тг.акк.')

        await callback.message.answer(text='Рассылка завершена✅', reply_markup=admin_table())
        await state.finish()


@dp.callback_query_handler(callback_inline_btn.filter(), state=SendMessageAllUsers)
async def clb_add_inline(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.delete()

    if callback_data['btn'] == 'url':
        await callback.message.answer(text='🔤Текст для внешней кнопки')
        await SendMessageAllUsers.inline_text.set()

    elif callback_data['btn'] == 'request':
        await callback.message.answer(text='🔤Текст для внешнего запроса кнопки✉️')
        await SendMessageAllUsers.inline_reqest_text.set()


@dp.callback_query_handler(callback_request_btn.filter())
async def clb_request_to_admin(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['req_btn'] == 'req_to_admin':
        data = parse_msg_date(callback.message.text)
        desc = data.get('desc')
        time = data.get('time')

        time_request = await get_time_request(time)
        user = db.get_user(callback.from_user.id)

        if time_request.days < 0:
            return await callback.answer(text='К сожалею вы не успели 😭', show_alert=True)

        if db.is_req_discount(callback.from_user.id) is True:
            return await callback.answer(text='Вы уже отправили запрос', show_alert=True)

        try:
            await callback.message.delete()
        except exceptions.MessageCantBeDeleted:
            pass
        finally:
            db.update_req_discount(callback.from_user.id)
            await callback.answer(text='Через некоторое время вам ответит менеджер🕘\n',
                                  show_alert=True)

            text = f'<b>{desc}</b>\n\n{user}\n\nДо: {time}'
            [await bot.send_message(chat_id=admin, text=text) for admin in ADMIN]