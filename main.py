# -*- coding: utf-8 -*-
import http.client

from bs4 import BeautifulSoup

from content_block import content_block_parse, check
from globals import db, data, CURRENT_TIME
from mongo import clean_mondo_coll
from variables import COUNTER

avito_coll = db.get_collection('avito_data')
clean_mondo_coll(avito_coll)

conn = http.client.HTTPSConnection("www.avito.ru")
conn.request("GET", "/irkutsk?q=%2Ctnjy")
response = conn.getresponse()
str_resp = response.read().decode("utf-8")
soup = BeautifulSoup(str_resp, 'html.parser')
mydivs = soup.find("div", class_="snippet-list")

counter = 1
for content_block in mydivs.findAll('div', class_='snippet-horizontal'):
    try:
        if check(content_block):
            continue

        content_block_parse(conn, content_block, avito_coll, counter)

        if counter == COUNTER:
            break
        counter += 1

    except Exception as e:
        print('not good')
        with open('logs.log', 'a') as f:
            f.write(str(e) + '\n')

avito_coll = db.get_collection('avito_days')
avito_coll.insert_one({CURRENT_TIME: data})
