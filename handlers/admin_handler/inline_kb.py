from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import FSMContext

from db.psql import DB

db = DB()

callback_delete_user = CallbackData('delete', 'yes_or_no')
callback_unseen = CallbackData('close', 'call', 'page')
callback_send_message = CallbackData('send', 'msg')
callback_inline_btn = CallbackData('inl_btn', 'btn')
callback_request_btn = CallbackData('inl_req', 'req_btn')


# ADMIN INLINE
async def paginate(page_number):
    ikb = InlineKeyboardMarkup()

    count_users = db.get_count_users()

    skip_size = 10
    max_pages = (count_users // skip_size) + (1 if count_users % skip_size != 0 else 0)

    page = InlineKeyboardButton(text=f'{page_number}/{max_pages}', callback_data=callback_unseen.new(call='pages',
                                                                                                     page='pages'))

    next_page = InlineKeyboardButton(text='➡️', callback_data=callback_unseen.new(call='next',
                                                                                  page=page_number))
    back_page = InlineKeyboardButton(text='⬅️', callback_data=callback_unseen.new(call='back',
                                                                                  page=page_number))
    close_page = InlineKeyboardButton(text='Закрыть❌', callback_data=callback_unseen.new(call='close',
                                                                                         page='close'))

    if page_number == 1 and page_number < max_pages:
        return ikb.add(page, next_page).row(close_page)

    elif page_number < max_pages:
        return ikb.add(back_page, page, next_page).row(close_page)

    elif page_number == max_pages and page_number > 1:
        return ikb.add(back_page, page).row(close_page)

    elif max_pages == 1:
        return ikb.add(page).row(close_page)


def yes_no_user():
    ikb = InlineKeyboardMarkup(row_width=2)
    yes = InlineKeyboardButton(text='Да', callback_data=callback_delete_user.new(yes_or_no='yes'))
    no = InlineKeyboardButton(text='Нет', callback_data=callback_delete_user.new(yes_or_no='no'))
    return ikb.add(yes, no)


def send_users_inline():
    ikb = InlineKeyboardMarkup(row_width=1)
    send_msg = InlineKeyboardButton(text='Отправить✅', callback_data=callback_send_message.new(msg='send_all'))
    back_btn = InlineKeyboardButton(text='Назад', callback_data=callback_send_message.new(msg='back'))
    cancel_msg = InlineKeyboardButton(text='Отменить🚫', callback_data=callback_send_message.new(msg='cancel'))
    return ikb.add(send_msg).row(back_btn, cancel_msg)


async def send_message_users(state: FSMContext):
    async with state.proxy() as data:
        photo = data.get('img')

    ikb = InlineKeyboardMarkup()

    add_photo = InlineKeyboardButton(text='Доб. фото', callback_data=callback_send_message.new(msg='add_photo'))
    update_photo = InlineKeyboardButton(text='Изм. фото', callback_data=callback_send_message.new(msg='update_img'))
    skip = InlineKeyboardButton(text='☑️', callback_data=callback_send_message.new(msg='skip'))
    update_text = InlineKeyboardButton(text='Изм. текст', callback_data=callback_send_message.new(msg='update_text'))
    cancel_msg = InlineKeyboardButton(text='Отменить🚫', callback_data=callback_send_message.new(msg='cancel'))

    inline_btn = InlineKeyboardButton(text='Кнопки', callback_data=callback_send_message.new(msg='inline_btn'))

    if photo:
        return ikb.add(update_photo, skip, update_text, inline_btn).row(cancel_msg)

    elif not photo:
        return ikb.add(add_photo, skip, update_text, inline_btn).row(cancel_msg)


async def send_users_modify(state: FSMContext):
    async with state.proxy() as data:
        request_text = data.get('inline_request_text')
        url_text = data.get('inline_text')

    ikb = InlineKeyboardMarkup(row_width=1)

    text_req_btn = InlineKeyboardButton(text='Запросочная', callback_data=callback_inline_btn.new(btn='request'))
    text_url_btn = InlineKeyboardButton(text='Ссылочная', callback_data=callback_inline_btn.new(btn='url'))
    cancel_msg = InlineKeyboardButton(text='Отменить🚫', callback_data=callback_send_message.new(msg='cancel'))
    back_btn = InlineKeyboardButton(text='Назад', callback_data=callback_send_message.new(msg='back'))

    menu = (back_btn, cancel_msg)

    if request_text and url_text:
        return ikb.row(*menu)
    elif not request_text and url_text:
        return ikb.add(text_req_btn).row(*menu)
    elif request_text and not url_text:
        return ikb.add(text_url_btn).row(*menu)
    else:
        return ikb.add(text_req_btn, text_url_btn).row(*menu)


async def send_users_inline_btn(state: FSMContext):
    async with state.proxy() as data:
        url_text = data.get('inline_text')
        url = data.get('inline_url')
        request_text = data.get('inline_request_text')

    ikb = InlineKeyboardMarkup(row_width=1)

    url_btn = InlineKeyboardButton(text=url_text, url=url)
    req_btn = InlineKeyboardButton(text=request_text,
                                   callback_data=callback_request_btn.new(req_btn='req_to_admin'))

    if request_text and url_text:
        return ikb.add(req_btn, url_btn)

    elif not request_text and url_text:
        return ikb.add(url_btn)

    elif request_text and not url_text:
        return ikb.add(req_btn)
