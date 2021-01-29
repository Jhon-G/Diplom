from utils import (today_date, correcting_parsed_data,
                   clearing_posts_text_to_parse)
from models import Event


def request_to_database(domain):
    name = set_name_to_request_to_database(domain)

    concert, concert_date = sqlite_db(name=name, domain=domain)

    return concert, concert_date


def set_name_to_request_to_database(domain):
    if 'mutabor' in domain:
        name = 'mutabor'
    elif 'rndm.club' in domain:
        name = 'random'
    return(name)


def sqlite_db(name, domain):
    event = Event()
    today = today_date()
    has_place = event.is_exists(name)
    if (has_place) is not True:
        concert, concert_date = clearing_posts_text_to_parse(domain=domain)
        if concert_date is not None and concert_date >= today:
            event.add_event(name, concert, concert_date)
            concert, concert_date = event.get_event(name)
            if concert_date.year != today.year:
                concert_date = correcting_parsed_data(concert, concert_date, today)
        else:
            return None, None

    else:
        concert, concert_date = event.get_event(name)
        if concert_date.year != today.year:
            concert, concert_date = correcting_parsed_data(concert, concert_date, today)
        if concert_date < today:
            concert, concert_date = clearing_posts_text_to_parse(domain=domain)
            if concert and concert_date is None:
                event.update_event(name, concert, concert_date)
                concert, concert_date = event.get_event(name)
            else:
                return None, None

    return concert, concert_date

