from utils import (get_from_redis_db, today_date, main_keyboard, date,
                   how_go_to)
from clubs_address import address


def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!', reply_markup=main_keyboard()
    )


def concert_info(place, domain=''):
    today = today_date()
    concert, concert_date = get_from_redis_db(domain=domain)
    place_name = place
    if type(concert_date) is date:
        if today < concert_date and abs(concert_date - today).days >= 3:
            return(f'Ближайшее мероприятие в {place_name} |\n {concert}')
        elif today == concert_date and abs(concert_date - today).days == 0:
            return(f'Сегодня в {place_name} |\n {concert}')
        elif today < concert_date and abs(concert_date - today).days == 1:
            return(f'Завтра в {place_name} |\n {concert}')
        elif today < concert_date and abs(concert_date - today).days == 2:
            return(f'После завтра в {place_name} |\n {concert}')
        else:
            return('Информация не найдена или нет объявленных концертов')
    else:
        return('Информация не найдена или нет объявленных концертов')


def club(update, context):
    print('Вазван/Club')
    user_say = update.message.text.lower()

    if 'mutabor' in user_say:
        place_name = 'Mutabor'
        location = 'Mutabor Location'
        address = 'Mutabor Address'
        concert = concert_info(domain='mutabor.moscow', place=place_name)

    if 'random' in user_say:
        place_name = 'Random'
        location = 'Random Location'
        address = 'Random Address'
        concert = concert_info(domain='rndm.club', place=place_name)

    update.message.reply_text(concert, reply_markup=how_go_to(location, address))


def send_location(update, context):
    update.callback_query.answer()
    request = update.callback_query.data

    if 'Random Location' in request:
        place = 'Random'
        update.callback_query.message.reply_location(latitude=address[place][0][0], longitude=address[place][0][1])
    elif 'Random Address' in request:
        place = 'Random'
        update.callback_query.message.reply_text(address[place][1])

    if 'Mutabor Location' in request:
        place = 'Random'
        update.callback_query.message.reply_location(latitude=address[place][0][0], longitude=address[place][0][1])
    elif 'Mutabor Address' in request:
        place = 'Random'
        update.callback_query.message.reply_text(address[place][1])
