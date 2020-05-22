import requests
from bs4 import BeautifulSoup

from globals import TODAY_DATE_STR, CURRENT_TIME, YESTERDAY_DATE_STR
from variables import ADS_CLASSES, VIP_CLASSES

avito_ads_block_class = {class_: 1 for class_ in ADS_CLASSES}
avito_vip_block_class = {class_: 1 for class_ in VIP_CLASSES}


def check(content_block):
    for content_block_class in content_block['class']:
        if avito_ads_block_class.get(content_block_class) is not None:
            print('This is ad')
            return True

        if avito_vip_block_class.get(content_block_class) is not None:
            print('VIP block')
            return True

    return False


def content_block_parse(conn, content_block, counter, proxy=False, print_data=True):
    content_block_link = content_block.find('a', class_='snippet-link')['href']

    if not proxy:
        conn.request("GET", content_block_link)
        tmp_response = conn.getresponse()
        tmp_str = tmp_response.read().decode("utf-8")
    else:
        tmp_response = requests.get(conn + content_block_link)
        tmp_str = tmp_response.content.decode("utf-8")

    content_block_link_about = BeautifulSoup(tmp_str, 'html.parser')

    content_block_data = {}
    content_block_data['hash'] = content_block_link.split('_')[-1]

    try:
        raising_time_array = content_block_link_about \
            .find('div', class_='title-info-actions-item') \
            .findAll('div')[0] \
            .text \
            .strip() \
            .split(' ')

        if raising_time_array[0] == 'сегодня':
            date = TODAY_DATE_STR
        elif raising_time_array[0] == 'вчера':
            date = YESTERDAY_DATE_STR
        else:
            date = ' '.join(raising_time_array[:2])

        content_block_data['rising_date'] = date

        content_block_data['rising_time'] = raising_time_array[-1]
    except:
        with open('logs.log', 'a') as f:
            f.write('\n' + str(content_block_link_about) + '\n')

    try:
        content_block_data['name'] = content_block_link_about \
            .find('span', class_='title-info-title-text') \
            .text \
            .strip()
    except:
        pass


    content_block_data['price'] = content_block_link_about \
        .find('span', class_='price-value-string') \
        .text \
        .strip() \
        .split('\xa0')[0]

    content_block_views = content_block_link_about \
        .find('div', class_='title-info-metadata-views') \
        .text \
        .strip()

    content_block_data['time_views'] = content_block_views.split()[1][2:-1]
    content_block_data['total_views'] = content_block_views.split()[0]
    content_block_data['current_time'] = CURRENT_TIME
    content_block_data['position'] = counter
    content_block_data['link'] = 'https://www.avito.ru' + content_block_link

    if print_data:
        print('good')

    return content_block_data
