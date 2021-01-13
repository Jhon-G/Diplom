import vk
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton

def session_api():
    session = vk.Session(access_token=settings.VK_TOKEN)
    api = vk.API(session, v=5.126)
    return api

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Mutabor'],
        ['Random']
    ])