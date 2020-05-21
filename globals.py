from mongo import connect_to_mongo

data = []
db = connect_to_mongo()

import datetime
from variables import MONTH_NAMES

TODAY_DATE_STR = str(datetime.date.today().day) + ' ' + MONTH_NAMES[(datetime.date.today().month - 1) % 12]
YESTERDAY_DATE_STR = str((datetime.date.today() - datetime.timedelta(days=1)).day) + ' ' + MONTH_NAMES[(datetime.date.today().month - 1) % 12]
CURRENT_TIME = str(datetime.datetime.now().replace(second=0, microsecond=0))
