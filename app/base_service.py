import json

import requests
from graphql import GraphQLResolveInfo

from app.errors import ResponseError, ValidationError, UnauthorizedError
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

    def verify_connection(self):
        if self.url is None:
            raise ResponseError(f"{self.service_name}"
                                f" Url is not specified")
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

    def _request(self, info: GraphQLResolveInfo, auth_header: dict):
        cleaned = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        query = json.loads(cleaned)['query']
        response = requests.post(self.url,
                                 data={'query': query},
                                 headers=auth_header)
        self._validate_errors(response)
        return response

    def _get_data(self, entity_name: str, info: GraphQLResolveInfo):
        self.verify_connection()
        auth_param = self._get_auth_header(info)
        response = self._request(info=info,
                                 auth_header={"AUTHORIZATION": auth_param})
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
        self.verify_connection()
        item = self._get_data(info=info, entity_name=entity_name)
        return item

    @staticmethod
    def _get_auth_header(info: GraphQLResolveInfo):
        try:
            auth_header: str = info.context.headers['AUTHORIZATION']
        except KeyError as key_error:
            raise UnauthorizedError('authorization error: AUTHORIZATION header'
                                    ' is not specified')
        except ResponseError as response_error:
            raise UnauthorizedError('authorization error: ',
                                    response_error.args[0])
        return auth_header
