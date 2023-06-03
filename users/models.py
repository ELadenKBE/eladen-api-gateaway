from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import AbstractUser

from app.errors import UnauthorizedError


class ExtendedUser(AbstractUser):
    # roles are: 1-user. 2-seller. 3-admin
    role = models.IntegerField(blank=False, default=1, validators=[
        MinValueValidator(1), MaxValueValidator(3)])
    address = models.CharField(max_length=256, null=True)
    firstname = models.CharField(max_length=256, null=True)
    lastname = models.CharField(max_length=256, null=True)

    def is_user(self):
        return self.role == 1

    def is_seller(self):
        return self.role == 2

    def is_admin(self):
        return self.role == 3

    def update_with_permissions(self, info, email, address,
                                firstname, lastname):
        """
        TODO write docs

        :param info:
        :param email:
        :param address:
        :param firstname:
        :param lastname:
        :return:
        """
        user: ExtendedUser = info.context.user
        if ((user.is_user() or user.is_seller()) and self == user)\
                or user.is_admin():
            self.email = email
            self.address = address
            self.firstname = firstname
            self.lastname = lastname
            self.save()
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")

    def delete_with_permission(self, info):
        """
        TODO add docstring

        :param info:
        :return:
        """
        user: ExtendedUser = info.context.user
        if user.is_admin():
            self.delete()
        elif (user.is_seller() or user.is_user()) and self == user:
            self.delete()
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")
