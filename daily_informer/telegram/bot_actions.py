import sys
from mysql.connector.errors import IntegrityError
sys.path.append('.')

from daily_informer.db.db_handler import *
from daily_informer.telegram.apps.data_processor import *
from daily_informer.logger import get_logger

logger = get_logger('bot-actions')


def reload_ids():
    ids_raw = get_user_ids()
    ids = []
    for id in ids_raw:
        ids.append(id[0])
    return ids

def add_user(id, username):
    try:
        post_new_user(id, username)
        return True
    except Exception as e:
        logger.error(e)
        print(e)
        return False

def add_to_db(id, type_, data):
    logger.debug(f'data to add to the database {data}')
    data = preprocess_data(data)
    
    if 'landkreis' == type_:
        post_new_user_data(id, 'corona_landkreis' ,data)
    elif 'land' == type_:
        post_new_user_data(id, 'corona_land', data)
    elif 'bundesland' == type_:
        post_new_user_data(id, 'corona_bundesland', data)
    elif 'wetter' == type_:
        post_new_user_data(id ,'wetter_ort', data)
    else:
        return False

def delete_from_db(id, type_, data):
    logger.debug(f'data to add to the database {data}')
    data = preprocess_data(data)
    
    if 'landkreis' == type_:
        delete_user_data(id, 'corona_landkreis' ,data)
    elif 'land' == type_:
        delete_user_data(id, 'corona_land', data)
    elif 'bundesland' == type_:
        delete_user_data(id, 'corona_bundesland', data)
    elif 'wetter' == type_:
        delete_user_data(id ,'wetter_ort', data)
    else:
        return False

def fetch_data(id):

    id ,name, landkreis, bundesland, land, wetter = get_user_data(id)

    urls = sort_data(landkreis, bundesland, land, wetter)

    raw_infos = get_infos_from_webpages(urls)
    
    return prepare_string(raw_infos)

def preprocess_data(data):
    output = []
    for ort in data:
        output.append(ort.replace("-", " "))
    
    return output
    



if __name__ == '__main__':
    #print(reload_ids())
    #1827750600
    #add_to_db(1827750600, ['land', 'test', 'bayern'])
    fetch_data(1827750600)
