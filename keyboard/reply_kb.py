from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db.psql import DB

db = DB()


def get_start():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Конфиденциальность📖'))
    return rkb


def get_back():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Продолжить▶️'))
    return rkb


def get_main():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Отправить запрос📨'))
    rkb.add(KeyboardButton('Частые вопросы❓🤔'))
    rkb.add(KeyboardButton('Instagram📷'))
    return rkb


def cancel_kb():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Прервать🚫'))
    return rkb


# ADMIN COMMAND
def admin_table():
    count_all = db.get_count_users()
    rkb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    rkb.add(KeyboardButton('Все 🚻'), KeyboardButton(f'{count_all}'), KeyboardButton('Удалить 🗑'),
            KeyboardButton('Рассылка 📨'))
    return rkb
