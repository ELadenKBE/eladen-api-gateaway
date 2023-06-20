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
    by_id_query = """query{
                  goodsLists(searchedId:1){
                    id
                    title
                    goods{
                      id
                      title
                    }
                  }
                }"""
    mutation_update = '''mutation{{
                      updateGoodsList(listId:{0}, title:"{1}"){{
                        id
                        title
                      }}
                    }}'''
    mutation_update_name = 'updateGoodsList'

    mutation_delete = '''mutation{{
                          deleteGoodsList(listId:{0}){{
                            id
                          }}
                        }}'''
    plural_name = "goodsLists"

    @staticmethod
    def create_item_with(user) -> models.Model:
        item = GoodsList(title="admin", user=user)
        item.save()
        return item

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
        self.update_by_id_as(role="admin", fields=["title"])

    def test_update_by_id_as_seller(self):
        self.update_by_id_as(role="seller", fields=["title"])

    def test_update_by_id_as_user(self):
        self.update_by_id_as(role="user", fields=["title"])

    def test_update_by_id_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as(fields=["title"])

    def test_delete_by_id_as_admin(self):
        self.delete_by_id_as("admin")

    def test_delete_by_id_as_seller(self):
        self.delete_by_id_as("seller")

    def test_delete_by_id_as_user(self):
        self.delete_by_id_as("user")

    def test_delete_by_id_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            self.delete_by_id_as()

    def test_get_all_items_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            super().test_get_all_items_as_anon()

    def test_get_by_id_as_anon(self):
        with self.assertRaises(UnauthorizedError):
            super().test_get_by_id_as_anon()
