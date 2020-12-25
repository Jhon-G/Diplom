import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
<<<<<<< HEAD
from handlers import start, club
=======
from handlers import start
>>>>>>> 2b8be6dc5c33983cf4c10d19408d521e47538c60
import settings

logging.basicConfig(filename='bot_log', level=logging.INFO)

def main():
    my_bot = Updater(settings.API_KEY, use_context=True) # Создаем бота и передаем ему ключ для авторизации на серверах Telegram

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', start))
<<<<<<< HEAD
    dp.add_handler(CommandHandler('Club', club))
=======
>>>>>>> 2b8be6dc5c33983cf4c10d19408d521e47538c60

    logging.info('Бот стартовал')

    my_bot.start_polling()
    my_bot.idle()

if __name__ == '__main__':
    main()