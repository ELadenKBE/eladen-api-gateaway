import abc

from django.db.models import QuerySet
from django.db import models


class IRepository(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_by_id():
        pass


class RepositoryBase(IRepository):

    @staticmethod
    def get_by_id_base(searched_id: str,
                       model: models.Model) -> [QuerySet]:
        data_to_return = model.objects.get(id=searched_id)
        return [data_to_return]
