import json

import requests
from decouple import config
from graphql import GraphQLResolveInfo

from app.errors import ResponseError, ValidationError
from category.models import Category
from goods.models import Good
from goods_list.models import GoodsList
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


def create_goods_list(**params):
    user_dict = None
    goods_dict = None
    if 'user' in params:
        user_dict = params['user']
        del params['user']
    if 'goods' in params:
        goods_dict = params['goods']
        del params['goods']
    if user_dict is not None and goods_dict is not None:
        goods_list = GoodsList(**params, user=ExtendedUser(**user_dict))
        goods = [Good(**param) for param in goods_dict]
        goods_list.goods.add(*[good.id for good in goods])
        return goods_list
    else:
        return GoodsList(**params)


class ProductService:

    url = config('PRODUCT_SERVICE_URL', default=False, cast=str)

    def _request(self, info: GraphQLResolveInfo):
        cleaned = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        return response

    @verify_connection
    def _get_items(self, entity_name: str, info: GraphQLResolveInfo):
        response = self._request(info=info)
        data = response.json().get('data', {})
        return data.get(entity_name, [])

    def get_categories(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='categories', info=info)
        return [Category(**item) for item in items_list]

    def get_goods(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='goods', info=info)
        return [create_good_filler(**item) for item in items_list]

    def get_good_lists(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='good_lists', info=info)
        return [GoodsList(**item) for item in items_list]