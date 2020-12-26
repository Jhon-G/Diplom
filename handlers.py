import vk
import settings

def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!'
    )

def club(update, context):
    print('Вазван/Club')
    user_say = update.message.text.split()
    if user_say[1].capitalize() == "Mutabor":
        session = vk.Session(access_token=settings.VK_TOKEN)
        api = vk.API(session, v=5.126)
        res = api.wall.get(domain='mutabor.moscow', count= 1)
        result = res['items'][0]['text']
        update.message.reply_text(result)
