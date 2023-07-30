import re

import graphene
import requests
from decouple import config
from graphene_django import DjangoObjectType

from app.base_service import BaseService
from app.errors import ResponseError
from goods.models import Good
from users.models import ExtendedUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


class UserService(BaseService):

    #url = config('USER_SERVICE_URL',
    #            default="http://user-identity:8081/graphql/", cast=str)
    url = "http://user-identity:8081/graphql/"
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

    def get_user_by_id(self, user_id: str):
        """
        Get user by id.

        :param user_id:
        :return:
        """
        self.verify_connection()
        query_template = """query{{
                  users(searchedId: {0}){{
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

        query = query_template.format(user_id)
        response = requests.post(self.url, data={'query': query})
        user_in_dict = response.json().get('data', {}).get('users')[0]
        if user_in_dict is None:
            user = ExtendedUser(id=0,
                                username="userNotFound",
                                email="userNotFound")
        else:
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
        if len(items_list_dict) == 0:
            response_users = [ExtendedUser(**user_dict)
                              for user_dict in items_list_dict]
        else:
            response_users = []
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

    def add_user_to_good_lists(self, info, items_list):
        input_query = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        pattern = r'user\s*{\s*[^}]*\s*}'
        if 'user' not in items_list[0]:
            return [create_goods_list_filler(user_service=self, **good_list)
                    for good_list in items_list]
        user_query = re.search(pattern, input_query).group()
        pattern = r'{([^}]*)}'
        matches = re.findall(pattern, user_query)
        user_query_template = """query{{ users(searchedId: {0}){{ {1} }} }}"""
        user_queries = [user_query_template.format(elem["userId"],
                                                   ''.join(matches)
                                                   ) for elem in items_list]
        users_dict = [self._get_data(entity_name='users',
                               info=info,
                               query=query) for query in user_queries]
        for goods_list_dict in items_list:
            user_id = goods_list_dict['userId']
            goods_list_dict.pop('userId')
            user_dict_final = None
            for user_dict in users_dict:
                if user_dict[0] is not None\
                        and int(user_dict[0]['id']) == user_id:
                    user_dict_final = user_dict[0]
                    break
            if user_dict_final is None:
                goods_list_dict['users'] = {'id': 0, 'username': 'deleted'}
            else:
                goods_list_dict['users'] = user_dict_final

        return [create_goods_list_filler(**good_list) for good_list in items_list]


class GoodType(DjangoObjectType):

    class Meta:
        model = Good


class GoodsListTransferType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    user = graphene.Field(UserType)
    goods = graphene.List(GoodType)

    def __init__(self, id=None, title=None, user=None, goods=None):
        self.id = id
        self.title = title
        self.user = user
        self.goods = goods


def create_goods_list_filler(user_service: UserService =None,
                             **params) -> GoodsListTransferType:
    user = None
    goods_dict = None
    if 'userId' in params:
        user_id = params['userId']
        user = user_service.get_user_by_id(user_id=user_id)
        del params['userId']
    if 'goods' in params:
        goods_dict = params['goods']
        del params['goods']
    if user is not None and goods_dict is not None:
        goods = [Good(**param) for param in goods_dict]
        goods_list = GoodsListTransferType(**params,
                                           user=user,
                                           goods=goods)
        return goods_list
    elif user is not None and goods_dict is None:
        goods_list = GoodsListTransferType(**params,
                                           user=user)
        return goods_list
    elif user is None and goods_dict is not None:
        goods = [Good(**param) for param in goods_dict]
        goods_list = GoodsListTransferType(**params,
                                           goods=goods)
        return goods_list
    else:
        type_object = GoodsListTransferType(**params)
        return type_object
