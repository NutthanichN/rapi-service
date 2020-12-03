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

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


bp = Blueprint('r_map', __name__)


def generate_map(list, list1, list2, list3,list4,list5):
    map2 = folium.Map(width=1200,height=600, location=[13.728, 100.561], zoom_start=20)

    marker_cluster = MarkerCluster().add_to(map2)
    print("pp")


    for point in range(0, len(list)):
        l1 = f'''Name: {list1[point]} \
        Adress: {list2[point]}  \
        Tripadvisor: {list3[point]}  \
        Michelin Star: {list4[point]}  \
        Cuisine: {list5[point]}'''
        folium.Marker(list[point], popup=folium.Popup(l1,
                                       max_width=400,min_width=300),
                      icon=folium.Icon(color='darkblue', icon_color='white', angle=0, prefix='fa'
                                       )).add_to(
            marker_cluster)
    map2.save(str(ROOT_DIR / 'rapi_site/templates/map_test.html'))


@bp.route('/', methods=('GET', 'POST'))
def index():
    print("5555555555", request.method)
    if request.method == 'POST':
        print("success")
        district_h = request.form["nm"]

        query_lat = db_session.query(Restaurant.latitude).join(District).filter(District.id == Restaurant.district_id) .\
            filter(District.name == district_h).all()
        query_long = db_session.query(Restaurant.longitude).join(District).filter(District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()
        query_name = db_session.query(Restaurant.name).join(District).filter(
            District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()
        query_trip_rating = db_session.query(Restaurant.tripadvisor_rating).join(District).filter(
            District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()
        query_adress = db_session.query(Restaurant.address).join(District).filter(
            District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()
        query_michelin = db_session.query(Restaurant.michelin_star).join(District).filter(
            District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()
        query_cuisine = db_session.query(Cuisine.name).join(Restaurant).join(District).filter(
            District.id == Restaurant.district_id). \
            filter(District.name == district_h).all()

        count = db_session.query(Restaurant.latitude).join(District).filter(District.id ==Restaurant.district_id) .\
            filter(District.name == district_h).count()


        list_detail = []
        list_detail1 = []
        list_detail2 = []
        list_detail3 = []
        list_detail4 = []
        list_detail5 = []
        for i in range(count):
            if query_lat[i-1][0] == query_lat[i][0] and query_long[i-1][0] == query_long[i][0]:
                if i == 0:
                    list_detail.append([float(query_lat[i][0]), float(query_long[i][0])])
            else:
                list_detail.append([float(query_lat[i][0]), float(query_long[i][0])])

        print(list_detail)

        for i in range(count):
            list_detail1.append(query_name[i][0])
        print(list_detail1)

        for i in range(count):
            list_detail2.append(query_adress[i][0])
        print(list_detail2)

        for i in range(count):
            list_detail3.append(float(query_trip_rating[i][0]))
        print(list_detail3)

        for i in range(count):
            list_detail4.append(float(query_michelin[i][0]))
        print(list_detail4)

        for i in range(count):
            list_detail5.append(query_cuisine[i][0])
        print(list_detail5)

        generate_map(list_detail,list_detail1,list_detail2,list_detail3,list_detail4,list_detail5)

    district = db_session.query(District.name)
    return render_template('r_map/index.html', dis_all=district)



@bp.route('/chart')
def chart():
    bar_label1 = labels
    bar_value1 = values
    bar_label2 = labels_1
    bar_value2 = values_1
    bar_value3 = values2
    if request.method == 'POST':
        print("66666666666666")
    return render_template('r_map/chart.html'
                           , title1='Cuisine', max=17000, set2=zip(values_1, labels_1, colors),
                           title2='Wongnai rating', label1=bar_label1, value1=bar_value1, value3=bar_value3,
                           title3='Tripadvisor rating', label2=bar_label2, value2=bar_value2)
