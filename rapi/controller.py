from sqlalchemy.orm.exc import NoResultFound

from rapi.autogen.openapi_server import models
from rapi_site.database import db_session
from flask import abort
from rapi_site.models import Restaurant, Cuisine, District


def get_restaurants():
    restaurants = db_session.query(Restaurant, Cuisine).join(Cuisine).filter(Restaurant.cuisine_id == Cuisine.id).all()

    results = [
        models.Restaurant(
            id=r[0].id, name=r[0].name, location=[r[0].latitude, r[0].longitude],
            cuisine_name=r[1].name, opening_hour=f"{r[0].open_time}-{r[0].close_time}",
            google_rating=r[0].google_rating,
            tripadvisor_rating=r[0].tripadvisor_rating,
            address=r[0].address, michelin_star=r[0].michelin_star
        ) for r in restaurants
    ]
    return results


def get_restaurant_details(restaurantId):
    try:
        restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
        cuisine = db_session.query(Cuisine).filter(Cuisine.id == restaurant.cuisine_id).one()

        result = models.Restaurant(
            id=restaurant.id, name=restaurant.name, location=[restaurant.latitude, restaurant.longitude],
            cuisine_name=cuisine.name, opening_hour=f"{restaurant.open_time}-{restaurant.close_time}",
            google_rating=restaurant.google_rating,
            tripadvisor_rating=restaurant.tripadvisor_rating,
            address=restaurant.address, michelin_star=restaurant.michelin_star
        )
        return result
    except NoResultFound:
        abort(404)


def get_michelin_restaurants():
    restaurants = db_session.query(Restaurant, Cuisine).join(Cuisine)\
        .filter(Restaurant.cuisine_id == Cuisine.id)\
        .filter(Restaurant.michelin_star > 0).all()

    # restaurants_distinct = []
    # restaurant_names = []
    # for r in restaurants:
    #     if r.name not in restaurant_names:
    #         restaurants_distinct.append(r)
    #         restaurant_names.append(r.name)

    results = [
        models.Restaurant(
            id=r[0].id, name=r[0].name, location=[r[0].latitude, r[0].longitude],
            cuisine_name=r[1].name, opening_hour=f"{r[0].open_time}-{r[0].close_time}",
            google_rating=r[0].google_rating,
            tripadvisor_rating=r[0].tripadvisor_rating,
            address=r[0].address, michelin_star=r[0].michelin_star
        ) for r in restaurants
    ]

    return results


def get_restaurant_google_rating(restaurantId):
    try:
        restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
        return restaurant.google_rating
    except NoResultFound:
        abort(404)


def get_restaurant_tripadvisor_rating(restaurantId):
    try:
        restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
        return restaurant.tripadvisor_rating
    except NoResultFound:
        abort(404)


def get_districts():
    districts = db_session.query(District).all()

    results = [
        models.District(id=d.id, name=d.name) for d in districts
    ]
    return results


def get_district_by_id(districtId):
    try:
        district = db_session.query(District).filter(District.id == districtId).one()
        return models.District(id=district.id, name=district.name)
    except NoResultFound:
        abort(404)


def get_restaurants_by_district(districtId):
    restaurants = db_session.query(Restaurant, Cuisine).join(Cuisine)\
        .filter(Restaurant.cuisine_id == Cuisine.id)\
        .filter(Restaurant.district_id == districtId).all()

    # restaurants_distinct = []
    # restaurant_names = []
    # for r in restaurants:
    #     if r[0].name not in restaurant_names:
    #         restaurants_distinct.append(r)
    #         restaurant_names.append(r[0].name)

    results = [
        models.Restaurant(
            id=r[0].id, name=r[0].name, location=[r[0].latitude, r[0].longitude],
            cuisine_name=r[1].name, opening_hour=f"{r[0].open_time}-{r[0].close_time}",
            google_rating=r[0].google_rating,
            tripadvisor_rating=r[0].tripadvisor_rating,
            address=r[0].address, michelin_star=r[0].michelin_star
        ) for r in restaurants
    ]
    return results


def get_cuisines():
    cuisines = db_session.query(Cuisine).all()

    results = [
        models.Cuisine(id=c.id, name=c.name) for c in cuisines
    ]
    return results


def get_cuisine_by_id(cuisineId):
    try:
        cuisine = db_session.query(Cuisine).filter(Cuisine.id == cuisineId).one()
        return models.Cuisine(id=cuisine.id, name=cuisine.name)
    except NoResultFound:
        abort(404)


def get_restaurants_by_cuisine(cuisineId):
    restaurants = db_session.query(Restaurant, Cuisine).join(Cuisine)\
        .filter(Restaurant.cuisine_id == Cuisine.id)\
        .filter(Cuisine.id == cuisineId).all()

    results = [
        models.Restaurant(
            id=r[0].id, name=r[0].name, location=[r[0].latitude, r[0].longitude],
            cuisine_name=r[1].name, opening_hour=f"{r[0].open_time}-{r[0].close_time}",
            google_rating=r[0].google_rating,
            tripadvisor_rating=r[0].tripadvisor_rating,
            address=r[0].address, michelin_star=r[0].michelin_star
        ) for r in restaurants
    ]
    return results
