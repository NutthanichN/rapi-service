from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, Markup
)
from werkzeug.exceptions import abort

from rapi_site.database import db_session
from rapi_site.models import Restaurant, District, Cuisine
import folium
from dirs import ROOT_DIR
from folium.plugins import MarkerCluster
import tkinter as tk
import random
import matplotlib.colors as mcolors
import re
import operator
import sqlalchemy

root = tk.Tk()

bp = Blueprint('r_map', __name__)
OPERATORS = {">": operator.gt, "<": operator.lt, ">=": operator.ge, "<=": operator.le, "==": operator.eq}


def generate_map(restaurants: list, locations: list, cuisine_names: dict):
    if locations:
        map2 = folium.Map(location=locations[0], zoom_start=20)
    else:
        map2 = folium.Map(location=[13.728, 100.561], zoom_start=20)

    marker_cluster = MarkerCluster().add_to(map2)

    for point in range(len(restaurants)):
        cuisines = ','.join(set(cuisine_names[restaurants[point].name]))

        l1 = f'''<p>
                    Name: {restaurants[point].name}</br>
                    Adress: {restaurants[point].address}</br>
                    Tripadvisor rating: {restaurants[point].tripadvisor_rating}</br>
                    Google rating: {restaurants[point].google_rating}</br>
                    Michelin Star: {restaurants[point].michelin_star}</br>
                    Cuisines: {cuisines}</br>
                    Open hours: {restaurants[point].open_time} - {restaurants[point].close_time}</p>
        '''
        folium.Marker(locations[point], popup=folium.Popup(l1,
                                                      max_width=400, min_width=300),
                      icon=folium.Icon(color='darkblue', icon_color='white', angle=0, prefix='fa'
                                       )).add_to(
            marker_cluster)
    map2.save(str(ROOT_DIR / 'rapi_site/templates/map.html'))


def convert_to_cuisine_name(restaurant_cuisines: dict) -> dict:
    r_cuisine_names = {}
    for r_name, c_id_lst in restaurant_cuisines.items():
        cuisine_names = []
        for c_id in c_id_lst:
            cuisine = db_session.query(Cuisine).filter(Cuisine.id == c_id).one()
            cuisine_names.append(cuisine.name)
        r_cuisine_names[r_name] = cuisine_names
    return r_cuisine_names

def count_michelin_stars(restaurant_lat) -> dict:
    michelin_stars_count = {0: 0, 1: 0, 2: 0, 3: 0}

    for r in restaurant_lat:
        if r.michelin_star == 0:
            michelin_stars_count[0] += 1
        elif r.michelin_star == 1:
            michelin_stars_count[1] += 1
        elif r.michelin_star == 2:
            michelin_stars_count[2] += 1
        elif r.michelin_star == 3:
            michelin_stars_count[3] += 1
    return michelin_stars_count



def count_ratings(restaurant_lat, mode) -> dict:
    rating_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for r in restaurant_lat:
        r_rating = -1
        if mode == "trip":
            r_rating = r.tripadvisor_rating
        elif mode == "google":
            r_rating = r.google_rating

        if r_rating == -1:
            continue
        elif 0 <= r_rating < 1:
            rating_count[0] += 1
        elif 1 <= r_rating < 2:
            rating_count[1] += 1
        elif 2 <= r_rating < 3:
            rating_count[2] += 1
        elif 3 <= r_rating < 4:
            rating_count[3] += 1
        elif 4 <= r_rating < 5:
            rating_count[4] += 1
        elif r_rating == 5:
            rating_count[5] += 1
    return rating_count


def split_operator_and_rating(rating_str):
    result = re.match(r"(?P<operator>>=|<=|>|<)(?P<rating>.*)", rating_str)
    if result is not None:
        return result["operator"], result["rating"]
    return "==", rating_str


@bp.route('/', methods=('GET', 'POST'))
def index():
    check_post = False
    check_t_graph = False
    check_g_graph = False
    check_m_graph = False
    color_cui = []
    label_cuisines = []
    cuisine_value = []

    if request.method == 'GET':
        generate_map([], [], {})

    elif request.method == 'POST':
        check_post = True
        # get vaule from html
        district_h = request.form.get("district-name")
        cuisine_h = request.form.get("cuisine")
        trip_ad_h = request.form.get("trip-ad")
        google_h = request.form.get("google")
        michelin = request.form.get("michelin")
        open_h = request.form.get("open")



        restaurant_result_lst = []
        restaurant_distinct_lst = []
        restaurants = db_session.query(Restaurant).all()

        value_cuisine = set()

        i = 0

        # check if user select district
        if district_h != "bangkok":
            district = db_session.query(District).filter(District.name == district_h).one()
            for r in restaurants:
                if r.district_id == district.id:
                    restaurant_result_lst.append(r)

            # cuisine pie chart
            cuisine_id = db_session.query(Restaurant.cuisine_id).join(District).join(Cuisine).filter(
                District.id == Restaurant.district_id). \
                filter(District.name == district_h).all()
            for c in cuisine_id:
                value_cuisine.add(c[0])

            for value in value_cuisine:
                i = i + 1
                cuisine_name = db_session.query(Cuisine.name).join(Restaurant).filter(
                    Restaurant.cuisine_id == value).first()
                cuisine_count = db_session.query(Restaurant.latitude).join(District).filter(
                    District.id == Restaurant.district_id). \
                    filter(Restaurant.latitude == Restaurant.latitude). \
                    filter(Restaurant.cuisine_id == value). \
                    filter(District.name == district_h).count()
                cuisine_value.append(int(cuisine_count))
                label_cuisines.append(cuisine_name[0])
                colors_cusine = random.choices(list(mcolors.CSS4_COLORS.values()))
                color_cui.append(colors_cusine[0])

        else:
            restaurant_result_lst = list(restaurants)

            # cuisine pie chart
            cuisine_id = db_session.query(Restaurant.cuisine_id)
            for c in cuisine_id:
                value_cuisine.add(c[0])

            for value in value_cuisine:
                i = i + 1
                cuisine_name = db_session.query(Cuisine.name).join(Restaurant).filter(
                    Restaurant.cuisine_id == value).first()
                cuisine_count = db_session.query(Restaurant.latitude).filter(
                    District.id == Restaurant.district_id). \
                    filter(Restaurant.latitude == Restaurant.latitude). \
                    filter(Restaurant.cuisine_id == value).count()

                cuisine_value.append(int(cuisine_count))
                label_cuisines.append(cuisine_name[0])
                colors_cusine = random.choices(list(mcolors.CSS4_COLORS.values()))
                color_cui.append(colors_cusine[0])

        restaurant_check = []
        restaurant_distinct = []
        for r in restaurant_result_lst:
            if r.name not in restaurant_check:
                restaurant_distinct.append(r)
                restaurant_check.append(r.name)

        restaurant_check.clear()
        # bar chart of tripdavisor and google rating and michenlin stars
        trip_rating_count = count_ratings(restaurant_distinct, "trip")
        google_rating_count = count_ratings(restaurant_distinct, "google")
        michelin_stars_count = count_michelin_stars(restaurant_distinct)

        trip_rating_count_lst = []
        for key, value in trip_rating_count.items():
            trip_rating_count_lst.append(value)
        google_rating_count_lst = []
        for key, value in google_rating_count.items():
            google_rating_count_lst.append(value)
        michelin_stars_count_lst = []
        for key, value in michelin_stars_count.items():
            michelin_stars_count_lst.append(value)

        if cuisine_h != "":
            restaurants_filtered_cuisine = []
            r_names_check = []
            try:
                cuisine = db_session.query(Cuisine).filter(Cuisine.name == cuisine_h).one()
                for r in restaurant_result_lst:
                    if r.cuisine_id == cuisine.id:
                        restaurants_filtered_cuisine.append(r)
                        r_names_check.append(r.name)
                    elif r.name in r_names_check:
                        restaurants_filtered_cuisine.append(r)
                restaurant_result_lst = restaurants_filtered_cuisine.copy()
            except sqlalchemy.orm.exc.NoResultFound:
                restaurant_result_lst = []

        if trip_ad_h != "":
            t_operator, t_rating = split_operator_and_rating(trip_ad_h)
            check_t_graph = True
            restaurants_filtered_t_rating = []

            for r in restaurant_result_lst:
                try:
                    t_condition = OPERATORS[t_operator](r.tripadvisor_rating, float(t_rating))
                    if -1 < r.tripadvisor_rating <= 5:
                        if t_condition:
                            restaurants_filtered_t_rating.append(r)
                except ValueError:
                    pass
            restaurant_result_lst = restaurants_filtered_t_rating.copy()

        if google_h != "":
            g_operator, g_rating = split_operator_and_rating(google_h)
            check_g_graph = True
            restaurants_filtered_g_rating = []
            for r in restaurant_result_lst:
                try:
                    g_condition = OPERATORS[g_operator](r.google_rating, float(g_rating))
                    if g_condition:
                        restaurants_filtered_g_rating.append(r)
                except ValueError:
                    pass
            restaurant_result_lst = restaurants_filtered_g_rating.copy()

        if michelin != "":
            m_operator, m_star = split_operator_and_rating(michelin)
            check_m_graph = True
            restaurants_filtered_michelin = []
            for r in restaurant_result_lst:
                try:
                    m_condition = OPERATORS[m_operator](r.michelin_star, float(m_star))
                    if m_condition:
                        restaurants_filtered_michelin.append(r)
                except ValueError:
                    pass
            restaurant_result_lst = restaurants_filtered_michelin.copy()

        if open_h != "":
            restaurants_filtered_open_hrs = []
            for r in restaurant_result_lst:
                try:
                    if r.open_time == "" and r.close_time == "":
                        continue
                    elif float(r.open_time) <= float(open_h) < float(r.close_time):
                        restaurants_filtered_open_hrs.append(r)
                except ValueError:
                    pass
            restaurant_result_lst = restaurants_filtered_open_hrs.copy()

        restaurant_names_check = []
        restaurant_cuisines = {}
        for r in restaurant_result_lst:
            # restaurant = {'': []}
            if r.name not in restaurant_names_check:
                restaurant_distinct_lst.append(r)
                restaurant_names_check.append(r.name)
                # restaurant_cuisines[str(r.address)] = [r.cuisine_id]
                restaurant_cuisines[r.name] = [r.cuisine_id]
            else:
                for r_name in restaurant_names_check:
                    if r_name == r.name:
                        # restaurant_cuisines[str(r.address)].append(r.cuisine_id)
                        restaurant_cuisines[r.name].append(r.cuisine_id)
        restaurant_names_check.clear()

        locations = []
        for r in restaurant_distinct_lst:
            locations.append([r.latitude, r.longitude])

        restaurant_cuisine_names = convert_to_cuisine_name(restaurant_cuisines)
        generate_map(restaurant_distinct_lst, locations, restaurant_cuisine_names)


    districts = db_session.query(District.name)
    district_names = [d[0] for d in districts]

    if check_post:
        number = len(restaurant_distinct_lst)
        if check_m_graph:
            if check_t_graph and check_g_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title1='Tripadvisor rating', value1_compare=trip_rating_count_lst,
                                       value3=michelin_stars_count_lst,
                                       title2='Google rating', value2_compare=google_rating_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
            elif check_t_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title1='Tripadvisor rating', value1=trip_rating_count_lst,
                                       value3=michelin_stars_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
            elif check_g_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title2='Google rating', value2=google_rating_count_lst,
                                       value3=michelin_stars_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
            else:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)

        else:
            if check_t_graph and check_g_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title1='Tripadvisor rating', value1_compare=trip_rating_count_lst,
                                       title2='Google rating', value2_compare=google_rating_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
            elif check_t_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title1='Tripadvisor rating', value1=trip_rating_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
            elif check_g_graph:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       title2='Google rating', value2=google_rating_count_lst,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)

            else:
                return render_template('r_map/index.html', dis_select=district_h, dis_all=district_names, max=17000,
                                       pre_district=district_h, pre_cuisine=cuisine_h, pre_trip_ad=trip_ad_h,
                                       pre_google=google_h, pre_michelin=michelin, pre_open=open_h,
                                       value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui,
                                       number_restautant=number)
    else:
        return render_template('r_map/index.html', dis_all=district_names, max=17000,
                               pre_district="", pre_cuisine="", pre_trip_ad="", pre_google="",
                               pre_michelin="", pre_open="",
                               value_cui=cuisine_value, label_cui=label_cuisines, color=color_cui
                               )