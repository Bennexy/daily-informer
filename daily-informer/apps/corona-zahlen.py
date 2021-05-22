#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import sys
import os
import json
sys.path.append('.')


def get_info_landkreis(url, landkreis):
    data = {}

    unparsed_page = requests.get(url).content

    parsed_page = BeautifulSoup(unparsed_page, 'html.parser')

    all_raw_data = parsed_page.find('div', class_='row row-cols-1 row-cols-md-3')
    raw_data = list(all_raw_data.find_all('b'))

    
    data['landkreis'] = landkreis

    data['einwohner'] = str(raw_data[0]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionen'] = str(raw_data[1]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionsrate'] = str(raw_data[2]).translate({ord(i): None for i in '\n <b>/'})

    data['neuinfektionen'] = str(raw_data[3]).translate({ord(i): None for i in '\n <b>/'})

    data['todesfälle'] = str(raw_data[4]).translate({ord(i): None for i in '\n <b>/'})

    data['letalitätsrate'] = str(raw_data[5]).translate({ord(i): None for i in '\n <b>/'})

    return data


def get_info_bundesland(url, bundesland):
    data = {}
    raw_data = []

    unparsed_page = requests.get(url).content

    parsed_page = BeautifulSoup(unparsed_page, 'html.parser')

    all_raw_data = parsed_page.find_all('div', class_='row row-cols-1 row-cols-md-3')
    for extracted_data in all_raw_data:
        for i in extracted_data.find_all('b'):
            raw_data.append(i)

    data['bundesland'] = bundesland

    data['einwohner'] = str(raw_data[0]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionen'] = str(raw_data[1]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionsrate'] = str(raw_data[2]).translate({ord(i): None for i in '\n <b>/'})

    data['neuinfektionen'] = str(raw_data[3]).translate({ord(i): None for i in '\n <b>/'})

    data['todesfälle'] = str(raw_data[4]).translate({ord(i): None for i in '\n <b>/'})

    data['letalitätsrate'] = str(raw_data[5]).translate({ord(i): None for i in '\n <b>/'})

    data['erstimpfungen'] = str(raw_data[6]).translate({ord(i): None for i in '\n <b>/'})

    data['impfquote (erstimpfung)'] = str(raw_data[7]).translate({ord(i): None for i in '\n <b>/'})

    data['impfquote (vollstaeding)'] = str(raw_data[8]).translate({ord(i): None for i in '\n <b>/'})

    return data

def get_info_land(url,land):
    data = {}
    raw_data = []

    unparsed_page = requests.get(url).content

    parsed_page = BeautifulSoup(unparsed_page, 'html.parser')

    all_raw_data = parsed_page.find_all('div', class_='row row-cols-1 row-cols-md-3')
    for extracted_data in all_raw_data:
        for i in extracted_data.find_all('b'):
            raw_data.append(i)

    data['land'] = land

    data['einwohner'] = str(raw_data[0]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionen'] = str(raw_data[1]).translate({ord(i): None for i in '\n <b>/'})

    data['infektionsrate'] = str(raw_data[2]).translate({ord(i): None for i in '\n <b>/'})

    data['neuinfektionen'] = str(raw_data[3]).translate({ord(i): None for i in '\n <b>/'})

    data['todesfälle'] = str(raw_data[4]).translate({ord(i): None for i in '\n <b>/'})

    data['letalitätsrate'] = str(raw_data[5]).translate({ord(i): None for i in '\n <b>/'})

    data['erstimpfungen'] = str(raw_data[6]).translate({ord(i): None for i in '\n <b>/'})

    data['impfquote (erstimpfung)'] = str(raw_data[7]).translate({ord(i): None for i in '\n <b>/'})

    data['impfquote (vollstaeding)'] = str(raw_data[8]).translate({ord(i): None for i in '\n <b>/'})

    return data

sorted_data = {}

with open(os.path.join(os.getcwd(), 'daily-informer', 'src', 'urls-corona.json')) as jsonfile:
    url_data = json.load(jsonfile)

liste = []
for landkreis in url_data['landkreise']:
    liste.append(get_info_landkreis(url_data['landkreise'][landkreis], landkreis))
sorted_data['landkreis'] = liste
liste = []
for bundesland in url_data['bundeslaender']:
    liste.append(get_info_bundesland(url_data['bundeslaender'][bundesland], bundesland))
sorted_data['bundesland'] = liste
liste = []
for land in url_data['laender']:
    liste.append(get_info_land(url_data['laender'][land], land))
sorted_data['land'] = liste
liste = []


for i in sorted_data:
    for x in sorted_data[i]:
        print(x)


print(sorted_data)

print(os.getcwd())






