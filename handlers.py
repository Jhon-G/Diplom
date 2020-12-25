<<<<<<< HEAD
import vk
import settings
=======
>>>>>>> 2b8be6dc5c33983cf4c10d19408d521e47538c60

def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!'
<<<<<<< HEAD
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
=======
    )
>>>>>>> 2b8be6dc5c33983cf4c10d19408d521e47538c60
