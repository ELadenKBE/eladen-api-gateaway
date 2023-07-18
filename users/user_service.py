import requests
from decouple import config
from graphene_django import DjangoObjectType

from app.base_service import BaseService
from app.errors import ResponseError
from users.models import ExtendedUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


class UserService(BaseService):

    url = config('USER_SERVICE_URL', default=None, cast=str)
    service_name = 'User'

    def get_user(self, sub: str):
        """
        Get user by sub.

        :param sub:
        :return:
        """
        self.verify_connection()
        query_template = """query{{
                  users(sub: "{0}"){{
                            id
                            username
                            email
                            role
                            address
                            firstName
                            lastName
                            sub
                      }}
                }}"""

        query = query_template.format(sub)
        response = requests.post(self.url, data={'query': query})
        user_in_dict = response.json().get('data', {}).get('users')[0]
        if user_in_dict is None:
            raise ResponseError('User not found')
        user = ExtendedUser(**user_in_dict)
        return user

    def get_users(self, info):
        """

        :return:
        """
        self.verify_connection()
        items_list_dict = self._get_data(entity_name='users', info=info)
        if items_list_dict is None:
            raise ResponseError('User not found')
        response_users = [ExtendedUser(**user_dict)
                          for user_dict in items_list_dict]
        return response_users

    def create_user(self, info):
        self.verify_connection()
        created_item_in_dict = self._create_item(info=info,
                                                 entity_name='createUser')
        return ExtendedUser(**created_item_in_dict)

    def update_user(self, info):
        self.verify_connection()
        updated_item: dict = self._get_data(entity_name='updateUser',
                                            info=info)
        if updated_item['firstname']:
            updated_item['firstName'] = updated_item['firstname']
            del updated_item['firstname']
        if updated_item['lastname']:
            updated_item['lastName'] = updated_item['lastname']
            del updated_item['lastname']
        return ExtendedUser(**updated_item)

    def delete_user(self, info):
        self._get_data(info=info, entity_name='deleteUser')

