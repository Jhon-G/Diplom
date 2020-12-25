
def start(update, context):
    print('Вазван/Start')
    user_name = update.effective_user.first_name
    update.message.reply_text(
        f'Привет {user_name}!'
    )