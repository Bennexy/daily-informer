import requests
import sys
import json
sys.path.append('.')
from daily_informer.config import API_KEY_OPEN_WEATHER
from daily_informer.logger import get_logger

logger = get_logger("get-wetter-data")

#orte = ["MarktSchwaben", "münchen"]
#for ort in orte:
#    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={ort}&appid={API_KEY_OPEN_WEATHER}")

#    print(response.text)



def get_wetter_data(ort):
    data = {}
    ort = ort.replace("-", " ")
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={ort}&appid={API_KEY_OPEN_WEATHER}")

    if res.status_code != 200:
        logger.error(f"invalid ort value {ort}, respons = {res.status_code}")
        data[ort] =  {'error': res.status_code, 'message' : f"Ort {ort} not found"}
        pass
    else:
        logger.info(f"found weather data")

        result = json.loads(res.text)
        data[ort] = {
                        'temp_max': round(result['main']['temp_max'] - 273.15, 3),
                        'temp_min': round(result['main']['temp_min'] - 273.15, 3),
                        'humidity': str(result['main']['humidity']) + "%",
                        'wind': round(result['wind']['speed'], 3)
                    }

    logger.debug(f'data got from weather api {data}')

    return data






if __name__ == '__main__':
    print(get_wetter_data(["münchen", "markt-schwaben"]))


