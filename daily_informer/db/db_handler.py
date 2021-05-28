import sys
import mysql.connector
from mysql.connector import cursor
sys.path.append('.')
from daily_informer.config import *
from daily_informer.logger import get_logger

logger = get_logger('db-actions')

mydb = mysql.connector.connect(
    host=DB,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

def get_cursor():
    logger.debug('generating new db coursor')
    mycursor = mydb.cursor()
    mycursor.execute("USE " + str(DB_NAME))
    return mycursor

def get_user_data(id, type_='*'):
    mycursor = get_cursor()
    mycursor.execute(f'SELECT {type_} FROM users WHERE id ={str(id)}')
    myresult = mycursor.fetchall()
    
    if myresult == []:
        return "User not yet registrated"
    else:
        return myresult[0]



def get_user_ids():
    mycursor = get_cursor()
    mycursor.execute(f'SELECT id FROM users')
    myresult = mycursor.fetchall()
    return myresult

def get_url_data(type_, name):
    name = str(name).replace("'", '')
    mycursor = get_cursor()
    mycursor.execute(f'SELECT url FROM urls WHERE (type ={type_} AND name ="{name}")')
    myresult = mycursor.fetchall()
    
    if myresult == []:
        logger.info(f"url {name, type_} not yet registrated")
        return "url not yet registrated"

    else:
        return myresult[0]

def post_new_user(id, name=None, corona_landkreis="", corona_bundesland="", corona_land="", wetter_ort=""):
    try:
        mycoursor = get_cursor()
        mycoursor.execute(f'INSERT INTO users (id, name, corona_landkreis, corona_bundesland, corona_land, wetter_ort) VALUES ("{id}", "{name}", "{corona_landkreis}", "{corona_bundesland}", "{corona_land}", "{wetter_ort}")')
        mydb.commit()
    except Exception as e:
        logger.error(f'ERROR {e} ocured')
        print(e)

def post_new_url(type_, name, url):
    try:
        mycoursor = get_cursor()
        mycoursor.execute(f'INSERT INTO urls (type, name, url) VALUES ("{type_}", "{name}", "{url}")')
        mydb.commit()
    except Exception as e:
        logger.error(f'ERROR {e} ocured')
        print(e)

def post_new_user_data(id, type_, dataset):
    
    mycursor = get_cursor()
    mycursor.execute(f'SELECT {type_} from users WHERE id = {id}')
    myresult = mycursor.fetchall()
    myresult = myresult[0][0].split(',')
    
    data_out = myresult
    for data in dataset:
        if data not in data_out:
            logger.debug(f'{data} not in {data_out}')
            data_out.append(data)
        else:
            logger.debug(f'{data} allready in {data_out}')
    
    data_out = ','.join(data_out)

    


    logger.debug(f'UPDATE users SET {type_} = "{data_out}" WHERE id = {id}')
    mycursor.execute(f'UPDATE users SET {type_} = "{data_out}" WHERE id = {id}')
    mydb.commit()

def delete_user_data(id, type_, dataset):
    mycursor = get_cursor()
    mycursor.execute(f'SELECT {type_} from users WHERE id = {id}')
    myresult = mycursor.fetchall()
    myresult = myresult[0][0].split(',')

    data_out = myresult

    for ort in dataset:
        data_out.remove(ort)

    data_out = ','.join(data_out)

    logger.debug(f'UPDATE users SET {type_} = "{data_out}" WHERE id = {id}')
    mycursor.execute(f'UPDATE users SET {type_} = "{data_out}" WHERE id = {id}')
    mydb.commit()


















#print(get_user_data(1827750600))
#print(get_url_data(1, 'ebersberg'))


#post_new_user(1827750600, 'ben', ['erding'], ['bayern'], ['deutschland'], ['marktschwaben'])
#post_new_url(1, 'ebersberg', r"https://www.corona-in-zahlen.de/landkreise/lk%20ebersberg/")
#post_new_url(1, 'muenchen', r"https://www.corona-in-zahlen.de/landkreise/sk%20m%C3%BCnchen/")
#post_new_url(1, 'freising', r"https://www.corona-in-zahlen.de/landkreise/lk%20freising/")
#post_new_url(1, 'hamburg', r"https://www.corona-in-zahlen.de/landkreise/sk%20hamburg/")
#post_new_url(2, 'bayern', r"https://www.corona-in-zahlen.de/bundeslaender/bayern/")
#post_new_url(3, 'deutschland', r"https://www.corona-in-zahlen.de/weltweit/deutschland/")
#post_new_url(4, 'marktschwaben', r"https://www.wetter.de/deutschland/wetter-markt-schwaben-18225735/wetterbericht-aktuell.html")
#post_new_url(4, 'muenchen', r"https://www.wetter.de/deutschland/wetter-muenchen-18225562/wetterbericht-aktuell.html")

