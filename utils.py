from datetime import date, timedelta
import vk
import settings
from telegram import ReplyKeyboardMarkup
import redis3
from rutimeparser import parse


def today_date():
    today = date.today()
    return today


def session_api():
    session = vk.Session(access_token=settings.VK_TOKEN)
    api = vk.API(session, v=5.126)
    return api


def redis_server():
    DB = redis3.Redis(host=settings.HOST, port=settings.PORT, db=settings.DB, encoding='utf-8', decode_responses=True)
    return DB


def get_wall_posts(domain=''):
    api = session_api()
    wall_posts = api.wall.get(domain=domain, count=10)  # domain is name of group https://vk.com/ "mutabor.moscow", count if how many posts from group we take
    posts = wall_posts['items']
    return posts


def clear_posts_text_to_parse(domain=''):
    posts = get_wall_posts(domain=domain)
    for post in posts:
        post_text = post['text']
        if 'rndm.club' in domain and '|' in post_text.replace('год', '').replace('лет', ''):  # we split text to create list where [1] object will be date "day(1) mounth(january)" and here we miss posts without "|" char
            clear_concert_text = post_text.split('|', 2)
            concert_date = parse(clear_concert_text[1])

        elif 'mutabor.moscow' in domain:
            clear_concert_text = post_text.replace('лет', '')  # here we reaplace word 'years' becouse parser get mistake
            concert_date = parse(clear_concert_text)

    concert, concert_date = correct_parsed_date(post_text, concert_date)    
    return concert, concert_date


def correct_parsed_date(post_text, concert_date):
    today = today_date()
    if concert_date is not None and type(concert_date) is date:
        if concert_date.year != today.year: # if parser find date with year == 2022 we correct this to 2021
            concert_date = concert_date - timedelta(days=365)
        try:
            if concert_date >= today:
                text_date = (post_text, concert_date)
                concert = text_date[0]
                concert_date = text_date[1]
        except(ValueError):
            pass
        finally:
            return concert, concert_date


def get_from_redis_DB(domain=''):
    if 'mutabor' in domain:
        name = 'mutabor'
        concert, concert_date = redis_db(name=name, domain=domain)
    elif 'rndm.club' in domain:
        name = 'random'
        concert, concert_date = redis_db(name=name, domain=domain)
    return concert, concert_date


def redis_db(name='', domain=''):
    DB = redis_server()
    text = DB.hexists(name=name, key='text')  # mean concert text
    date = DB.hexists(name=name, key='date')  # mean concert date
    today = today_date()
    if (text and date) is not True:
        concert, concert_date = clear_posts_text_to_parse(domain=domain)
        DB.hset(name=name, key='text', value=concert)
        DB.hset(name=name, key='date', value=str(concert_date))
        concert = DB.hget(name=name, key='text')
        concert_date = parse(DB.hget(name=name, key='date'))

    else:
        concert = DB.hget(name=name, key='text')
        concert_date = parse(DB.hget(name=name, key='date'))
        if concert_date < today:
            DB.delete(name, 2)  #Delete 2 keys text and date
            return None, None

    return concert, concert_date


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Mutabor'],
        ['Random']
    ])
