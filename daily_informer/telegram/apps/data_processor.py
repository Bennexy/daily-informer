import sys
sys.path.append('.')
from daily_informer.db.db_handler import get_url_data
from daily_informer.logger import get_logger
from daily_informer.apps.corona_zahlen import *
from daily_informer.apps.openweather_map import get_wetter_data
from daily_informer.telegram.apps.url_searcher_covid import url_finder


logger = get_logger('url-data-processing')


def sort_data(landkreis, bundesland, land, wetter):
    landkreis = landkreis.split(',')
    bundesland = bundesland.split(',')
    land = land.split(',')
    wetter = wetter.split(',')

    try:
        landkreis.remove('None')
    except ValueError:
        pass
    try:
        bundesland.remove('None')
    except ValueError:
        pass
    try:
        land.remove('None')
    except ValueError:
        pass
    try:
        wetter.remove('None')
    except ValueError:
        pass

    urls = {}

    logger.debug(f'raw data from database {landkreis, bundesland, land, wetter}')

    if landkreis is None and bundesland is None and land is None and wetter is None:
        logger.info(f'No data for this user in db')
        return 'No data for this user in db'

    if landkreis is not None:
        liste = {}
        for ort in landkreis:
            if ort != '':
                data = get_url_data(1, ort)
                logger.debug(f'ort: {ort}  url data found in db: {data}')
                if data != 'url not yet registrated':
                    liste[ort] = data[0]
                else:
                    liste[ort] = data
        urls['landkreis'] = liste
    if bundesland is not None:
        liste = {}
        for ort in bundesland:
            if ort != '':
                data = get_url_data(2, ort)
                logger.debug(f'ort: {ort}  url data found in db: {data}')
                if data != 'url not yet registrated':
                    liste[ort] = data[0]
                else:
                    liste[ort] = data
        urls['bundesland'] = liste
    if land is not None:
        liste = {}
        for ort in land:
            if ort != '':
                data = get_url_data(3, ort)
                logger.debug(f'ort: {ort}  url data found in db: {data}')
                if data != 'url not yet registrated':
                    liste[ort] =  data[0]
                else:
                    liste[ort] = data
        urls['land'] = liste
    if wetter is not None:
        liste = {}
        for ort in wetter:
            if ort != '':
                liste[ort] = data
        urls['wetter'] = liste

    logger.debug(f'data found {urls}')

    return urls

def get_infos_from_webpages(urls):
    data = {}
    data['landkreis'] = []
    data['bundesland'] = []
    data['land'] = []
    data['wetter'] = []
    for key_base, value_base in urls.items():
        for ort, url in value_base.items():
            if key_base != 'wetter' and url == 'url not yet registrated':
                url = url_finder(key_base, ort)


            logger.debug(f' {key_base} {ort} {url}')
            if key_base == "landkreis" and url != 'url not yet registrated':
                data['landkreis'].append(get_info_landkreis(url, ort))
            if key_base == "bundesland" and url != 'url not yet registrated':
                data['bundesland'].append(get_info_bundesland(url, ort))
            if key_base == "land" and url != 'url not yet registrated':
                data['land'].append(get_info_land(url, ort))
            if key_base == "wetter" and url != 'url not yet registrated':
                data['wetter'].append(get_wetter_data(ort))
    
    logger.debug(f'data {data}')

    return data

def prepare_string(data):
    output = [[],[],[],[]]
    for key_base, value_list in data.items():
        if key_base == 'landkreis':
            for item_dict in value_list:
                output[0].append(f"""Landkreis: {item_dict['landkreis']} Einwohnerzahl: {item_dict['einwohner']} Infektionen: {item_dict['infektionen']} Infektionsrate: {item_dict['infektionsrate']} Neuinfektionen: {item_dict['neuinfektionen']} Todesf??lle: {item_dict['todesf??lle']} Letalit??tsrate: {item_dict['letalit??tsrate']}""")
        if key_base == 'bundesland':
            for item_dict in value_list:
                output[1].append(f"""Bundesland: {item_dict['bundesland']} Einwohnerzahl: {item_dict['einwohner']} Infektionen: {item_dict['infektionen']} Infektionsrate: {item_dict['infektionsrate']} Neuinfektionen: {item_dict['neuinfektionen']} Todesf??lle: {item_dict['todesf??lle']} Letalit??tsrate: {item_dict['letalit??tsrate']} Erstimpfungen: {item_dict['erstimpfungen']} Impfquote (erstimpfung) {item_dict['impfquote (erstimpfung)']} Impfquote (vollstaeding) {item_dict['impfquote (vollstaeding)']}""")
        if key_base == 'land':
            for item_dict in value_list:
                output[2].append(f""" Land: {item_dict['land']} Einwohnerzahl: {item_dict['einwohner']} Infektionen: {item_dict['infektionen']} Infektionsrate: {item_dict['infektionsrate']} Neuinfektionen: {item_dict['neuinfektionen']} Todesf??lle: {item_dict['todesf??lle']} Letalit??tsrate: {item_dict['letalit??tsrate']} Erstimpfungen: {item_dict['erstimpfungen']} Impfquote (erstimpfung) {item_dict['impfquote (erstimpfung)']} Impfquote (vollstaeding) {item_dict['impfquote (vollstaeding)']}""")
        if key_base == 'wetter':
            for item_dict in value_list:
                for ort, data in item_dict.items():
                    #logger.info(f""" Ort: {ort} Temp max {data['temp_max']} Temp min {data['temp_min']} Luftfeuchtigkeit {data['humidity']} Wind: {data['wind']}""")
                    output[3].append(f""" Ort: {ort} Temp max {data['temp_max']} Temp min {data['temp_min']} Luftfeuchtigkeit {data['humidity']} Wind: {data['wind']}""")

    return output

