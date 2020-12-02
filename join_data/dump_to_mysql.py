import sqlalchemy
from sqlalchemy import create_engine
from dirs import ROOT_DIR
from rapi_site.database import db_session as session_mysql
from rapi_site.models import Restaurant, District, Cuisine
from sqlalchemy.sql import exists
from geopy.geocoders import Nominatim


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
    # messy data
    if 'Closes in' in opening_hours:
        return '', ''

    open_close = opening_hours.split(' - ')
    open_close = [t.replace(':', '.') for t in open_close]
    open_t = period_to_24hrs(open_close[0].split(' '))
    close_t = period_to_24hrs(open_close[-1].split(' '))
    return open_t, close_t


def group_cuisine(cuisines: str):
    ids = []
    news = []
    cuisine_lst = cuisines.split(',')
    for name in cuisine_lst:
        if session_mysql.query(exists().where(Cuisine.name == name)).scalar():
            cuisine = session_mysql.query(Cuisine).filter(Cuisine.name == name).first()
            ids.append(cuisine.id)
        else:
            news.append(name)
    return ids, news


def commit_new_cuisines(new_cuisines: list):
    count = 0
    for name in new_cuisines:
        c = Cuisine(name=name)
        session_mysql.add(c)
        count += 1
    session_mysql.commit()
    print(f"Committed {count} cuisine(s)")


def commit_districts(districts: list):
    count = 0
    for district_name in districts:
        d = District(name=district_name)
        session_mysql.add(d)
        count += 1
    session_mysql.commit()
    print(f"Committed {count} district(s)")


districts_eng = ['Bang Bon', 'Bang Kapi', 'Bang Khae', 'Bang Khen', 'Bang Kho Laem', 'Bang Khun Thian', 'Bang Na', 'Bang Phlat', 'Bang Rak', 'Bang Sue', 'Bangkok Noi', 'Bangkok Yai', 'Bueng Kum', 'Chatuchak', 'Chom Thong', 'Din Daeng', 'Don Mueang', 'Dusit', 'Huai Khwang', 'Khan Na Yao', 'Khlong Sam Wa', 'Khlong San', 'Khlong Toei', 'Lak Si', 'Lat Krabang', 'Lat Phrao', 'Min Buri', 'Nong Chok', 'Nong Khaem', 'Pathum Wan', 'Phasi Charoen', 'Phaya Thai', 'Phra Khanong', 'Phra Nakhon', 'Pom Prap Sattru Phai', 'Prawet', 'Rat Burana', 'Ratchathewi', 'Sai Mai', 'Samphanthawong', 'Saphan Sung', 'Sathon', 'Suan Luang', 'Taling Chan', 'Thawi Watthana', 'Thon Buri', 'Thung Khru', 'Wang Thonglang', 'Watthana', 'Yan Nawa']

districts_map = {
    'เขตบางบอน': 'Bang Bon', 'เขตบางกะปิ': 'Bang Kapi', 'เขตบางแค': 'Bang Khae',
    'เขตบางเขน': 'Bang Khen', 'เขตบางคอแหลม':'Bang Kho Laem', 'เขตบางขุนเทียน': 'Bang Khun Thian',
    'เขตบางนา': 'Bang Na', 'เขตบางพลัด': 'Bang Phlat', 'เขตบางรัก': 'Bang Rak',
    'เขตบางซื่อ': 'Bang Sue', 'เขตบางกอกน้อย': 'Bangkok Noi', 'เขตบางกอกใหญ่': 'Bangkok Yai',
    'เขตบึงกุ่ม': 'Bueng Kum', 'เขตจตุจักร': 'Chatuchak', 'เขตจอมทอง': 'Chom Thong',
    'เขตดินแดง': 'Din Daeng', 'เขตดอนเมือง': 'Don Mueang', 'เขตดุสิต': 'Dusit',
    'เขตห้วยขวาง': 'Huai Khwang', 'เขตคันนายาว': 'Khan Na Yao', 'เขตคลองสามวา': 'Khlong Sam Wa',
    'เขตคลองสาน': 'Khlong San', 'เขตคลองเตย': 'Khlong Toei', 'เขตหลักสี่': 'Lak Si',
    'เขตลาดกระบัง':'Lat Krabang', 'เขตลาดพร้าว': 'Lat Phrao', 'เขตมีนบุรี': 'Min Buri',
    'เขตหนองจอก': 'Nong Chok', 'เขตหนองแขม': 'Nong Khaem', 'เขตปทุมวัน': 'Pathum Wan',
'เขตภาษีเจริญ':'Phasi Charoen',
'เขตพญาไท':'Phaya Thai',
'เขตพระโขนง':'Phra Khanong',
'เขตพระนคร':'Phra Nakhon',
'เขตป้อมปราบศัตรูพ่าย':'Pom Prap Sattru Phai',
'เขตประเวศ':'Prawet',
'เขตราษฏร์บูรณะ':'Rat Burana',
'เขตราชเทวี':'Ratchathewi',
'เขตสายไหม':'Sai Mai',
'เขตสัมพันธวงศ์':'Samphanthawong',
'เขตสะพานสูง':'Saphan Sung',
'เขตสาทร':'Sathon',
'เขตสวนหลวง':'Suan Luang',
'เขตตลิ่งชัน':'Taling Chan',
'เขตทวีวัฒนา':'Thawi Watthana',
'เขตธนบุรี':'Thon Buri',
'เขตทุ่งครุ':'Thung Khru',
'เขตวังทองหลาง':'Wang Thonglang',
'เขตวัฒนา':'Watthana',
'เขตยานนาวา':'Yan Nawa',
}


# engine_lite = create_engine(f"sqlite:///{ROOT_DIR / 'web_scraping/data/tripadvisor/test_restaurants_t2.sqlite3'}")
# connection = engine_lite.connect()
# sql_query = sqlalchemy.text("SELECT name, rating, cuisines, address, opening_hour FROM restaurants_tripadvisor")
# result = connection.execute(sql_query)
# restaurants = result.fetchall()

# geo_locator = Nominatim()
# location = geo_locator.reverse("13.6592, 100.3991")
#
# print(location.address)


# for restaurant in restaurants:
#     name, rating, cuisines, address, opening_hr = restaurant
#
#     new_cuisines = group_cuisine(cuisines)[1]
#     if new_cuisines:
#         commit_new_cuisines(new_cuisines)
#     cuisine_ids = group_cuisine(cuisines)[0]
#
#     open_time, close_time = split_time(opening_hr)
#
#     for i in range(len(cuisine_ids)):
#         r_instance = Restaurant(
#             name=name,
#             latitude='',
#             longitude='',
#             open_time=open_time,
#             close_time=close_time,
#             google_rating='',
#             tripadvisor_rating=rating,
#             address=address,
#             cuisine_id=cuisine_ids[i],
#             district_id='',
#             michelin_star=0,
#         )



# ('Chez Shibata365', 5.0, 'French,Japanese,Thai,Japanese sweets parlour,Japanese Fusion', '27 Soi Sukhumvit 55 Hotel Nikko Thonglor The Ginza Zone Escalator At 3rd Floor, Bangkok 10110 Thailand', '10:00 AM - 9:00 PM')

# print(session_mysql.query(Restaurant))
# print(session_mysql.query(Cuisine).filter(Cuisine.name == 'Thai').first())
# print(session_mysql.query(exists().where(Cuisine.name == 'Japanese')).scalar())

# print(group_cuisine('Thai,JJJ'))
# print(split_time('Closes in 39 min: '))

# cuisines = 'French,Japanese,Thai,Japanese sweets parlour,Japanese Fusion'
# new_cuisines = group_cuisine(cuisines)[1]
# old_cuisine_ids = group_cuisine(cuisines)[0]
# print(old_cuisine_ids)
# print(new_cuisines)
# if new_cuisines:
#     commit_new_cuisines(new_cuisines)
# cuisine_ids = group_cuisine(cuisines)[0]
# print(cuisine_ids)
# print(new_cuisines)

# # works fine
# r_instance = Restaurant(
#             name='Test 2',
#             latitude='0.000000',
#             longitude='1.000000',
#             open_time='12.00',
#             close_time='24.00',
#             google_rating='2.0',
#             tripadvisor_rating='3.0',
#             address='Somewhere',
#             cuisine_id=1,
#             district_id=1
#         )
#
# session_mysql.add(r_instance)
# session_mysql.commit()
