import json

import requests
from decouple import config
from graphql import GraphQLResolveInfo

from category.models import Category


class CategoryService:

    url = config('PRODUCT_SERVICE_URL', default=False, cast=str)

    def get_items(self, info: GraphQLResolveInfo = None):
        cleaned = info.context.body.decode('utf-8')\
            .replace('\\n', ' ')\
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        data = response.json().get('data', {})
        category_list = data.get('categories', [])
        return [Category(**item) for item in category_list]
