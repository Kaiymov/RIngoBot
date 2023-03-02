from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_text = '''Доброго времени суток🙋🏻‍♂️
Хочешь понять систему RINGO TRADE?
И начать зарабатывать большие суммы?📈💵
Тогда ознакамливайся с конфиденциальностью📊
И начинай прямо сейчас📲'''


conf_text = '''Мы стремимся обеспечивать надежность и 
конфиденциальность. Ваших личных данных, а также вашего 
персонального и бизнес-информационного контента.🕴
Мы достигаем этого посредством установления 
и соблюдения высоких стандартов безопасности.🪪
Мы используем надежные стандарты шифрования 
для защиты личных данных, хранящихся на наших серверах.📶
Также мы используем защитные меры, чтобы защитить 
информацию от несанкционированного доступа, 
использования, изменения и раскрытия.🌐 
Также хочется упомянуть, компания не несёт 
ответственность за утерю денег❗️
Будьте внимательны и удачи вам в деятельности трейдера🤝🏼💸

УПОМИНАНИЕ❗️❗️❗️: «Организация коммерческая,соблюдайте правила и стандарты нашей конторы»✅
'''


send_request_text = """Если вы согласны с условиями конфиденциальности 📚
Просмотрите часто задаваемые вопросы✅
И подпишитесь на наш INSTAGRAM📝

Оставляй «Отправить запрос📨» и наши наставники с тобой обязательно свяжутся👨‍🏫✅"""


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


def save_cancel():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Прервать отправку🚫'))
    return rkb


def save_or_update():
    rkb = ReplyKeyboardMarkup(resize_keyboard=True)
    rkb.add(KeyboardButton('Да'), KeyboardButton('Обновить'))
    return rkb



