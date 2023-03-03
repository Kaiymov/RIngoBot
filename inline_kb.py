from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

data_question_answer = {
    '1':
        {'question': """Стоимость обучения❓""",
         'answer': """-Наставничество стоит 2000 сом но эта сумма только за обучение,на старт у вас должно быть минимум 500 сомов.\nКурс будет длиться 3 дня.(есть задания и схемы по которым вы будете обучаться).📚"""},
    '2':
        {'question': """Есть ли гарантия на прибыль❓""",
         'answer': """Гарантия 100%,прибыль будет, при правильном понимании схемы и указании наставника.✅"""},
    '3':
        {'question': """Сколько мы на этом заработали❓""",
         'answer': """Ответ просто,так как наша организация коммерческая мы не даем отчёты на нашу прибыль.Но прибыль у нас большая,растёт с каждым днём.🤫💰"""},
    '4':
        {'question': """Что потребуется для начала❓""",
         'answer': """📍Для начала тебе нужен лишь (смартфон,ноутбук,компьютер и тд) одно из перечисленных.
📍Хорошая сеть.
📍Быстрый интернет.
📍Твоя внимательность и ум.💡"""},
    '5':
        {'question': """Сколько можно заработать в день❓""",
         'answer': """В день обычно делают … сомов.✅\nНо об этом поговорим при условии если ты уверен в себе и хочешь заработать денег используя только свой мозг.💴💲"""}
}


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

