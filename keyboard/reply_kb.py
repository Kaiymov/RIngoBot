from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Конфиденциальность📖'))
    return rkb


def get_back():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Продолжить▶️'))
    return rkb


def get_return():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Главная'))
    return rkb


def get_main():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Отправить запрос📨'))
    rkb.add(KeyboardButton('Частые вопросы❓🤔'))
    rkb.add(KeyboardButton('Instagram📷'))
    return rkb


def cancel_save():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Прервать🚫'))
    return rkb


# ADMIN COMMAND
def admin_table():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('/get_users'), KeyboardButton('/delete_user'))
    return rkb



