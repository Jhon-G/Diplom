import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import start, club
import settings

logger = logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    my_bot = Updater(settings.API_KEY, use_context=True)

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('Club', club))
    dp.add_handler(MessageHandler(Filters.regex('^(Mutabor)$'), club))
    dp.add_handler(MessageHandler(Filters.regex('^(Random)$'), club))

    logging.info('Бот стартовал')

    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()
