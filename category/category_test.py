from graphene_django.utils import GraphQLTestCase

from . import schema


class QuestionModelTests(GraphQLTestCase):
    GRAPHENE_SCHEMA = schema.schema

    def test_get_all_categories(self):
        response = self.query = """
                    query{
                      categories{
                        id
                        title
                      }
                    }
                """
        self.assertResponseNoErrors(response)