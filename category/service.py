import json

import requests
from decouple import config
from graphql import GraphQLResolveInfo

from app.errors import ResponseError
from category.models import Category


def verify_connection(func):
    def wrapper(*args, **kwargs):
        try:
            response = requests.post(CategoryService.url)
            # TODO finish here 21.06.2023
            if response.status_code == 200:
                pass
            else:
                raise ResponseError("Category Service is not answering")
        except requests.exceptions.RequestException:
            raise ResponseError("Category Service is not answering")
        return func(*args, **kwargs)

    return wrapper


class CategoryService:

    url = config('PRODUCT_SERVICE_URL', default=False, cast=str)

    @verify_connection
    def get_items(self, info: GraphQLResolveInfo = None):
        cleaned = info.context.body.decode('utf-8')\
            .replace('\\n', ' ')\
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        data = response.json().get('data', {})
        category_list = data.get('categories', [])
        return [Category(**item) for item in category_list]
