from dotenv import find_dotenv, load_dotenv
from os import getenv as env


def load_configurations_file():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

load_configurations_file()

API_TOKEN = env("API_TOKEN")
API_KEY_OPEN_WEATHER = env("API_KEY_OPEN_WEATHER")
DB = env('DB')
DB_PORT = env('DB_PORT')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_NAME = env('DB_NAME')

