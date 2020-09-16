from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CartTest(APITestCase):
    def setUp(self) -> None:
        pass

    def test_cart_create(self):
        self.fail()

    def test_cart_item_list(self):
        self.fail()

    def test_cart_item_update(self):
        self.fail()

    def test_cart_item_delete(self):
        self.fail()
