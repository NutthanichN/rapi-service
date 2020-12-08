import requests
import json
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, Float
from join_data.api_config import API_KEY
from dirs import ROOT_DIR

db_name = 'restaurants_t2_1001_1500'
engine = create_engine(f"sqlite:///{ROOT_DIR / 'join_data' / db_name+'.sqlite3'}")
connection = engine.connect()
sql_query = sqlalchemy.text("SELECT name FROM restaurants_tripadvisor")
result = connection.execute(sql_query)

engine2 = create_engine(f"sqlite:///{ROOT_DIR / 'join_data' / db_name+'_api.sqlite3'}")
meta = MetaData()
tripadvisor = Table(
   'restaurants_tripadvisor_api', meta,
   Column('id', Integer, primary_key=True),
   Column('tripadvisor_name', String),
   Column('latitude', String),
   Column('longitude', String),
   Column('google_rating', Float))


meta.create_all(engine2)

restaurant_names = result.fetchall()

list_data = []
for row in restaurant_names:
    list_data.append(row[0])

c = 0
c_valid = 0
c_invalid = 0
json_data = []
dict_invaid = {}
for i in range(0,81):
    c = c + 1
    response = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={list_data[i]}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={API_KEY}")

    response_json = response.json()
    if response_json['status'] != "ZERO_RESULTS":
        c_valid = c_valid + 1
        name_place = response_json['candidates'][0]['name']
        google_rating = response_json['candidates'][0]['rating']
        latitude = response_json['candidates'][0]['geometry']['location']['lat']
        longitude = response_json['candidates'][0]['geometry']['location']['lng']
        print(list_data[i], latitude, longitude, google_rating)

        engine2.execute(
            tripadvisor.insert(), [{
                "tripadvisor_name": list_data[i],
                "latitude": latitude,
                "longitude": longitude,
                "google_rating": google_rating
            }]
        )
    else:
        c_invalid = c_invalid + 1

    # with open('datatrip-111.json', 'w') as outfile:
    #     json_data.append(response.json())
    #     json.dump(json_data, outfile, sort_keys=True, indent=2)

print(len(json_data))
print(c_valid)
print(c_invalid)
print(dict_invaid)
