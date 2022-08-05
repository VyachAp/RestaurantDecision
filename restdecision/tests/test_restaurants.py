import json
from rest_framework import status
from django.test import TestCase, Client

from restdecision.models.restaurant import Restaurant
from restdecision.serializers.restaurant import RestaurantSerializer

# initialize the APIClient app
client = Client()


class GetAllRestaurantsTest(TestCase):
    """Test module for GET all restaurants API"""

    def setUp(self):
        Restaurant.objects.create(name="Frank")
        Restaurant.objects.create(name="Gwidon")
        Restaurant.objects.create(name="Red Fox")

    def test_get_all_restaurants(self):
        response = client.get("/api/restaurants/")
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateRestaurantTest(TestCase):
    """Test module for inserting a new restaurant"""

    def setUp(self):
        self.valid_payload = {
            "name": "Cool Restaurant",
        }
        self.invalid_payload = {
            "brand": "Some brand",
        }

    def test_create_valid_restaurant(self):
        response = client.post(
            "/api/restaurants/",
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_restaurant(self):
        response = client.post(
            "/api/restaurants/",
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UploadRestaurantMenuTest(TestCase):
    def setUp(self):
        self.rest_1 = Restaurant.objects.create(name="Frank")
        self.rest_2 = Restaurant.objects.create(name="Gwidon")

        self.first_menu = {
            "restaurant_id": self.rest_1.pk,
            "items": [
                {"name": "Spaghetti", "price": "1002.00"},
                {"name": "Pizza", "price": "200.00"},
                {"name": "Beer", "price": "50.00"},
            ],
        }

        self.second_menu = {
            "restaurant_id": self.rest_2.pk,
            "items": [
                {"name": "Soup", "price": "100.00"},
                {"name": "Pasta", "price": "400.00"},
                {"name": "Beef", "price": "500.00"},
            ],
        }

    def test_upload_menu(self):
        response_1 = client.post(
            "/api/restaurants/actions/upload_menu/",
            data=json.dumps(self.first_menu),
            content_type="application/json",
        )
        response_2 = client.post(
            "/api/restaurants/actions/upload_menu/",
            data=json.dumps(self.second_menu),
            content_type="application/json",
        )
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

        check_response_1 = client.get(f"/api/restaurants/{self.rest_1.pk}/menu/")
        check_response_2 = client.get(f"/api/restaurants/{self.rest_2.pk}/menu/")
        self.assertEqual(
            json.dumps(check_response_1.data["items"]),
            json.dumps(self.first_menu["items"]),
        )
        self.assertEqual(
            json.dumps(check_response_2.data["items"]),
            json.dumps(self.second_menu["items"]),
        )
