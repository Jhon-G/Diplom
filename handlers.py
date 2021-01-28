from utils import (
    today_date, main_keyboard,
    date, how_go_to_keyboard
    )
from clubs_address import ADDRESS
from sqlite_db import get_from_db


def start(update, context):
    '''Command to start the bot, and tell user what he can do

    The bot takes the user name to address by nickname
    '''
    print('Вазван/Start')
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}, {chat_id}!', reply_markup=main_keyboard()
    )


def concert_info(place, domain):
    '''Create message and count days left for concert

     1. Request for database to set variables(concert and concert_date)
     2. Count days left for concert
     3. Return fstring with place name and concert info
    '''
    today = today_date()
    concert, concert_date = get_from_db(domain=domain)
    place_name = place
    if type(concert_date) is date:
        # Count days left for concert
        days_left_for_concert = abs(concert_date - today).days
        if today == concert_date and days_left_for_concert == 0:
            return(f'Сегодня в {place_name} |\n {concert}')
        elif today < concert_date and days_left_for_concert == 1:
            return(f'Завтра в {place_name} |\n {concert}')
        elif today < concert_date and days_left_for_concert == 2:
            return(f'После завтра в {place_name} |\n {concert}')
        elif today < concert_date and days_left_for_concert >= 3:
            return(f'Ближайшее мероприятие в {place_name} |\n {concert}')
        else:
            return('Информация не найдена или нет объявленных концертов')
    else:
        return('Информация не найдена или нет объявленных концертов')


def club(update, context):
    '''Sending concert info to user

    Take user message with name of place
    set the variable place to use it in concer_info function,
    then go variables (Location, address), that needed for arguments at 
    'how_go_to_keyboard' function
    '''
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

    update.message.reply_text(concert, reply_markup=how_go_to_keyboard(location, address))


def send_location(update, context):
    ''' Send location as map and address as text

    Take request and then set the variable
    Use 'place' to take data from dict with keys Mutabor and Random,
    and values in format, dict with key lacotion : value (tuple) and key address : value text
    '''
    update.callback_query.answer()
    request = update.callback_query.data

    location = 'location'
    address = 'address'

    if 'Random Location' in request:
        place = 'Random'
        latitude = ADDRESS[place][location][0]
        longitude = ADDRESS[place][location][1]

        update.callback_query.message.reply_location(latitude, longitude)
    elif 'Random Address' in request:
        place = 'Random'
        address = ADDRESS[place][address]
        update.callback_query.message.reply_text(address)

    if 'Mutabor Location' in request:
        place = 'Mutabor'
        latitude = ADDRESS[place][location][0]
        longitude = ADDRESS[place][location][1]

        update.callback_query.message.reply_location(latitude, longitude)
    elif 'Mutabor Address' in request:
        place = 'Mutabor'
        address = ADDRESS[place][address]
        update.callback_query.message.reply_text(address)
