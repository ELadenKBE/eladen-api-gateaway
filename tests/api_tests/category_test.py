import json
from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from django.test import TestCase

from category.models import Category


class QuestionModelTests(GraphQLTestCase):
    """Test category endpoint.
    """
    GRAPHQL_URL = '/graphql/'
    test_data = []

    @classmethod
    def setUpTestData(cls):
        """Create test data
        """
        cls.test_data = [
            Category(title='Example'),
            Category(title='Example2'),
            Category(title='Example3'),
            Category(title='Example4')
        ]
        Category.objects.bulk_create(cls.test_data)

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

        self.assertResponseNoErrors(response)
        self.assertEqual(len(self.test_data), len(response_data),
                         "query does not return right amount of data")


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
