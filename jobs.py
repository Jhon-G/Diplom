from sqlite_db import request_to_database
from models import Users
from utils import today_date


def sending_out_new_events(context):
    users = Users()
    print('База данных обновлена')
    domains = ['mutabor', 'rndm.club']
    chat_id = users.get_chat_id()
    mutabor, random = users.is_exists_subscribe(chat_id)
    for domain in domains:
        new_concert, new_concert_date = request_to_database(domain)
        if mutabor is True:
            text = f'Рассылка !\n {new_concert}'
        if random is True:
            text = f'Рассылка !\n {new_concert}'
        context.bot.send_message(chat_id=chat_id, text=text)


def notification_before_event(context):
    users = Users()
    today = today_date()
    domains = ['mutabor', 'rndm.club']
    chat_id = users.get_chat_id()
    mutabor, random = users.is_exists_subscribe(chat_id)
    for domain in domains:
        concert, concert_date = request_to_database(domain)
        if concert_date is not None:
            days_left_for_event = abs(concert_date - today).days
            if days_left_for_event == 1:
                context.bot.send_message(chat_id=chat_id, text=concert)
