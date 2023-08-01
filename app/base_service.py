import json
import re

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


def build_mutation_string(operation, operation_name, variables, params):
    # Build the variables part of the mutation string
    variables_string = ', '.join([f"{key}: \"{value}\"" if isinstance(value, str) else f"{key}: {value}" for key, value in variables.items()])
    mutation_string = f" {operation} {{ {operation_name}({variables_string}) " \
                      f"{{{ params } }}}}"

    return mutation_string


def extract_content_in_brackets(input_string):
    pattern = r"\{(.*?)\}"
    matches = re.findall(pattern, input_string)

    if matches:
        result = matches[0].strip().split("{")[1]
    return result


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
                                    f" Service is not answering: request sent"
                                    f" to {self.url}")
        except requests.exceptions.RequestException:
            raise ResponseError(f"{self.service_name}"
                                    f" Service is not answering: request sent"
                                    f" to {self.url}")

    def _request(self,  query: str, auth_header: dict = None,):
        if auth_header is None:
            response = requests.post(self.url,
                                     data={'query': query})
        else:
            response = requests.post(self.url,
                                     data={'query': query},
                                     headers=auth_header)
        self._validate_errors(response)
        return response

    def _get_data(self,
                  entity_name: str,
                  info: GraphQLResolveInfo,
                  query=None):
        if query is None:
            query = self._clean_query(info)
        self.verify_connection()
        try:
            auth_param = self._get_auth_header(info)
            response = self._request(auth_header={"AUTHORIZATION": auth_param},
                                     query=query)
        except UnauthorizedError:
            response = self._request(query=query)
        data = response.json().get('data', {})
        response_dict = data.get(entity_name, [])
        return response_dict

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

    @staticmethod
    def _clean_query(info: GraphQLResolveInfo):
        cleaned = info.context.body.decode('utf-8') \
            .replace('\\n', ' ') \
            .replace('\\t', ' ')
        json_cleaned = json.loads(cleaned)
        query = json_cleaned['query']
        try:
            variables = json_cleaned['variables']
            operation_name = json_cleaned['operationName'][0].lower() +\
                             json_cleaned['operationName'].split()[0][1:]
            mutation_name = query.split()[0]
            params = extract_content_in_brackets(query)
            query = build_mutation_string(params=params,
                                          variables=variables,
                                          operation_name=operation_name,
                                          operation=mutation_name)
        except KeyError:
            pass
        return query
