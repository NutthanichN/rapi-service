from rapi.autogen.openapi_server import models
from rapi_site.database import db_session
from flask import abort
from rapi_site.models import Restaurant, Cuisine, District


def get_restaurant():
    restaurants = db_session.query(Restaurant, Cuisine).join(Cuisine).filter(Restaurant.cuisine_id == Cuisine.id).all()

    # TODO: update .yaml (wongnai_rating -> google_rating)
    results = [
        models.Restaurant(
            id=r[0].id, name=r[0].name, location=[r[0].latitude, r[0].longitude],
            cuisine_name=r[1].name, opening_hour=f"{r[0].open_time}-{r[0].close_time}",
            google_rating=r[0].google_rating,
            tripadvisor_rating=r[0].tripadvisor_rating,
            address=r[0].address
        ) for r in restaurants
    ]
    return results


def get_restaurant_details(restaurantId):
    restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()

    print(restaurant)

    # TODO: update .yaml (wongnai_rating -> google_rating)
    result = models.Restaurant(
            id=restaurant.id, name=restaurant.name, location=[restaurant.latitude, restaurant.longitude],
            cuisine_name=restaurant.name, opening_hour=f"{restaurant.open_time}-{restaurant.close_time}",
            google_rating=restaurant.google_rating,
            tripadvisor_rating=restaurant.tripadvisor_rating,
            address=restaurant.address
        )
    return result


print(get_restaurant_details(68))


# def get_michelin_restaurant():
#     restaurants = db_session.query(Restaurant).all()
#
#     print(restaurants)
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     results = [
#         models.Restaurant(
#             id=r[0].id, name=r[0].name
#         ) for r in restaurants
#     ]
#     return results
#
#
# print(get_michelin_restaurant())


# def get_restaurant_google_rating(restaurantId):
#     restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
#
#     print(restaurant)
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     result = models.Restaurant(
#             id=restaurant.id, name=restaurant.name,
#             google_rating=restaurant.google_rating,
#         )
#     return result
#
#
# print(get_restaurant_google_rating(68))


# def get_restaurant_tripadvisor_rating(restaurantId):
#     restaurant = db_session.query(Restaurant).filter(Restaurant.id == restaurantId).one()
#
#     print(restaurant)
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     result = models.Restaurant(
#             id=restaurant.id, name=restaurant.name,
#             tripadvisor_rating=restaurant.tripadvisor_rating,
#         )
#     return result
#
#
# print(get_restaurant_tripadvisor_rating(68))


# def get_district():
#     districts = db_session.query(District).all()
#
#     print(districts)
#
#     results = [
#         models.District(
#             id=d[1].id, name=d[1].name
#         ) for d in districts
#     ]
#     return results
#
# print(get_district())


# def get_restaurant_by_district(districtId):
#     district = db_session.query(District, Restaurant).join(Restaurant).filter(Restaurant.district_id == District.Id).filter(District.id == districtId).one()
#
#     print(district)
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     result = models.District(
#         id=district.id, name=district.name,
#     )
#     return result
#
#
# print(get_restaurant_by_district(51))


# def get_cuisine():
#     cuisines = db_session.query(Cuisine).all()
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     results = [
#         models.Cuisine(
#             id=c[0].id, name=c[0].name
#         ) for c in cuisines
#     ]
#     return results


def get_specified_cuisine(cuisineId):
    cuisine = db_session.query(Cuisine).filter(Cuisine.id == cuisineId).one()

    # TODO: update .yaml (wongnai_rating -> google_rating)
    result = models.District(
        id=cuisine.id, name=cuisine.name,
    )
    return result


# def get_specified_cuisine_restaurant(cuisineId):
#     cuisine = db_session.query(Cuisine, Restaurant).join(Restaurant).filter(Restaurant.cuisine_id == Cuisine.id).filter(Cuisine.id == cuisineId).one()
#
#     # TODO: update .yaml (wongnai_rating -> google_rating)
#     result = models.District(
#         id=cuisine.id, name=cuisine.name,
#     )
#     return result