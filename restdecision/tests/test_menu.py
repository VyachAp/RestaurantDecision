import json
from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase, Client
from restdecision.models.restaurant import Restaurant

# initialize the APIClient app
client = Client()


class GetAllRestaurantsTest(TestCase):
    """Test module for GET all restaurants API"""

    def setUp(self):
        self.restaurant_1 = Restaurant.objects.create(name="Frank")
        self.restaurant_2 = Restaurant.objects.create(name="Basta")
        self.restaurant_3 = Restaurant.objects.create(name="345")

        self.user = User.objects.create(username="testuser", password="12345")
        self.menu_1 = {
            "restaurant_id": self.restaurant_1.pk,
            "items": [
                {"name": "Spaghetti", "price": "1002.00"},
                {"name": "Pizza", "price": "200.00"},
                {"name": "Beer", "price": "50.00"},
            ],
        }
        self.menu_2 = {
            "restaurant_id": self.restaurant_2.pk,
            "items": [
                {"name": "Lasagna", "price": "102.00"},
                {"name": "Coffee", "price": "20.00"},
                {"name": "Chocolate", "price": "520.00"},
            ],
        }
        self.menu_3 = {
            "restaurant_id": self.restaurant_3.pk,
            "items": [
                {"name": "Chicken", "price": "10.00"},
                {"name": "Burger", "price": "20.00"},
                {"name": "Cider", "price": "50.00"},
            ],
        }
        self.response_menu_1 = client.post(
            "/api/restaurants/actions/upload_menu/",
            data=json.dumps(self.menu_1),
            content_type="application/json",
        )
        self.response_menu_2 = client.post(
            "/api/restaurants/actions/upload_menu/",
            data=json.dumps(self.menu_2),
            content_type="application/json",
        )
        self.response_menu_3 = client.post(
            "/api/restaurants/actions/upload_menu/",
            data=json.dumps(self.menu_3),
            content_type="application/json",
        )
        self.response = [
            {"restaurant": "Frank", "points": 3},
            {"restaurant": "Basta", "points": 2},
            {"restaurant": "345", "points": 1},
        ]

    def test_first_version_vote(self):
        client.force_login(self.user)
        version_header = {"BUILD_VERSION": "1"}
        response = client.post(
            "/api/menus/actions/vote",
            data={"menu": self.response_menu_1.json()["restaurant_id"]},
            **version_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_second_version_vote(self):
        client.force_login(self.user)
        version_header = {"BUILD_VERSION": "2"}
        data = [
            {"menu": self.response_menu_1.json()["restaurant_id"], "points": 3},
            {"menu": self.response_menu_2.json()["restaurant_id"], "points": 2},
            {"menu": self.response_menu_3.json()["restaurant_id"], "points": 1},
        ]
        response = client.post(
            "/api/menus/actions/vote",
            data=json.dumps(data),
            content_type="application/json",
            **version_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check = client.get("/api/menus/votes/")
        self.assertEqual(json.dumps(check.data), json.dumps(self.response))
