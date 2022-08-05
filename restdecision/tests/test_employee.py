import json
from rest_framework import status
from django.test import TestCase, Client

from restdecision.models.restaurant import Restaurant
from restdecision.serializers.restaurant import RestaurantSerializer

# initialize the APIClient app
client = Client()


class CreateEmployeeTest(TestCase):
    pass
