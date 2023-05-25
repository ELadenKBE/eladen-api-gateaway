import json
from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from django.test import TestCase

from app.errors import UnauthorizedError
from category.models import Category
from users.models import ExtendedUser


class QuestionModelTests(GraphQLTestCase):
    """Test category endpoint.
    """
    GRAPHQL_URL = '/graphql/'
    test_category_data = []
    test_users_data = []

    @classmethod
    def setUpTestData(cls):
        """Create test data
        """
        cls.test_category_data = [
            Category(title='Example'),
            Category(title='Example2'),
            Category(title='Example3'),
            Category(title='Example4')
        ]
        Category.objects.bulk_create(cls.test_category_data)
        admin = ExtendedUser(email="sometest@gmail.com",
                             username="admin",
                             role=3)
        admin.set_password("12345")
        seller = ExtendedUser(email="sometest@gmail.com",
                              username="seller",
                              role=2)
        seller.set_password("12345")
        user = ExtendedUser(email="sometest@gmail.com",
                            username="user",
                            role=1)
        user.set_password("12345")
        cls.test_users_data = [admin, seller, user]
        ExtendedUser.objects.bulk_create(cls.test_users_data)

    def request_graphql(self, role, formatted_query):
        if role:
            user = ExtendedUser.objects.get(username=role)
            token = get_token(user)
            headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
            return self.query(
                query=formatted_query,
                headers=headers
            )
        else:
            return self.query(
                query=formatted_query,
            )

    @staticmethod
    def check_for_permission_errors(response):
        try:
            errors = json.loads(response.content).get('errors')
            if errors[0].get('message') == 'Not enough permissions to call ' \
                                           'this endpoint':
                raise UnauthorizedError("not enough permissions")
        except TypeError:
            return
        except AttributeError as e:
            raise e

    def create_item_as(self, role=None):
        """Test if the item can be created with admin role"""
        query = '''mutation{{ createCategory(title:"{0}"){{
                               id
                               title 
                           }} 
                         }}
                       '''
        category_title = 'some_special_title'
        formatted_query = query.format(category_title)

        response = self.request_graphql(role, formatted_query)
        self.check_for_permission_errors(response)

        tested_id = json.loads(response.content) \
            .get('data') \
            .get('createCategory') \
            .get('id')
        expected_id = Category.objects.get(id=tested_id).id

        self.assertResponseNoErrors(response, "response has errors")
        self.assertEqual(expected_id, tested_id,
                         "the object's id are not match")

    def test_get_all_categories(self):
        """Test get all categories"""
        query = """
                    query{
                      categories{
                        id
                        title
                      }
                    }
                """
        response = self.query(query)
        response_data = json.loads(response.content).get("data") \
            .get("categories")

        self.assertResponseNoErrors(response, "response has errors")
        self.assertEqual(len(self.test_category_data), len(response_data),
                         "query does not return right amount of data")

    def test_create_item_as_admin(self):
        """Test if can be created by admin"""
        self.create_item_as("admin")

    def test_create_item_as_seller(self):
        """Test if can be created by seller"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("seller")

    def test_create_item_as_user(self):
        """Test if can be created by user"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("user")

    def test_create_item_as_anon(self):
        """Test if can be created by anonymous user"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as()

    def test_get_by_id(self):
        """Test get by id. Should be implemented by every entity"""
        query = """query{
                  categories(searchedId: "1"){
                    id
                    title
                  }
                }"""
        response = self.query(query)
        response_data = json.loads(response.content).get("data") \
            .get("categories")

        self.assertResponseNoErrors(response, "response has errors")
        self.assertEqual("1", response_data[0].get('id'), "id should match")

    def update_by_id_as(self, role: str = None):
        """Perform update on specified role

        :param role: string definition of role
        """
        query = '''mutation{{
                      updateCategory(id:1, title:"{0}"){{
                        id
                        title
                      }}
                    }}'''
        category_title = 'updated'
        formatted_query = query.format(category_title)
        response = self.request_graphql(role=role,
                                        formatted_query=formatted_query)
        self.check_for_permission_errors(response)

        tested_update = json.loads(response.content) \
            .get('data') \
            .get('updateCategory') \
            .get('title')
        expected_title = "updated"

        self.assertResponseNoErrors(response, "response has errors")
        self.assertEqual(expected_title, tested_update,
                         "the object was not updated")

    def test_update_by_id_as_admin(self):
        """Test admin should be allowed to update any entity"""
        self.update_by_id_as("admin")

    def test_update_by_id_as_seller(self):
        """Test seller should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as("seller")

    def test_update_by_id_as_user(self):
        """Test user should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as("user")

    def test_update_by_id_as_anon(self):
        """Test anon should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as()


@skip("")
class YourTestCase(TestCase):
    def test_post_request(self):
        query = """query{
                              categories{
                                id
                                title
                              }
                            }
                        """

        response = self.client.post('/graphql/', data={'query': query})

        self.assertEqual(response.status_code, 200)
        print(response.content)
