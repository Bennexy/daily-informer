
import sys
import json
import requests
sys.path.append('.')
from daily_informer.logger import get_logger

# Set up the logger
logger = get_logger('bot_functions')


def bot_start_command(update, context):
    update.message.reply_text('Hello there! I\'m your personal bot. Type /help to see al options!')


def bot_help_command(update, context):
    text = ""
    for key in help_commands:
        text += key + " - " + help_commands[key]['description'] + "\n"
    update.message.reply_text(text)


def custom_command(update, context):
    update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def bot_handle_message(update, context):
    text = str(update.message.text).lower()
    logger.debug(f'User ({update.message.chat.id}) says: {text}')

    # Bot response
    update.message.reply_text(text)


def bot_error(update, context):
    # Logs errors
    logger.debug(f'Update {str(update.message.text).lower()} caused error {context.error}')


help_commands = {
    "/help": {"description": "displays all functions", "function": bot_help_command},
    "/start": {"description": "sends the start message", "function": bot_start_command}
    }