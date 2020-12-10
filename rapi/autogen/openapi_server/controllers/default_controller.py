import connexion
import six

from rapi.autogen.openapi_server.models.cuisine import Cuisine  # noqa: E501
from rapi.autogen.openapi_server.models.district import District  # noqa: E501
from rapi.autogen.openapi_server.models.restaurant import Restaurant  # noqa: E501
from rapi.autogen.openapi_server import util


def rapi_controller_get_cuisine_by_id(cuisine_id):  # noqa: E501
    """Returns the specified cuisine.

     # noqa: E501

    :param cuisine_id: 
    :type cuisine_id: int

    :rtype: Cuisine
    """
    return 'do some magic!'


def rapi_controller_get_cuisines():  # noqa: E501
    """Returns an array of cuisine object.

     # noqa: E501


    :rtype: List[Cuisine]
    """
    return 'do some magic!'


def rapi_controller_get_district_by_id(district_id):  # noqa: E501
    """Returns a district object with the specified ID

     # noqa: E501

    :param district_id: 
    :type district_id: int

    :rtype: District
    """
    return 'do some magic!'


def rapi_controller_get_districts():  # noqa: E501
    """Returns an array of district object.

     # noqa: E501


    :rtype: List[District]
    """
    return 'do some magic!'


def rapi_controller_get_michelin_restaurants():  # noqa: E501
    """Returns a restaurant which receives Michelin Star.

     # noqa: E501


    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def rapi_controller_get_restaurant_details(restaurant_id):  # noqa: E501
    """Returns complete details of the specified restaurant.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: Restaurant
    """
    return 'do some magic!'


def rapi_controller_get_restaurant_google_rating(restaurant_id):  # noqa: E501
    """Returns rating of the specified restaurant from Google.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: int
    """
    return 'do some magic!'


def rapi_controller_get_restaurant_tripadvisor_rating(restaurant_id):  # noqa: E501
    """Returns rating of the specified restaurant from Tripadvisor.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: int
    """
    return 'do some magic!'


def rapi_controller_get_restaurants():  # noqa: E501
    """Returns an array of restaurant object.

     # noqa: E501


    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def rapi_controller_get_restaurants_by_cuisine(cuisine_id):  # noqa: E501
    """Returns the array of restaurants with the specified cuisine.

     # noqa: E501

    :param cuisine_id: 
    :type cuisine_id: int

    :rtype: List[Restaurant]
    """
    return 'do some magic!'


def rapi_controller_get_restaurants_by_district(district_id):  # noqa: E501
    """Returns all restaurants with the specified district.

     # noqa: E501

    :param district_id: 
    :type district_id: int

    :rtype: List[Restaurant]
    """
    return 'do some magic!'
