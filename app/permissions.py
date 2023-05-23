import abc
from typing import Type

from django.contrib.auth.models import AnonymousUser

from app.errors import UnauthorizedError


class IUser(abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def is_equal(role):
        pass


class Admin(IUser):
    @staticmethod
    def is_equal(role):
        pass


class User(IUser):
    @staticmethod
    def is_equal(role):
        pass


class Seller(IUser):
    @staticmethod
    def is_equal(role):
        pass


class All(IUser):
    @staticmethod
    def is_equal(role):
        if isinstance(role, AnonymousUser):
            return True
        return False


def permission(roles: list[Type[IUser]] = None):
    def inner_permission(func):
        def validate_permission_scope(*arg, **kwargs):
            user = arg[1].context.user
            for allowed_role in roles:
                if allowed_role.is_equal(user):
                    return func(*arg, **kwargs)
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")
        return validate_permission_scope
    return inner_permission
