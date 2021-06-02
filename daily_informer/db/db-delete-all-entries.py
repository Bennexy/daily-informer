import sys
import mysql.connector
from mysql.connector import cursor
sys.path.append('.')
from daily_informer.config import *
from daily_informer.logger import get_logger

mydb = mysql.connector.connect(
    host=DB,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

mycursor = mydb.cursor()
mycursor.execute("USE " + str(DB_NAME))

mycursor.execute("truncate users")

mydb.commit()


print('done')


