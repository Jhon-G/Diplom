from datetime import date, timedelta
from rutimeparser import parse
from utils import session_api, main_keyboard


def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!', reply_markup=main_keyboard()
    )


def get_wall_posts(domain=''):
    api = session_api()
    wall_posts = api.wall.get(domain=domain, count=10)  # domain is name of group https://vk.com/ "mutabor.moscow", count if how many posts from group we take
    posts = wall_posts['items']
    return posts


def clear_posts_text_to_parse(domain=''):
    posts = get_wall_posts(domain=domain)
    for post in posts:
        concert = post['text']
        if 'лет' in concert:
            clear_concert_text = concert.replace('лет', '')  # here we reaplace word 'years' becouse parser get mistake
            concert_date = parse(clear_concert_text)
            return concert, concert_date
        elif '|' in concert:  # we split text to create list where [1] object will be date "day(1) mounth(january)" and here we miss posts without "|" char
            clear_concert_text = concert.split('|')
            concert_date = parse(clear_concert_text[1])
            return concert, concert_date


def concert_info(domain=''):
    today = date.today()
    concert, concert_date = clear_posts_text_to_parse(domain=domain)
    if concert_date.year != today.year:  # if parser find date with year == 2022 we correct this to 2021
        concert_date = concert_date - timedelta(days=365)
    if concert_date is not None and type(concert_date) is date:
        if today == concert_date and abs(concert_date - today).days == 0:
            return f'Сегодня: {concert}'
        elif today < concert_date and abs(concert_date - today).days == 1:
            return f'Завтра: {concert}'
        elif today < concert_date and abs(concert_date - today).days == 2:
            return f'После завтра{concert}'
        elif today < concert_date and abs(concert_date - today).days >= 3:
            return f'Ближайшее мероприятие: {concert}'
        else:
            return 'Информация не найдена'


def club(update, context):
    print('Вазван/Club')
    user_say = update.message.text.lower()
    if 'mutabor' in user_say:
        concert = concert_info(domain='mutabor.moscow')
    if 'random' in user_say:
        concert = concert_info(domain='rndm.club')

    update.message.reply_text(concert, reply_markup=main_keyboard())
