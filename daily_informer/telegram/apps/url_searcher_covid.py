import sys
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('.')
from daily_informer.db.db_handler import post_new_url

def url_validator(url):
    raw_data = []
    unparsed_page = requests.get(url).content

    parsed_page = BeautifulSoup(unparsed_page, 'html.parser')

    all_raw_data = parsed_page.find_all('div', class_='row row-cols-1 row-cols-md-3')
    for extracted_data in all_raw_data:
        for i in extracted_data.find_all('b'):
            raw_data.append(i)
    
    if len(raw_data) >= 3:
        return True
    else:
        return False

def upload_data_to_db(ort_type, ort, url):
    if ort_type == 'landkreis':
        ort_type_num = 1
    elif ort_type == 'bundesland':
        ort_type_num = 2
    elif ort_type == 'land':
        ort_type_num = 3
    else:
        pass
    post_new_url(ort_type_num, ort, url)

def url_finder(ort_type, ort):
    print(ort_type, ort)
    if ort_type == 'landkreis':
        url =  f"https://www.corona-in-zahlen.de/landkreise/lk%20{ort}/"
    elif ort_type == 'bundesland':
        url =  f"https://www.corona-in-zahlen.de/bundeslaender/{ort}/"
    elif ort_type == 'land':
        url =  f"https://www.corona-in-zahlen.de/weltweit/{ort}/"
    else:
        return f'Error unnown ort_type {ort_type}'
    
    if url_validator(url) == True:
        upload_data_to_db(ort_type, ort, url)
        return url
    else:
        return 'url not yet registrated'



if __name__ == '__main__':
    print(url_finder('landkreis', 'erding'))




