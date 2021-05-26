import sys
import json
import requests
import telegram
from telegram.error import Unauthorized
sys.path.append('.')
from daily_informer.config import API_TOKEN
from daily_informer.telegram.bot_functions import *
from daily_informer.logger import get_logger


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logger = get_logger('bot_starter')

def telegram_bot():
    try:
        logger.info('starting telegram bot')
        updater = Updater(API_TOKEN, use_context=True)
        dp = updater.dispatcher

        # Commands
        logger.debug('adding commands to bot')
        dp.add_handler(CommandHandler('start', bot_start_command))
        dp.add_handler(CommandHandler('help', bot_help_command))
        dp.add_handler(CommandHandler('register', bot_register_command))
        dp.add_handler(CommandHandler('add', bot_add_orte))


        dp.add_handler(MessageHandler(Filters.text, bot_handle_message))

        # Log all errors
        dp.add_error_handler(bot_error)

        # Run the bot
        logger.info('telegram bot ready')
        print('telegram bot ready')
        updater.start_polling(1.0)
        updater.idle()

    except Unauthorized as e:
        logger.error("Unauthorized, invalid api key?")
    except KeyboardInterrupt as e:
        logger.info("shutting down telegram bot")
        print("shutting down telegram bot")
    except Exception as e:
        logger.error(f"Exception {e} of type {type(e)} occured")

if __name__ == '__main__':
    telegram_bot()
