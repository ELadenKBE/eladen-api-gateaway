from django.db import models

from api_tests.base_api_test import WrapperForBaseTestClass


class GoodEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test category endpoint.
    """

    mutation_create = '''
                                   '''

    def test_create_item_as_admin(self):
        pass

    def test_create_item_as_seller(self):
        pass

    def test_create_item_as_user(self):
        pass

    def test_create_item_as_anon(self):
        pass



    @staticmethod
    def create_item() -> models.Model:
        pass