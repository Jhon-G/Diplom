from datetime import date, timedelta, datetime
import vk
import settings
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)
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
    db = redis3.Redis(host=settings.HOST, port=settings.PORT, db=settings.DB, encoding='utf-8', decode_responses=True)
    return db


def get_wall_posts(domain=''):
    api = session_api()
    # domain is name of group https://vk.com/ "mutabor.moscow",
    # count if how many posts from group we take
    wall_posts = api.wall.get(domain=domain, count=10)
    posts = wall_posts['items']
    return posts


def clear_posts_text_to_parse(domain=''):
    # clear text from words who can give as ValueError by parser
    posts = get_wall_posts(domain=domain)
    today = today_date()
    if 'rndm.club' in domain:
        for post in reversed(posts):
            post_text = post['text']
            post_date = datetime.utcfromtimestamp(post['date']).date().year
            # if post date is 2020 year we skip that post and take next
            if post_date == today.year:
            # we split text to create list where [1] object will be date ->
            # "day(1) mounth(january)" and here we miss posts without "|" char
                if '|' in post_text.replace('год', '').replace('лет', ''):
                    clear_concert_text = post_text.split('|', 2)
                    concert_date = parse(clear_concert_text[1], allowed_results=(date, None))
                    if concert_date >= today:
                        text_date = (post_text, concert_date)
                        concert = text_date[0]
                        concert_date = text_date[1]
                        return concert, concert_date

    elif 'mutabor.moscow' in domain:
        for post in reversed(posts):
            post_text = post['text']
            post_date = datetime.utcfromtimestamp(post['date']).date().year
            # if post date is 2020 year we skip that post and take next
            if post_date == today.year:
                # here we reaplace word 'years' becouse parser get mistake
                clear_concert_text = post_text.replace('лет', '').replace('год', '')
                concert_date = parse(clear_concert_text, allowed_results=(date, None))
                post_text, concert_date = correct_parsed_date(post_text, concert_date, today)
                if concert_date >= today:
                    text_date = (post_text, concert_date)
                    concert = text_date[0]
                    concert_date = text_date[1]
                    return concert, concert_date


def correct_parsed_date(post_text, concert_date, today):
    if concert_date is not None and type(concert_date) is date:
        # if parser find date with year == 2022 we correct this to 2021
        if concert_date.year != today.year:
            correct_date = concert_date - timedelta(days=365)
            concert_date = correct_date
            return post_text, correct_date
        else:
            return post_text, concert_date


def get_from_redis_db(domain=''):
    if 'mutabor' in domain:
        name = 'mutabor'
        concert, concert_date = redis_db(name=name, domain=domain)
    elif 'rndm.club' in domain:
        name = 'random'
        concert, concert_date = redis_db(name=name, domain=domain)
    return concert, concert_date


def redis_db(name='', domain=''):
    redis = redis_server()
    text = redis.hexists(name=name, key='text')  # mean concert text
    date = redis.hexists(name=name, key='date')  # mean concert date
    today = today_date()
    if (text and date) is not True:
        concert, concert_date = clear_posts_text_to_parse(domain=domain)
        if concert_date >= today:
            redis.hset(name=name, key='text', value=concert)
            redis.hset(name=name, key='date', value=str(concert_date))
            concert = redis.hget(name=name, key='text')
            concert_date = parse(redis.hget(name=name, key='date'))

    else:
        concert = redis.hget(name=name, key='text')
        concert_date = parse(redis.hget(name=name, key='date'))
        if concert_date < today:
            redis.delete(name, 2)  # Delete 2 keys text and date
            return None, None

    return concert, concert_date


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Mutabor'],
        ['Random'],
    ])


def how_go_to(location, address):
    keyboard = [
        [
            InlineKeyboardButton('Как добратсья', callback_data=location),  # 'Location'
        ], [
            InlineKeyboardButton('Адрес и метро', callback_data=address)  # 'Address'
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
