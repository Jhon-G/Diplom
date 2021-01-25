from datetime import date, timedelta, datetime
import vk
import settings
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)
import redis3
from rutimeparser import parse


def today_date():
    '''
    Use to know today date
    '''
    today = date.today()
    return today


def session_api():
    '''
    Creating session to authy by access token in 'Vkontakte' or 'VK' (social web).
    Return API
    '''
    session = vk.Session(access_token=settings.VK_TOKEN)
    api = vk.API(session, v=5.126)
    return api


def redis_server():
    '''
    Connect to redis server.
    Select the encoding format.
    Set "decode_responses" to True.
    If you left it false, you will get data from the DB with 'b' < - bytes
    
    Example: ask redis get foo
    Answer: 'b' 100
    '''
    db = redis3.Redis(host=settings.HOST, port=settings.PORT, db=settings.DB,
                      encoding='utf-8', decode_responses=True)
    return db


def get_wall_posts(domain):
    """We get data from vk group
    
    'Domain' of group https://vk.com/ "mutabor.moscow" <- DOMAIN
    'Count' is how many posts from the group we take from top to bottom
    """
    api = session_api()
    wall_posts = api.wall.get(domain=domain, count=10)
    posts = wall_posts['items']
    return posts


def clearing_posts_text_to_parse(domain):
    '''Clearing text from words[RUS(лет, год, года),EN(years, year, years)]

    Clear 'post_text', because if you don't, the parser will get a ValueError

    !!! CRITICALLY IMPORTANT !!!
      ! USE REVERSED CYCLE !

    1. If group have fixed post, date parser will take it first and then leave from cycle.
    2. If you need post under fixed post, the easiest way to take right post, it's reversed cycle

    EXAMPLE:
    Today is 20.01.2021
    Posts from group:
        1st or fixed post"some text..... date in post 25.01.2021"
        2nd "some text..... date in post 23.01.2021"

    If you don't follow this rule you will get incorrect information about the concert.

    Take 'post' and 'post date', if 'post date' published lower than 2021 year skip it.
    For 'Random' only posts in this group have char | only in post with concert.

    Then correcting 'date_from_post' and return 'concert', 'concert_date'
    If we don't find a post with a date (greater than today or equal)
    Or the concert wasn't announced
    it will return "No, No".
    '''
    # clear text from words who can give as ValueError by parser
    posts = get_wall_posts(domain=domain)
    today = today_date()
    if 'rndm.club' in domain:
        # make "reversed" cycle because this is the easiest way to take post with right date
        for post in posts[::-1]:
            post_text = post['text']
            post_date = datetime.utcfromtimestamp(post['date']).date().year
            # if post date is 2020 year we skip that post and take next
            if post_date == today.year:
            # we split text to create list where [1] object will be date ->
            # "day(1) mounth(january)" and here we miss posts without "|" char
                if '|' in post_text.replace('год', '').replace('лет', ''):
                    clear_concert_text = post_text.split('|', 2)
                    # allowed_results=(date, None) Because parser can take datetime object
                    date_from_post = parse(clear_concert_text[1], allowed_results=(date, None))
                    concert, concert_date = correcting_parsed_data(post_text, date_from_post, today)
                    if concert_date is not None and concert_date >= today:
                        concert, concert_date = concert_text_and_date(post_text, concert_date, today)
                        return concert, concert_date
        else:
            return None, None

    elif 'mutabor.moscow' in domain:
        for post in posts:
            post_text = post['text']
            post_date = datetime.utcfromtimestamp(post['date']).date().year
            # if post date is 2020 year we skip that post and take next
            if post_date == today.year:
                # here we reaplace word 'years' becouse parser get mistake
                clear_concert_text = post_text.replace('лет', '').replace('год', '')
                date_from_post = parse(clear_concert_text, allowed_results=(date, None))
                post_text, concert_date = correcting_parsed_data(post_text, date_from_post, today)
                if concert_date is not None and concert_date >= today:
                    concert, concert_date = concert_text_and_date(post_text, concert_date, today)
                    return concert, concert_date
        else:
            return None, None


def correcting_parsed_data(post_text, date_from_post, today):
    '''Correcting parsed date from post

    If parser find post with date(23.01)<-mean 2021, he can get mistake and return
    with date 23.01.2022.
    Here we fix it and return 'corrected_date'
    Or if it's a right date, return 'correct_date'
    '''
    if date_from_post is not None and type(date_from_post) is date:
        # if parser find date with year == 2022 we correct this to 2021
        if date_from_post.year != today.year:
            corrected_date = date_from_post - timedelta(days=365)
            return post_text, corrected_date
        elif date_from_post.year == today.year:
            correct_date = date_from_post
            return post_text, correct_date


def concert_text_and_date(post_text, concert_date, today):
    '''
    A small function, so as not to write it everywhere
    '''
    concert = post_text
    concert_date = concert_date
    return concert, concert_date


def get_from_redis_db(domain):
    ''' GET 'concet' and 'concert_info' from DB

    Selecting a name to send a query to the database as a name
    '''
    if 'mutabor' in domain:
        name = 'mutabor'
        concert, concert_date = redis_db(name=name, domain=domain)
    elif 'rndm.club' in domain:
        name = 'random'
        concert, concert_date = redis_db(name=name, domain=domain)
    return concert, concert_date


def redis_db(name, domain):
    ''' HSET HGET HDELETE info from Redis DB

    1. connect to DB
    2. checking the "text" and "date" keys, if returned None
        2.1 if " None" was returned, request "concert" and "concert_date".
        2.2 if the concert wasn't announced, we will get None
            and DB return None
        2.3 if 'concert' and concert_date is not None,
            
            !!! SET DATE with str method !!!

            DB we set it with name from 'get_from_redis_db',
            key 'text' for 'concert'
            key 'date' for 'concert_date'
        2.4 after set values, we need return new values, use get
        2.5 correct our date from DB if parser get mistake
        2.6 return concert and date info

    3. checking the "text" and "date" keys, if returned True
        3.1 get 'concert' and 'concert_date'
        3.2 correct our date from DB if parser get mistake
        3.3 if 'concert_date' from DB lower then today date,
            delete one or more keys specified by names
            3.3.1 call function 'get_from_redis_db' to update DB info
                  back to step 2
        3.4 return concert and date info
    '''
    redis = redis_server()
    today = today_date()
    has_text = redis.hexists(name=name, key='text')  # mean concert text
    has_date = redis.hexists(name=name, key='date')  # mean concert date
    if (has_text and has_date) is not True:
        concert, concert_date = clearing_posts_text_to_parse(domain=domain)
        if concert_date is not None and concert_date >= today:
            redis.hset(name=name, key='text', value=concert)
            redis.hset(name=name, key='date', value=str(concert_date))
            concert = redis.hget(name=name, key='text')
            #parse date to use like object datetime:date
            concert_date = parse(redis.hget(name=name, key='date'))
            if concert_date.year != today.year:
                concert_date = correcting_parsed_data(concert, concert_date, today)
        else:
            return None, None

    else:
        concert = redis.hget(name=name, key='text')
        concert_date = parse(redis.hget(name=name, key='date'))
        if concert_date.year != today.year:
            concert, concert_date = correcting_parsed_data(concert, concert_date, today)
        if concert_date < today:
            redis.delete(name, 2)  # Delete 2 keys text and date
            # call function again to try update info
            concert, concert_date = get_from_redis_db(domain=domain)

    return concert, concert_date


def main_keyboard():
    '''
    Create keyboard for easier call command /club
    '''
    return ReplyKeyboardMarkup([
        ['Mutabor'],
        ['Random'],
    ])


def how_go_to_keyboard(location, address):
    ''' Inline keyboard for building a path to the club or find out the address

    Arguments (location, address) direct by club function
    '''
    keyboard = [
        [
            InlineKeyboardButton('Как добратсья', callback_data=location),  # 'Location'
        ], [
            InlineKeyboardButton('Адрес и метро', callback_data=address)  # 'Address'
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
