from dotenv import find_dotenv, load_dotenv

load_configurations_file()

def load_configurations_file():
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

