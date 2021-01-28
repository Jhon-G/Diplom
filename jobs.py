from redis_db import get_from_redis_db


def job(context):
    print('База данных обновлена')
    lst = ['mutabor', 'rndm.club']
    for i in lst:
        new_concert, new_concert_date = get_from_redis_db(i)
        context.bot.send_message(chat_id=613744476, text=f'Рассылка {new_concert}')
