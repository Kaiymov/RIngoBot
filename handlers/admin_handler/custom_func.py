import pytz
from datetime import datetime


async def get_time_request(time: str):
    time_out_date = datetime.strptime(time, '%d/%m/%Y')
    time_now_date = datetime.now(tz=pytz.timezone('Asia/Bishkek'))
    time_out_zone = pytz.timezone('Asia/Bishkek').localize(time_out_date)

    time_deadline = time_out_zone - time_now_date
    return time_deadline


def parse_msg_date(text: str):
    msg = {}
    description = text.rsplit(sep='\n', maxsplit=2)[0]
    time = text.split(':')[-1].replace(' ', '')

    max_length = 60
    if len(description) > max_length:
        description = text[:max_length] + '...\n'

    msg['desc'] = description
    msg['time'] = time
    return msg
