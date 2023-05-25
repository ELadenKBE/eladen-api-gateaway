import json
from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token
from django.test import TestCase

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
        cls.test_users_data = [
           admin
        ]
        ExtendedUser.objects.bulk_create(cls.test_users_data)

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

    def test_create_category_as_admin(self):
        user = ExtendedUser.objects.get(username="admin")
        token = get_token(user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        query = '''mutation{{ createCategory(title:"{0}"){{
                        id
                        title 
                    }} 
                  }}
                '''
        category_title = 'some_special_title'

        formatted_query = query.format(category_title)
        response = self.query(
            query=formatted_query,
            headers=headers
        )
        tested_id = json.loads(response.content) \
            .get('data') \
            .get('createCategory') \
            .get('id')
        expected_id = Category.objects.get(id=tested_id).id
        self.assertResponseNoErrors(response, "response has errors")
        self.assertEqual(expected_id, tested_id,
                         "the object's id are not match")



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
