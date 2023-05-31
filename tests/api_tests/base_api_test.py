import abc
import json
import re

from django.db import models
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.shortcuts import get_token

from app.errors import UnauthorizedError
from category.models import Category
from goods.models import Good
from users.models import ExtendedUser


class IEndpointTest:

    @property
    @abc.abstractmethod
    def model(self) -> models.Model:
        """
        Every class has to define a reference to data model.

        :return: models.Model django model
        """
        pass

    @property
    @abc.abstractmethod
    def mutation_delete(self) -> str:
        """
        Every class has to define a delete-mutation.

        :return: str name
        """
        pass

    @property
    @abc.abstractmethod
    def mutation_create_name(self) -> str:
        """
        Every class has to define a  name of the create-mutation.
        For example "createCategories"

        :return: str name
        """
        pass

    @property
    @abc.abstractmethod
    def mutation_update_name(self) -> str:
        """
        Every class has to define a name of the update-mutation.
        For example "updateCategories"

        :return: str name
        """
        pass

    @property
    @abc.abstractmethod
    def plural_name(self) -> str:
        """
        Every class has to define a plural name of the entity.
        For example "categories"

        :return: str name
        """
        pass

    @property
    @abc.abstractmethod
    def mutation_update(self) -> str:
        """
        Every class has to define an update-mutation of the entity.

        :return: str name
        """
        pass

    @property
    @abc.abstractmethod
    def mutation_create(self) -> str:
        """
        Every class has to define a create-mutation
        :return: str mutation
        """
        pass

    @property
    @abc.abstractmethod
    def all_query(self) -> str:
        """
        Every class has to define a query for all elements
        :return: str query
        """
        pass

    @property
    @abc.abstractmethod
    def by_id_query(self) -> str:
        """
        Every class has to define a query to get one first element by id
        :return: str query
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_item() -> models.Model:
        """
        Every test class must implement create object method.

        :return: models.Model
        """
        pass

    @abc.abstractmethod
    def test_create_item_as_admin(self):
        """
        Implement test creation by admin
        """
        pass

    @abc.abstractmethod
    def test_create_item_as_seller(self):
        """
                Implement test creation by Seller
                """
        pass

    @abc.abstractmethod
    def test_create_item_as_user(self):
        """
                Implement test creation by User
                """
        pass

    @abc.abstractmethod
    def test_create_item_as_anon(self):
        """
                Implement test creation by Anonymous User
                """
        pass

    @abc.abstractmethod
    def test_update_by_id_as_admin(self):
        """
        Implement test update by Admin
        """
        pass

    @abc.abstractmethod
    def test_update_by_id_as_seller(self):
        """
        Implement test update by Seller
        """
        pass

    @abc.abstractmethod
    def test_update_by_id_as_user(self):
        """
        Implement test update by User
        """
        pass

    @abc.abstractmethod
    def test_update_by_id_as_anon(self):
        """
        Implement test update by Anonymous User
        """
        pass

    @abc.abstractmethod
    def test_delete_by_id_as_admin(self):
        """
          Implement test delete by Admin
        """
        pass

    @abc.abstractmethod
    def test_delete_by_id_as_seller(self):
        """
            Implement test delete by Seller
        """
        pass

    @abc.abstractmethod
    def test_delete_by_id_as_user(self):
        """
           Implement test update by User
        """
        pass

    @abc.abstractmethod
    def test_delete_by_id_as_anon(self):
        """
          Implement test update by Anonymous User
        """
        pass


class WrapperForBaseTestClass:
    """Wrapper class prevents execution when tests are discovered"""

    class BaseEndpointsTests(GraphQLTestCase, IEndpointTest):
        """Base class for api tests.

        1.Use double brackets for non parameter brackets.

        2.String parameters should be with quotes:  title: "{0}"
        """
        GRAPHQL_URL = '/graphql/'
        mutation_create = None

        @classmethod
        def setUpClass(cls):
            """Create test data
            """
            cls.create_users()
            cls.create_categories()
            cls.create_goods()

        @classmethod
        def tearDownClass(cls):
            pass

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
                if errors[0].get('message') == 'Not enough permissions to call' \
                                               ' this endpoint':
                    raise UnauthorizedError("not enough permissions")
            except TypeError:
                return
            except AttributeError as e:
                raise e

        @staticmethod
        def count_occurrences_of_variables(string):
            pattern = r"{\d+}"
            occurrences = re.findall(pattern, string)
            return len(occurrences)

        def create_item_as(self, role=None):
            """Test if the item can be created with admin role"""
            formatted_mutation = self.format_mutation(self.mutation_create,
                                                      "test_mock")

            response = self.request_graphql(role, formatted_mutation)
            self.check_for_permission_errors(response)
            tested_id = json.loads(response.content) \
                .get('data') \
                .get(self.mutation_create_name) \
                .get('id')
            expected_id = self.model.objects.get(id=tested_id).id

            self.assertResponseNoErrors(response, "response has errors")
            self.assertEqual(expected_id, tested_id,
                             "the object's id are not match")

        def update_by_id_as(self, fields: list, role: str = None):
            """Perform update on specified role

            :param fields: fields to update
            :param role: string definition of role
            """
            if self.mutation_update_name == "":
                self.fail("self.mutation_update_name is not defined!")
            update_title = 'updated'
            update_titles_list = [update_title] * len(fields)
            formatted_mutation = self.format_mutation(self.mutation_update,
                                                      update_title)
            response = self.request_graphql(role=role,
                                            formatted_query=formatted_mutation)
            self.check_for_permission_errors(response)
            try:
                received_updates = list(
                    map(lambda field: json.loads(response.content) \
                        .get('data') \
                        .get(self.mutation_update_name) \
                        .get(field), fields))
                self.assertResponseNoErrors(response, "response has errors")
                self.assertEqual(update_titles_list, received_updates,
                                 "the object was not updated")
            except Exception:
                print(json.loads(response.content))
                self.fail()

        def delete_by_id_as(self, role=None):
            """
            Helper function to delete object with specified role

            :param role: str definition of role
            """
            object_to_delete = self.create_item()
            id_to_delete = object_to_delete.id
            formatted_mutation = self.format_mutation(self.mutation_delete,
                                                      str(id_to_delete))
            response = self.request_graphql(role=role,
                                            formatted_query=formatted_mutation)
            self.check_for_permission_errors(response)
            self.assertIsNone(
                self.model.objects.filter(id=id_to_delete).first(),
                "object has to be deleted")
            self.assertResponseNoErrors(response, "response has errors")

        def test_get_all_items(self):
            """Test get all items"""
            query = self.all_query
            response = self.query(query)
            response_data = json.loads(response.content).get("data") \
                .get(self.plural_name)

            self.assertResponseNoErrors(response, "response has errors")
            self.assertEqual(self.model.objects.all().count(),
                             len(response_data),
                             "query does not return right amount of data")

        def test_get_by_id(self):
            """Test get by id. Should be implemented by every entity"""
            if self.by_id_query == "":
                self.fail("self.by_id_query is not defined!")
            query = self.by_id_query
            response = self.query(query)
            response_data = json.loads(response.content).get("data") \
                .get(self.plural_name)

            self.assertResponseNoErrors(response, "response has errors")
            self.assertEqual("1", response_data[0].get('id'), "id should match")

        def format_mutation(self, mutation: str, filler: str) -> str:
            number_of_params = self.count_occurrences_of_variables(
                self.mutation_create)
            string_list = []
            for i in range(number_of_params):
                string_var = filler
                string_list.append(string_var)
                try:
                    return mutation.format(*string_list)
                except KeyError:
                    self.fail("check double brackets in mutation")

        @classmethod
        def create_users(cls):
            if ExtendedUser.objects.all().count() > 0:
                return
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
            test_users_data = [admin, seller, user]
            ExtendedUser.objects.bulk_create(test_users_data)

        @classmethod
        def create_categories(cls):
            if Category.objects.all().count() > 0:
                return
            test_category_data = [
                                     Category(title='Example')] * 4
            Category.objects.bulk_create(test_category_data)

        @classmethod
        def create_goods(cls):
            if Good.objects.all().count() > 0:
                return
            test_goods_data = [
                                  Good(url="https://moodle.htw-berlin.de/my/",
                                       description="test_description",
                                       title="some_test_title",
                                       seller_id=2,
                                       address="some_test_address",
                                       category_id=1,
                                       price=123
                                       ),
                              ] * 4
            Good.objects.bulk_create(test_goods_data)

# @skip("")
#             class YourTestCase(TestCase):
#                 def test_post_request(self):
#                     query = """query{
#                                                             categories{
#                                                                      id
#                                                                        title
#                                                                          }
#                                                                        }
#                                                                    """
#
#                     response = self.client.post('/graphql/',
#                                                 data={'query': query})
#
#                     self.assertEqual(response.status_code, 200)
#                     print(response.content)
