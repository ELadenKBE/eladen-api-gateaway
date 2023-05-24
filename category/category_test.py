from unittest import skip

from graphene_django.utils.testing import GraphQLTestCase
from django.test import TestCase


class QuestionModelTests(GraphQLTestCase):
    GRAPHQL_URL = '/graphql/'

    def test_get_all_categories(self):
        query = """
                    query{
                      categories{
                        id
                        title
                      }
                    }
                """
        response = self.query(query)
        print(response.content)
        self.assertResponseNoErrors(response)


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
