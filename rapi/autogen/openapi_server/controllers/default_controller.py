import connexion
import six

from openapi_server.models.cuisine import Cuisine  # noqa: E501
from openapi_server.models.district import District  # noqa: E501
from openapi_server.models.restaurant import Restaurant  # noqa: E501
from openapi_server import util


def controller_get_cuisine():  # noqa: E501
    """Returns an array of cuisine object.

     # noqa: E501


    :rtype: Cuisine
    """
    return 'do some magic!'


def controller_get_district():  # noqa: E501
    """Returns an array of district object.

     # noqa: E501


    :rtype: District
    """
    return 'do some magic!'


def controller_get_michelin_restaurant():  # noqa: E501
    """Returns a restaurant which receives Michelin Star.

     # noqa: E501


    :rtype: Restaurant
    """
    return 'do some magic!'


def controller_get_restaurant():  # noqa: E501
    """Returns an array of restaurant object.

     # noqa: E501


    :rtype: Restaurant
    """
    return 'do some magic!'


def controller_get_restaurant_by_district(district_id):  # noqa: E501
    """Returns all restaurants with the specified district.

     # noqa: E501

    :param district_id: 
    :type district_id: int

    :rtype: District
    """
    return 'do some magic!'


def controller_get_restaurant_details(restaurant_id):  # noqa: E501
    """Returns complete details of the specified restaurant.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: Restaurant
    """
    return 'do some magic!'


def controller_get_restaurant_tripadvisor_rating(restaurant_id):  # noqa: E501
    """Returns rating of the specified restaurant from Tripadvisor.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: Restaurant
    """
    return 'do some magic!'


def controller_get_restaurant_wongnai_rating(restaurant_id):  # noqa: E501
    """Returns rating of the specified restaurant from Wongnai.

     # noqa: E501

    :param restaurant_id: 
    :type restaurant_id: int

    :rtype: Restaurant
    """
    return 'do some magic!'


def controller_get_specified_cuisine(cuisine_id):  # noqa: E501
    """Returns the specified cuisine.

     # noqa: E501

    :param cuisine_id: 
    :type cuisine_id: int

    :rtype: Cuisine
    """
    return 'do some magic!'


def controller_get_specified_cuisine_restaurant(cuisine_id):  # noqa: E501
    """Returns the array of restaurants with the specified cuisine.

     # noqa: E501

    :param cuisine_id: 
    :type cuisine_id: int

    :rtype: Cuisine
    """
    return 'do some magic!'
