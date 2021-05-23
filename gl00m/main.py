#!/usr/bin/python3
import json

from bs4 import BeautifulSoup
import requests

orte = ['sk%20berlin%20neukölln', 'sk%20hamburg', 'sk%20m%C3%BCnchen']
data_list = []


def parsing():
    for ort in orte:
        url = f'https://www.corona-in-zahlen.de/landkreise/{ort}/'
        unparsed_page = requests.get(url)
        parsed_page = BeautifulSoup(unparsed_page.content, 'html.parser')
        raw_location_data = parsed_page.find('div', attrs={'class': 'jumbotron jumbotron-fluid'})
        location_data = raw_location_data.find_all('h1')
        raw_data = parsed_page.find('div', attrs={'class': 'row row-cols-1 row-cols-md-3'})
        necessary_data = raw_data.find_all('b')
        create_data_list(necessary_data, location_data)
    print(data_list)
    for dictionary in data_list:
        print('\n')
        for key, value in dictionary.items():
            print(key, ':', value)


def create_data_list(necessary_data, location_data):
    collected_data = {}
    collected_data['Location'] = location_data[0].text
    collected_data['Einwohner'] = necessary_data[0].text
    collected_data['Infektionen'] = necessary_data[1].text
    collected_data['Infektionsrate'] = necessary_data[2].text
    collected_data['7-Tage-Inzidenz'] = necessary_data[3].text
    collected_data['Todesfälle'] = necessary_data[4].text
    collected_data['Letalitätsrate'] = necessary_data[5].text
    data_list.append(collected_data)


parsing()