#!/usr/bin/python3

from telegram.ext import Updater, CommandHandler
import time
import requests


def get_url():
    contents = requests.get('https://random.dog/woof.json').json
    url = contents['url']
    return url


def bop(update, bot):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater('1848482410:AAHAG5mnjr7r11JDikNPf3Dfc_VFWFcT2hI')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()