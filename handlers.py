import vk
from datetime import datetime
from rutimeparser import parse
from utils import session_api, main_keyboard


def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!', reply_markup=main_keyboard()
    )

def get_wall_posts():
    api = session_api()
    today = datetime.now().strftime('%Y-%m-%d')
    wall_posts = api.wall.get(domain='mutabor.moscow', count=10)
    posts = wall_posts['items']
    return posts , today

def club(update, context):
    print('Вазван/Club')
    user_say = update.message.text.lower()
    if 'mutabor' in user_say:
        posts, today = get_wall_posts()
        for post in posts:
            concert = post['text']
            concert_date = parse(concert).strftime('%Y-%m-%d')
            if concert_date != None and today < concert_date:
                concert_info = f'Ближайшее мероприятие: {concert}'
                break
            elif concert_date == today:
                concert_info = f'Сегодня: {concert}'
                break
            else:
                concert_info = 'Информация не найдена'
    update.message.reply_text(concert_info, reply_markup=main_keyboard())
