import json

import requests
from decouple import config
from graphql import GraphQLResolveInfo

from app.errors import ResponseError
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


class ProductService:

    url = config('PRODUCT_SERVICE_URL', default=False, cast=str)

    @verify_connection
    def _get_items(self, entity_name: str, info: GraphQLResolveInfo):
        cleaned = info.context.body.decode('utf-8')\
            .replace('\\n', ' ')\
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        data = response.json().get('data', {})
        return data.get(entity_name, [])

    def get_categories(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='categories', info=info)
        return [Category(**item) for item in items_list]

    def get_goods(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='goods', info=info)
        # TODO continue here: item has objects
        return [create_good_filler(**item) for item in items_list]

    def get_good_lists(self, info: GraphQLResolveInfo = None):
        items_list = self._get_items(entity_name='good_lists', info=info)
        return [GoodsList(**item) for item in items_list]
