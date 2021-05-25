import sys
from mysql.connector.errors import IntegrityError
sys.path.append('.')

from daily_informer.db.db_handler import *
from daily_informer.telegram.apps.get_data import *

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

def add_to_db(id, data):
    logger.debug(f'data to add to the database {data}')
    data_null = data.pop(0)
    
    if 'landkreis' == data_null:
        post_new_user_data(id, 'corona_landkreis',data)
    elif 'land' == data_null:
        post_new_user_data(id, 'corona_land', data)
    elif 'bundesland' == data_null:
        post_new_user_data(id, 'corona_bundesland', data)
    elif 'wetter' == data_null:
        post_new_user_data(id ,'wetter_ort', data)
    else:
        return False

def fetch_data(id):

    id ,name, landkreis, bundesland, land, wetter = get_user_data(id)

    urls = sort_data(landkreis, bundesland, land, wetter)

    raw_infos = get_infos_from_webpages(urls)
    
    print(raw_infos)
    

if __name__ == '__main__':
    #print(reload_ids())
    #1827750600
    #add_to_db(1827750600, ['land', 'test', 'bayern'])
    fetch_data(1827750600)
