from django.db import models

from app.errors import UnauthorizedError
from goods.models import Good
from orders.models import Order
from .base_api_test import WrapperForBaseTestClass


class OrderEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test goods list endpoint.
        """
    model = Order
    mutation_create = '''mutation{{
          createOrder(timeOfOrder:"1999-05-23 11:12",
             deliveryAddress:"{0}",
             itemsPrice:123,
             deliveryPrice:123){{
            id
            timeOfOrder
            deliveryAddress
            itemsPrice
            deliveryPrice
            user{{
              id
            }}
          }}
        }}'''
    mutation_create_name = "createOrder"
    all_query = """"""
    by_id_query = """"""
    mutation_update = ''''''
    mutation_update_name = ''

    mutation_delete = ''''''
    plural_name = "orders"

    @staticmethod
    def create_item_with(user) -> models.Model:
        pass

    def test_create_item_as_admin(self):
        self.create_item_as("admin")

    def test_create_item_as_seller(self):
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("seller")

    def test_create_item_as_user(self):
        self.create_item_as("user")

    def test_create_item_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            self.create_item_as()

    def test_update_by_id_as_admin(self):
        self.fail()

    def test_update_by_id_as_seller(self):
        self.fail()

    def test_update_by_id_as_user(self):
        self.fail()

    def test_update_by_id_as_anon(self):
        self.fail()

    def test_delete_by_id_as_admin(self):
        self.fail()

    def test_delete_by_id_as_seller(self):
        self.fail()

    def test_delete_by_id_as_user(self):
        self.fail()

    def test_delete_by_id_as_anon(self):
        self.fail()
