import os
import sys
#from multiprocessing import Process
sys.path.append('.')
from daily_informer.logger import get_logger
from daily_informer.telegram import telegram_bot

logger = get_logger('main_process handler')

#processes = [Process(target=telegram_bot)]#, args=(Unauthorized,))]


if __name__ == '__main__':

    telegram_bot()



