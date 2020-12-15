# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from rapi.autogen.openapi_server.models.cuisine import Cuisine  # noqa: E501
from rapi.autogen.openapi_server.models.district import District  # noqa: E501
from rapi.autogen.openapi_server.models.restaurant import Restaurant  # noqa: E501
from rapi.autogen.openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_get_cuisine(self):
        """Test case for controller_get_cuisine

        Returns an array of cuisine object.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/cuisines/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_district(self):
        """Test case for controller_get_district

        Returns an array of district object.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/districts/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_michelin_restaurant(self):
        """Test case for controller_get_michelin_restaurant

        Returns a restaurant which receives Michelin Star.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/restaurants/michelin',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_restaurant(self):
        """Test case for controller_get_restaurant

        Returns an array of restaurant object.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/restaurants/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_restaurant_by_district(self):
        """Test case for controller_get_restaurant_by_district

        Returns all restaurants with the specified district.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/districts/{district_id}/restaurants'.format(district_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_restaurant_details(self):
        """Test case for controller_get_restaurant_details

        Returns complete details of the specified restaurant.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/restaurants/{restaurant_id}'.format(restaurant_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_restaurant_tripadvisor_rating(self):
        """Test case for controller_get_restaurant_tripadvisor_rating

        Returns rating of the specified restaurant from Tripadvisor.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/restaurants/rating/tripadvisor/{restaurant_id}'.format(restaurant_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_restaurant_wongnai_rating(self):
        """Test case for controller_get_restaurant_wongnai_rating

        Returns rating of the specified restaurant from Wongnai.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/restaurants/rating/wongnai/{restaurant_id}'.format(restaurant_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_specified_cuisine(self):
        """Test case for controller_get_specified_cuisine

        Returns the specified cuisine.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/cuisines/{cuisine_id}'.format(cuisine_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_specified_cuisine_restaurant(self):
        """Test case for controller_get_specified_cuisine_restaurant

        Returns the array of restaurants with the specified cuisine.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/restaurant-api/cuisines/{cuisine_id}/restaurants'.format(cuisine_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
