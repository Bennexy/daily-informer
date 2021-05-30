import sys
import os
sys.path.append('.')
path = os.path.join('daily_informer', 'apis', 'telegram', 'src', 'last_message.txt')
if os.path.isfile(path):
    with open(path, 'r') as file:
        last_message = int(file.readline())
    print(last_message)