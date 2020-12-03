import sqlalchemy
import logging

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


def get_michelin_restaurant_names():
    engine_lite_2 = create_engine(f"sqlite:///{ROOT_DIR / 'join_data/michelin_restaurants.sqlite3'}")
    connection_2 = engine_lite_2.connect()
    one_star_query = sqlalchemy.text(
        """
        SELECT name, city FROM one_star_michelin_restaurants
        WHERE city = 'Bangkok';
        """
    )
    two_star_query = sqlalchemy.text(
        """
        SELECT name, city FROM two_stars_michelin_restaurants
        WHERE city = 'Bangkok';
        """
    )
    three_star_query = sqlalchemy.text(
        """
        SELECT name, city FROM three_stars_michelin_restaurants
        WHERE city = 'Bangkok';
        """
    )

    queries = [one_star_query, two_star_query, three_star_query]
    one_star_lst = []
    two_stars_lst = []
    three_stars_lst = []
    for i in range(len(queries)):
        result = connection_2.execute(queries[i])
        for r_michelin in result.fetchall():
            r_name = r_michelin[0]
            if i + 1 == 1:
                one_star_lst.append(r_name)
            elif i + 1 == 2:
                two_stars_lst.append(r_name)
            else:
                three_stars_lst.append(r_name)
    return one_star_lst, two_stars_lst, three_stars_lst


districts_eng = [
    'Bang Bon', 'Bang Kapi', 'Bang Khae', 'Bang Khen', 'Bang Kho Laem', 'Bang Khun Thian', 'Bang Na', 'Bang Phlat',
    'Bang Rak', 'Bang Sue', 'Bangkok Noi', 'Bangkok Yai', 'Bueng Kum', 'Chatuchak', 'Chom Thong', 'Din Daeng',
    'Don Mueang', 'Dusit', 'Huai Khwang', 'Khan Na Yao', 'Khlong Sam Wa', 'Khlong San', 'Khlong Toei', 'Lak Si',
    'Lat Krabang', 'Lat Phrao', 'Min Buri', 'Nong Chok', 'Nong Khaem', 'Pathum Wan', 'Phasi Charoen', 'Phaya Thai',
    'Phra Khanong', 'Phra Nakhon', 'Pom Prap Sattru Phai', 'Prawet', 'Rat Burana', 'Ratchathewi', 'Sai Mai',
    'Samphanthawong', 'Saphan Sung', 'Sathon', 'Suan Luang', 'Taling Chan', 'Thawi Watthana', 'Thon Buri', 'Thung Khru',
    'Wang Thonglang', 'Watthana', 'Yan Nawa'
]

districts_map = {
    'เขตบางบอน': 'Bang Bon', 'เขตบางกะปิ': 'Bang Kapi', 'เขตบางแค': 'Bang Khae',
    'เขตบางเขน': 'Bang Khen', 'เขตบางคอแหลม':'Bang Kho Laem', 'เขตบางขุนเทียน': 'Bang Khun Thian',
    'เขตบางนา': 'Bang Na', 'เขตบางพลัด': 'Bang Phlat', 'เขตบางรัก': 'Bang Rak',
    'เขตบางซื่อ': 'Bang Sue', 'เขตบางกอกน้อย': 'Bangkok Noi', 'เขตบางกอกใหญ่': 'Bangkok Yai',
    'เขตบึงกุ่ม': 'Bueng Kum', 'เขตจตุจักร': 'Chatuchak', 'เขตจอมทอง': 'Chom Thong',
    'เขตดินแดง': 'Din Daeng', 'เขตดอนเมือง': 'Don Mueang', 'เขตดุสิต': 'Dusit',
    'เขตห้วยขวาง': 'Huai Khwang', 'เขตคันนายาว': 'Khan Na Yao', 'เขตคลองสามวา': 'Khlong Sam Wa',
    'เขตคลองสาน': 'Khlong San', 'เขตคลองเตย': 'Khlong Toei', 'เขตหลักสี่': 'Lak Si',
    'เขตลาดกระบัง': 'Lat Krabang', 'เขตลาดพร้าว': 'Lat Phrao', 'เขตมีนบุรี': 'Min Buri',
    'เขตหนองจอก': 'Nong Chok', 'เขตหนองแขม': 'Nong Khaem', 'เขตปทุมวัน': 'Pathum Wan',
    'เขตภาษีเจริญ': 'Phasi Charoen', 'เขตพญาไท': 'Phaya Thai', 'เขตพระโขนง': 'Phra Khanong',
    'เขตพระนคร': 'Phra Nakhon', 'เขตป้อมปราบศัตรูพ่าย': 'Pom Prap Sattru Phai', 'เขตประเวศ': 'Prawet',
    'เขตราษฏร์บูรณะ': 'Rat Burana', 'เขตราชเทวี': 'Ratchathewi', 'เขตสายไหม': 'Sai Mai',
    'เขตสัมพันธวงศ์': 'Samphanthawong', 'เขตสะพานสูง': 'Saphan Sung', 'เขตสาทร': 'Sathon',
    'เขตสวนหลวง': 'Suan Luang', 'เขตตลิ่งชัน': 'Taling Chan', 'เขตทวีวัฒนา': 'Thawi Watthana',
    'เขตธนบุรี': 'Thon Buri', 'เขตทุ่งครุ': 'Thung Khru', 'เขตวังทองหลาง': 'Wang Thonglang',
    'เขตวัฒนา': 'Watthana', 'เขตยานนาวา': 'Yan Nawa',
}

# for converting lat, long to district
geolocator = Nominatim(user_agent='rapi-service')

one_star_restaurants, two_stars_restaurants, three_stars_restaurants = get_michelin_restaurant_names()

# after mapped with lat, long from an api
engine_lite = create_engine(f"sqlite:///{ROOT_DIR / 'join_data/restaurants_t2_3.sqlite3'}")
connection = engine_lite.connect()
sql_query = sqlalchemy.text(
    """
    SELECT tripadvisor_name, latitude, longitude, google_rating 
    FROM restaurants_tripadvisor_api
    """
)
result = connection.execute(sql_query)
restaurant_locations = result.fetchall()

# base db from tripadvisor
engine_lite = create_engine(f"sqlite:///{ROOT_DIR / 'web_scraping/data/tripadvisor/restaurants_t2.sqlite3'}")
connection = engine_lite.connect()

time = 0
for r_location in restaurant_locations:
    # print(r_location)
    # print()
    tripadvisor_name, lat, long, g_rating = r_location
    query = f"""
        SELECT name, rating, cuisines, address, opening_hour
        FROM restaurants_tripadvisor
        WHERE name = "{tripadvisor_name}";
    """
    sql_query = sqlalchemy.text(query)
    result = connection.execute(sql_query)
    restaurant = result.fetchone()

    name, rating, cuisines, address, opening_hr = restaurant

    new_cuisines = group_cuisine(cuisines)[1]
    if new_cuisines:
        commit_new_cuisines(new_cuisines)
    cuisine_ids = group_cuisine(cuisines)[0]

    open_time, close_time = split_time(opening_hr)

    district_id = 0
    location = geolocator.reverse(f"{lat}, {long}")
    locations = location.address.split(',')
    for loc_th in locations:
        if 'เขต' in loc_th:
            districts_eng = districts_map[loc_th.strip()]
            district = session_mysql.query(District).filter(District.name == districts_eng).first()
            district_id = district.id
    if district_id == 0:
        logging.warning(f"({lat}, {long}) is not in Bangkok: {restaurant}")
        continue

    michelin_star = 0
    if name in one_star_restaurants:
        print(f"1: {restaurant}")
        michelin_star = 1
    elif name in two_stars_restaurants:
        print(f"2: {restaurant}")
        michelin_star = 2
    elif name in three_stars_restaurants:
        print(f"3: {restaurant}")
        michelin_star = 3

    r_same_address_lst = session_mysql.query(Restaurant).filter(Restaurant.address == address).all()
    all_existing_cuisine_ids = [r.cuisine_id for r in r_same_address_lst]
    # print(all_existing_cuisine_ids)
    # cuisine_ids = [2, 3, 16]
    count = 0
    for i in range(len(cuisine_ids)):
        r_instance = Restaurant(
            name=name,
            latitude=lat,
            longitude=long,
            open_time=open_time,
            close_time=close_time,
            google_rating=g_rating,
            tripadvisor_rating=rating,
            address=address,
            cuisine_id=cuisine_ids[i],
            district_id=district_id,
            michelin_star=michelin_star,
        )

        if r_instance.cuisine_id in all_existing_cuisine_ids:
            print(f"pass {r_instance}")
            pass
        else:
            session_mysql.add(r_instance)
            count += 1
    session_mysql.commit()
    print(f"Committed {count} restaurants")
    # time += 1
    # if time == 1:
    #     break

# print(split_time('Closes in 39 min: '))
