from django.db import models

from app.errors import UnauthorizedError
from goods.models import Good
from users.models import ExtendedUser
from .base_api_test import WrapperForBaseTestClass


class UserEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test goods list endpoint.
        """
    model = ExtendedUser
    mutation_create = ''''''
    mutation_create_name = ""
    all_query = """"""
    by_id_query = """"""
    mutation_update = ''''''
    mutation_update_name = ''

    mutation_delete = ''''''
    plural_name = ""

    @staticmethod
    def create_item() -> models.Model:
        pass

    def test_create_item_as_admin(self):
        self.fail()

    def test_create_item_as_seller(self):
        self.fail()

    def test_create_item_as_user(self):
        self.fail()

    def test_create_item_as_anon(self):
        self.fail()

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