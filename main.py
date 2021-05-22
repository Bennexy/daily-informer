#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests

url = 'https://www.corona-in-zahlen.de/landkreise/sk%20m%C3%BCnchen/'
#url = f'https://npgeo-corona-npgeo-de.hub.arcgis.com/'
#url = 'http://127.0.0.1:5050/'
data_list = []

unparsed_page = requests.get(url)
parsed_page = BeautifulSoup(unparsed_page.content, 'html.parser')

#cards_none = parsed_page.find('div', id='ember68')
cards = parsed_page.find('div', class_='row row-cols-1 row-cols-md-3')
new = cards.find_all('p', class_='card-title')


print(cards)
print(list(new)[3])