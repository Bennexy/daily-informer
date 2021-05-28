
import sys
import json
import requests
sys.path.append('.')
from daily_informer.logger import get_logger
from daily_informer.telegram.bot_actions import *

# Set up the logger
logger = get_logger('bot_functions')

global ids
ids = []

def auth(func):
    def inner(update, context):
        global ids
        id = update.message.chat.id 
        if ids == []:
            ids = reload_ids()
        
        if id in ids:
            func(update, context)
        else:
            update.message.reply_text('please add your username to the register command-> /register <username>.\nor try /reload if you are allready registerd')
    
    return inner

def bot_start_command(update, context):
    update.message.reply_text('Hello there! I\'m your personal bot. Type /help to see al options!')

def bot_help_command(update, context):
    text = ""
    for key in help_commands:
        text += key + " - " + help_commands[key]['description'] + "\n"
    update.message.reply_text(text)
  
def bot_register_command(update, context):
    text = str(update.message.text).lower()
    id = update.message.chat.id
    text = text.split(" ")
    if len(text) != 2:
        update.message.reply_text('please add your username to the register command-> /register <username>')
    else:
        ergeb = add_user(id, text[1])
        if ergeb == True:
            update.message.reply_text(f"welcome {text[1]} and thank you for registering!")
            global ids
            ids = reload_ids()
        else:
            update.message.reply_text('an error has occured')

# hier kann noch schöner gemacht werden das wir direct nach der id des users in der db suchen
def bot_reload_command(update, context):
    global ids
    ids = reload_ids()
    update.message.reply_text('reloaded ids')

@auth
def bot_add_orte(update, context):
    text = str(update.message.text).lower()
    id = update.message.chat.id
    if text[1].lower() == 'corona' or text[1].lower() =="covid":
        del text[0]
        del text[0] 
        
        if len(text) >= 2:
            if text[0].lower() == 'landkreis':
                add_to_db(id, text)
                update.message.reply_text('added corona data to the db')
            elif text[0].lower() == 'bundesland':
                add_to_db(id, text)
                update.message.reply_text('added corona data to the db')
            elif text[0].lower() == 'land':
                add_to_db(id, text)
                update.message.reply_text('added corona data to the db')
            else:
                update.message.reply_text('please enter /add <corona> <landkreis/bundesland/land> <orte (zum hinzufügen geteilt mit einem leerzeichen)>')
        else:
            update.message.reply_text('please enter /add <corona> <landkreis/bundesland/land> <orte (zum hinzufügen geteilt mit einem leerzeichen)>')

    elif text[1].lower() == 'wetter':
        del text[0]
        if len(text) >= 0:
            add_to_db(id, text)
            update.message.reply_text('added wether data to the db')
        
        else:
            update.message.reply_text('please enter /add <wetter> <orte (zum hinzufügen geteilt mit einem leerzeichen)>')
    else:
        update.message.reply_text('please enter \n/add <wetter> <orte (zum hinzufügen geteilt mit einem leerzeichen)> \n/add <corona> <landkreis/bundesland/land> <orte (zum hinzufügen geteilt mit einem leerzeichen)>')

@auth
def bot_get_daten(update, context):
    id = update.message.chat.id 

    text = fetch_data(id)
    for data_set in text:
        for data in data_set:
            update.message.reply_text(data)

@auth
def bot_remove_orte(update, context):
    id = update.message.chat.id
    text = str(update.message.text).lower().split(' ')
    text.pop(0)
    type_ = text.pop(0)
    if type_ == 'corona' or type_ == 'covid':
        type_ = text.pop(0)
        if type_ in ['landkreis', 'bundesland', 'land']:
            db_data = get_user_data(id, 'corona_' + type_)[0]
            logger.debug(f'input data from db {db_data}, to remove data from user input: {text}')
            for orte in text:
                try:
                    db_data = db_data.replace(f'{orte},', '')
                    logger.debug(f'db_data: {db_data}')
                    
                except Exception as e:
                    logger.error(f'error {e} occured while trying to remove {orte} from {db_data}')
            post_new_user_data(id, 'corona_' + type_, db_data)
            update.message.reply_text(f'removed {orte} from db column {type_}')
        else:
            update.message.reply_text('please enter /del <corona> <landkreis/bundesland/land> <orte (zum entfernen von mehreren objekten geteilt mit einem leerzeichen auflisten)>')
    elif type_ == 'wetter':
        db_data = get_user_data(id, type_ + '_ort')[0]
        for orte in text:
            try:
                db_data = db_data.replace(f'{orte},', '')
                post_new_user_data(id, type_ + '_ort', db_data)
            except Exception as e:
                logger.error(f'error {e} occured while trying to remove {orte} from {db_data}')
    else:
        update.message.reply_text('please enter /del <corona> <landkreis/bundesland/land> <orte (zum entfernen von mehreren objekten geteilt mit einem leerzeichen auflisten)>')
        update.message.reply_text('please enter /del <wetter> <orte (zum entfernen von mehreren objekten geteilt mit einem leerzeichen auflisten)>')
    


@auth
def bot_handle_message(update, context):
    update.message.reply_text(update.message.text)


    
    
    


    

def bot_error(update, context):
    # Logs errors
    logger.debug(f'Update {str(update.message.text).lower()} caused error {context.error}')


help_commands = {
    "/help": {"description": "displays all functions", "function": bot_help_command},
    "/start": {"description": "sends the start message", "function": bot_start_command}
    }