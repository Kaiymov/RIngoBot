from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from text import data_question_answer


def question_answer():
    buttons = []
    for key, value in data_question_answer.items():
        question_button = InlineKeyboardButton(value['question'], callback_data=f'question_{key}')
        buttons.append(question_button)
    ikb = InlineKeyboardMarkup(row_width=1)
    return ikb.add(*[i for i in buttons])


def url_inst():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton(text='Instagram',
                                 url='https://instagram.com/ringo_training?igshid=YmMyMTA2M2Y='))
    return ikb


def yes_no_user():
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb.add(InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no'))
    return ikb