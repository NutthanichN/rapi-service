import json
import sqlalchemy
from sqlalchemy import create_engine
from dirs import ROOT_DIR
from rapi_site.database import engine as engine_mysql


def period_to_24hrs(t_lst: list) -> str:
    # t_lst = ['12.00', 'PM']
    # 12.00 PM -> noon, 12.00 AM -> midnight
    if t_lst[0] == '12.00':
        if t_lst[1] == 'PM':
            return t_lst[0]
        else:
            return '0.00'

    if t_lst[1] == 'PM':
        hr_min = t_lst[0].split('.')
        hr = int(hr_min[0]) + 12
        return '.'.join([str(hr), hr_min[1]])
    else:
        return t_lst[0]


def split_time(opening_hours: str) -> tuple:
    # opening_hours='12:00 AM - 10:00 PM'
    open_close = opening_hours.split(' - ')
    open_close = [t.replace(':', '.') for t in open_close]
    open_time = period_to_24hrs(open_close[0].split(' '))
    close_time = period_to_24hrs(open_close[-1].split(' '))
    return open_time, close_time


# engine_lite = create_engine(f"sqlite:///{ROOT_DIR / 'web_scraping/data/tripadvisor/test_restaurants_t2.sqlite3'}")
# connection = engine_lite.connect()
# sql_query = sqlalchemy.text("SELECT * FROM restaurants_tripadvisor")
# result = connection.execute(sql_query)
#
# result_as_list = result.fetchall()
#
# for row in result_as_list:
#     print(row)
