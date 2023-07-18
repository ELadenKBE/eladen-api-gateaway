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
