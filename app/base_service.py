import json

import requests
from graphql import GraphQLResolveInfo

from app.errors import ResponseError, ValidationError
from app.product_service import ProductService, GoodsListTransferType
from category.models import Category
from goods.models import Good
from users.models import ExtendedUser


def verify_connection(func):
    def wrapper(*args, **kwargs):
        try:
            introspection_query = {
                "query": """
                            query {
                                __schema {
                                    queryType {
                                        name
                                    }
                                }
                            }
                        """
            }
            response = requests.post(ProductService.url,
                                     json=introspection_query)
            if response.status_code == 200:
                pass
            else:
                raise ResponseError("Product Service is not answering")
        except requests.exceptions.RequestException:
            raise ResponseError("Product Service is not answering")
        return func(*args, **kwargs)

    return wrapper


def create_good_filler(**params):
    category_dict = None
    seller_dict = None
    if 'category' in params:
        category_dict = params['category']
        del params['category']
    if 'seller' in params:
        seller_dict = params['seller']
        del params['seller']
    if seller_dict is not None and category_dict is not None:
        return Good(
            **params,
            category=Category(**category_dict),
            seller=ExtendedUser(**seller_dict)
        )
    elif seller_dict is None and category_dict is not None:
        return Good(
            **params,
            category=Category(**category_dict)
        )
    elif seller_dict is not None and category_dict is  None:
        return Good(
            **params,
            seller=ExtendedUser(**seller_dict)
        )
    else:
        return Good(**params)


def create_goods_list_filler(**params) -> GoodsListTransferType:
    user_dict = None
    goods_dict = None
    if 'user' in params:
        user_dict = params['user']
        del params['user']
    if 'goods' in params:
        goods_dict = params['goods']
        del params['goods']
    if user_dict is not None and goods_dict is not None:
        goods = [Good(**param) for param in goods_dict]
        goods_list = GoodsListTransferType(**params,
                                           user=ExtendedUser(**user_dict),
                                           goods=goods)
        return goods_list
    if user_dict is not None and goods_dict is None:
        goods_list = GoodsListTransferType(**params,
                                           user=ExtendedUser(**user_dict))
        return goods_list
    else:
        type_object = GoodsListTransferType(**params)
        return type_object


class BaseService:

    url = None

    def _request(self, info: GraphQLResolveInfo):
        cleaned = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        self._validate_errors(response)
        return response

    @verify_connection
    def _get_data(self, entity_name: str, info: GraphQLResolveInfo):
        response = self._request(info=info)
        data = response.json().get('data', {})
        return data.get(entity_name, [])

    @staticmethod
    def _validate_errors(response):
        if 'errors' in str(response.content):
            cleaned_json = json.loads(
                response.content.decode('utf-8').replace("/", "")
            )['errors']
            raise ValidationError(cleaned_json[0]['message'])

    @verify_connection
    def _create_item(self, entity_name: str, info: GraphQLResolveInfo):
        item = self._get_data(info=info, entity_name=entity_name)
        return item
