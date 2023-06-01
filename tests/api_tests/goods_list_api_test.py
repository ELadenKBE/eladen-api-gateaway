from django.db import models

from app.errors import UnauthorizedError
from goods_list.models import GoodsList
from .base_api_test import WrapperForBaseTestClass


class GoodsListEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test goods list endpoint.
        """

    model = GoodsList
    mutation_create = '''mutation{{
                      createGoodsList(
                        title:"{0}",
                      ){{
                        id
                            title
                      }}
                    }}'''
    mutation_create_name = "createGoodsList"
    all_query = """query{
                  goodsLists{
                    id
                    title
                    user {
                      id
                    }
                  }
                }"""
    by_id_query = """"""
    mutation_update = ''''''
    mutation_update_name = ''

    mutation_delete = ''''''
    plural_name = ""

    @staticmethod
    def create_item() -> models.Model:
        pass

    def test_create_item_as_admin(self):
        self.create_item_as("admin")

    def test_create_item_as_seller(self):
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

    def test_get_all_items_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            super().test_get_all_items_as_anon()
