
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

def bot_add_orte(update, context):
    global ids
    text = str(update.message.text).lower()
    id = update.message.chat.id
    
    text = text.split(" ")

    logger.debug(text)
    

    if ids == []:
        ids = reload_ids()
    if id in ids:
        if text[1].lower() == 'corona' :
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
    else:
        update.message.reply_text('please add your username to the register command-> /register <username>') 

def bot_get_daten(update, context):
    global ids
    text = str(update.message.text).lower()
    id = update.message.chat.id
    if ids == []:
        ids = reload_ids()
    if id in ids:
        text = fetch_data(id)
        for data_set in text:
            for data in data_set:
                update.message.reply_text(data)



    else:
        update.message.reply_text('please add your username to the register command-> /register <username>') 

def bot_handle_message(update, context):
    global ids
    
    id = update.message.chat.id
    text = str(update.message.text).lower()
    logger.debug(f'User ({id}) says: {text}')
    if ids == [] or id not in ids:
        ids = reload_ids()

    if id in ids:
        
        update.message.reply_text(text)
    
    else:
        update.message.reply_text("Please register via /register command - we will then save your user id and your username in a private db - use at your own risk")
    
    
    


    

def bot_error(update, context):
    # Logs errors
    logger.debug(f'Update {str(update.message.text).lower()} caused error {context.error}')


help_commands = {
    "/help": {"description": "displays all functions", "function": bot_help_command},
    "/start": {"description": "sends the start message", "function": bot_start_command}
    }