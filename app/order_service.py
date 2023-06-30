from decouple import config

from app.base_service import BaseService


class OrderService(BaseService):

    url = config('ORDER_SERVICE_URL', default=False, cast=str)

