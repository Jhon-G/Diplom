from utils import get_from_redis_db, today_date, main_keyboard, date


def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!', reply_markup=main_keyboard()
    )


def concert_info(domain=''):
    today = today_date()
    concert, concert_date = get_from_redis_db(domain=domain)
    if type(concert_date) is date:
        if today < concert_date and abs(concert_date - today).days >= 3:
            return(f'Ближайшее мероприятие: {concert}')
        elif today == concert_date and abs(concert_date - today).days == 0:
            return(f'Сегодня: {concert}')
        elif today < concert_date and abs(concert_date - today).days == 1:
            return(f'Завтра: {concert}')
        elif today < concert_date and abs(concert_date - today).days == 2:
            return(f'После завтра: {concert}')
        else:
            return('Информация не найдена или нет объявленных концертов')
    else:
        return('Информация не найдена или нет объявленных концертов')


def club(update, context):
    print('Вазван/Club')
    user_say = update.message.text.lower()
    if 'mutabor' in user_say:
        concert = concert_info(domain='mutabor.moscow')
    if 'random' in user_say:
        concert = concert_info(domain='rndm.club')

    update.message.reply_text(concert, reply_markup=main_keyboard())
