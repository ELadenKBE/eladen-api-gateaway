import json

import requests
from graphql import GraphQLResolveInfo

from app.errors import ResponseError, ValidationError
from category.models import Category
from goods.models import Good
from users.models import ExtendedUser


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
    elif seller_dict is not None and category_dict is None:
        return Good(
            **params,
            seller=ExtendedUser(**seller_dict)
        )
    else:
        return Good(**params)


class BaseService:

    url = None
    service_name = None

    def _verify_connection(self):
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
            response = requests.post(self.url,
                                     json=introspection_query)
            if response.status_code == 200:
                pass
            else:
                raise ResponseError(f"{self.service_name}"
                                    f" Service is not answering")
        except requests.exceptions.RequestException:
            raise ResponseError(f"{self.service_name} Service is not answering"
                                )

    def _request(self, info: GraphQLResolveInfo):
        cleaned = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url, data={'query': query})
        self._validate_errors(response)
        return response

    def _get_data(self, entity_name: str, info: GraphQLResolveInfo):
        self._verify_connection()
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

    def _create_item(self, entity_name: str, info: GraphQLResolveInfo):
        self._verify_connection()
        item = self._get_data(info=info, entity_name=entity_name)
        return item
