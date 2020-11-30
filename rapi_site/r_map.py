from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, Markup
)
from werkzeug.exceptions import abort

from rapi_site.database import db_session
import folium

bp = Blueprint('r_map', __name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

values2 = [
    66.67, 117.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]


colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]



labels_1 = [
    'Bananas', 'Apples',
    'Oranges', 'Strawberries', 'Lemons',
    'Watermelons', 'Coconuts'
]

values_1 = [
    10.0, 20.0, 10.0, 20.0, 20.0, 10.0, 10.0
]

labels_2 = [
    'Bananas', 'Apples',
    'Oranges', 'Strawberries', 'Lemons',
    'Watermelons', 'Coconuts'
]

values_2 = [
    20.0, 10.0, 20.0, 10.0, 10.0, 20.0, 10.0
]

labels_3 = [
    'Bananas', 'Apples',
    'Oranges', 'Strawberries', 'Lemons',
    'Watermelons', 'Coconuts'
]

values_3 = [
    30.0, 10.0, 10.0, 10.0, 20.0, 10.0, 10.0
]

@bp.route('/')
def index():
    bar_label1 = labels
    bar_value1 = values
    bar_label2 = labels_1
    bar_value2 = values_1
    bar_value3 = values2
    return render_template('r_map/index.html'
                           , title1='Cuisine', max=17000, set2=zip(values_1, labels_1, colors),
                           title2='Wongnai rating', label1=bar_label1, value1=bar_value1, value3=bar_value3,
                           title3='Tripadvisor rating', label2=bar_label2, value2=bar_value2)

@bp.route('/chart')
def chart():
    bar_label1 = labels
    bar_value1 = values
    bar_label2 = labels_1
    bar_value2 = values_1
    bar_value3 = values2
    return render_template('r_map/chart.html'
                           , title1='Cuisine', max=17000, set2=zip(values_1, labels_1, colors),
                           title2='Wongnai rating', label1=bar_label1, value1=bar_value1, value3=bar_value3,
                           title3='Tripadvisor rating', label2=bar_label2, value2=bar_value2)

@bp.route('/map')
def map():
    start_coords = (7.1898, 100.5954)
    folium_map = folium.Map(location=start_coords,
                             zoom_start=14)
    return folium_map._repr_html_()