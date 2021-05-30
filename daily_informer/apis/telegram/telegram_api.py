from os import stat
import requests
import json
import time
import sys
import os
from requests.api import get
sys.path.append('.')
from daily_informer.apis.telegram.src.exceptions import *
from daily_informer.logger import get_logger
from daily_informer.config import API_TOKEN

logger = get_logger("telegram-api")


class TelegramAPI:
    
    def __init__(self, api_token, commands_location=None):
        self.token = api_token
        self.last_message = 0
        self.commands = None
        if commands_location != None:
            with open(commands_location, 'r') as json_file:
                self.commands = json.loads(json_file)
        path = os.path.join('daily_informer', 'apis', 'telegram', 'src', 'last_message.txt')
        if os.path.isfile(path):
            with open(path, 'r') as file:
                file_data = file.readline()
                if file_data != '':
                    self.last_message = int(file_data)
        # check that the api token is valid
        self.test_api_token(self.token)

        

    def get(self, file):
        url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        res = requests.get(url)

        if res.status_code == 200:

            data = json.loads(res.text)
            
            for message in data['result']:
                message_id = message['message']['message_id']
                if self.last_message < message_id:
                    self.last_message = message_id
                    user_id = message['message']['from']['id']
                    is_bot = message['message']['from']['is_bot']
                    name = message['message']['from']['first_name']
                    lang = message['message']['from']['language_code']
                    text = message['message']['text']
                    is_command = False
                    if 'entities' in message['message']:
                        if message['message']['entities'][0]['type'] == 'bot_command':
                            is_command = True
                    
                    # message_processing
                    if is_command == False:
                        self.message_processing(user_id=user_id, text=text)
                    else:
                        self.command_handler(user_id=user_id, text=text)

        else:
            logger.error(f'get text request returend {res.status_code}, text: {res.text}')
            raise NoConnectionError(message=f'getUpdates Request return status code: {res.status_code}')

    def send_message(self, user_id, message):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        data = {'chat_id': {user_id}, 'text': message}

        res = requests.post(url, data=data)

    def command_handler(self, user_id, text):
        pass

    def message_processing(self, user_id, text):
        self.send_message(user_id, text)


    def serve(self, intervall=1):

        try:
            while True:
                logger.debug("pulling data")
                self.get()
                time.sleep(intervall)
        except KeyboardInterrupt:
            print("shutting down")

    @staticmethod
    def process_message(data):
        pass

    @staticmethod
    def test_api_token(token):
        url = f'https://api.telegram.org/bot{token}/getMe'

        res = requests.get(url)

        res_text = json.loads(res.text)

        if res.status_code == 404 and res_text == {'ok': False, 'error_code': 404, 'description': 'Not Found'}:
            raise InvalidApiToken(f"Invalid Api Token {token} response code: 404")

api = TelegramAPI(API_TOKEN)

api.serve()
