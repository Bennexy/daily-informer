from bs4 import BeautifulSoup
import requests
import sys
import os
import json
sys.path.append('.')


def get_weather_temp(url, ort):
    data = {}

    unparsed_page = requests.get(url).content

    parsed_page = BeautifulSoup(unparsed_page, 'html.parser')

    data['temp_max'] = parsed_page.find('div', class_='weather-daysummary__minMax__max').getText()

    data['temp_min'] = parsed_page.find('div', class_='weather-daysummary__minMax__min').getText()

    data['rain'] = parsed_page.find('span', class_='weather-rainindicator__chance').getText()

    data['date'] = parsed_page.find('div', class_='weather-daysummary__date__date').getText()

    data['weekday'] = parsed_page.find('div', class_='weather-daysummary__date__weekday').getText()



    return data
    




















with open(os.path.join(os.getcwd(), 'daily-informer', 'src', 'urls-wetter.json')) as jsonfile:
    url_data = json.load(jsonfile)


for ort in url_data:
    sorted_data = get_weather_temp(url_data[ort], ort)

print(sorted_data)