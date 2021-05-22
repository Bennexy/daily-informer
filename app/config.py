from dotenv import find_dotenv, load_dotenv
from os import getenv as env


def load_configurations_file():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

load_configurations_file()

API_TOKEN = env("API_TOKEN")


