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

    def get_users(self, searched_id=None, search=None):
        """

        :return:
        """
        self.verify_connection()
        if searched_id:
            template = """query{{ users(searchedId: {0} )
            {{ id username email role address firstName lastName }} }}"""
            query = template.format(searched_id)
        elif search:
            template = """query{{ users(search: "{0}")
            {{ id username email role address firstName lastName }} }}"""
            query = template.format(search)
        else:
            query = """query{ users
        { id username email role address firstName lastName } }"""
        response = requests.post(self.url, data={'query': query})
        users_in_dict = response.json().get('data', {}).get('users')
        if users_in_dict is None:
            raise ResponseError('User not found')
        response_users = [ExtendedUser(**user_dict)
                          for user_dict in users_in_dict]
        return response_users
