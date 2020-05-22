# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup

from content_block import content_block_parse, check
from globals import db, CURRENT_TIME
from mongo import clean_mondo_coll
from variables import COUNTER, LOCAL
from secret import api_avito

if not LOCAL:
    avito_coll = db.get_collection('avito_data')
    clean_mondo_coll(avito_coll)
else:
    avito_coll = {}

url = '/irkutsk?q=%2Ctnjy'


response = requests.get(api_avito + url)
str_resp = response.content.decode("utf-8")
soup = BeautifulSoup(str_resp, 'html.parser')
mydivs = soup.find("div", class_="snippet-list")
divs = mydivs.findAll('div', class_='snippet-horizontal')

counter = 1

import multiprocessing as mp
manager = mp.Manager()
procs = []
data = manager.list()


def worker(*args):
    try:
        data.append(content_block_parse(*args))
    except Exception as e:
        print('not good')
        with open('logs.log', 'a') as f:
            f.write(str(e) + '\n')


for content_block in divs:
    try:
        if check(content_block):
            continue

        proc = mp.Process(target=worker, args=(api_avito, content_block, counter, True,))
        procs.append(proc)
        proc.start()
        time.sleep(2)
        if counter == COUNTER:
            break
        counter += 1

    except Exception as e:
        print('not good')
        with open('logs.log', 'a') as f:
            f.write(str(e) + '\n')

for proc in procs:
    proc.join()

data = list(data)

if not LOCAL:
    avito_coll.insert_many(data)
    avito_coll = db.get_collection('avito_days')
    avito_coll.insert_one({CURRENT_TIME: data})
else:
    print(data)