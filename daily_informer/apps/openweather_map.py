import requests
import sys
sys.path.append('.')
from daily_informer.config import API_KEY_OPEN_WEATHER

city = "NewYork"

response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_OPEN_WEATHER}")

print(response.text)