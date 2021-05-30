import requests
import sys
import json
sys.path.append('.')

from daily_informer.config import API_TOKEN


url = f'https://api.telegram.org/bot{API_TOKEN}/Message'
#url = f'https://api.telegram.org/bot120/getMe'


res = requests.get(url)

data = json.loads(res.text)

print(res, data)

print(res.content)

"""
last_message_id = 539

for message in data['result']:
    message_id = message['message']['message_id']
    if last_message_id < message_id:
        last_message_id = message_id
        user_id = message['message']['from']['id']
        id_bot = message['message']['from']['is_bot']
        name = message['message']['from']['first_name']
        lang = message['message']['from']['language_code']
        text = message['message']['text']
        is_command = False
        if 'entities' in message['message']:
            if message['message']['entities'][0]['type'] == 'bot_command':
                is_command = True


        print(last_message_id, name, text, is_command)

print(data['result'])
"""
