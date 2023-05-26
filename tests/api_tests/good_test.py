from django.db import models

from app.errors import UnauthorizedError
from goods.models import Good
from .base_api_test import WrapperForBaseTestClass


class GoodEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test category endpoint.
    """

    model = Good
    mutation_create = '''mutation{{
                             createGood(
                                title:{0},
                                description:{1},
                                address:{2},
                                categoryId:1,
                                price: 123.12
                        
                        ){{ title }} }}
                      '''
    mutation_create_name = "createGood"
    all_query = """query{ goods{ id title description address url price category
                        { id title } seller{ id username email } } }
                        """
    by_id_query = """"""
    mutation_update = ''''''
    mutation_update_name = ''

    mutation_delete = ''''''
    plural_name = "goods"

    def test_create_item_as_admin(self):
        """Test. if can be created by admin"""
        self.create_item_as("admin")

    def test_create_item_as_seller(self):
        """Test. if can be created by seller"""
        self.create_item_as("seller")

    def test_create_item_as_user(self):
        """Test. if can be created by user"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("user")

    def test_create_item_as_anon(self):
        """Test. if can be created by anon"""
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

    @staticmethod
    def create_item() -> models.Model:
        item = Good(url="https://moodle.htw-berlin.de/my/",
             description="test_description",
             title="some_test_title",
             seller_id=2,
             address="some_test_address",
             category_id=1,
             price=123
             )
        item.save()
        return item
