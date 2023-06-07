from django.db import models
from django.db.models import QuerySet

from app.errors import UnauthorizedError
from users.models import ExtendedUser


class Order(models.Model):
    time_of_order = models.DateTimeField()
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=256)
    items_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_status = models.CharField(max_length=256)
    payment_status = models.CharField(max_length=256)

    @staticmethod
    def get_all_orders_with_permission(info) -> QuerySet:
        """
        TODO add docstr

        :param info:
        :return:
        """
        user: ExtendedUser = info.context.user
        if user.is_user():
            return Order.objects.filter(user=user).all()
        if user.is_admin():
            return Order.objects.all()

    @staticmethod
    def get_by_id_with_permission(info, searched_id) -> QuerySet:
        """
        TODO add strings

        :param info:
        :param searched_id:
        :return:
        """
        user: ExtendedUser = info.context.user
        if user.is_user():
            return Order.objects.filter(user=user, id=searched_id).first()
        if user.is_admin():
            return Order.objects.filter(id=searched_id).first()

    def update_with_permission(self, info, delivery_address, items_price,
                               delivery_price):
        """
        :param info:
        :param delivery_address:
        :param items_price:
        :param delivery_price:
        :return:
        """
        user: ExtendedUser = info.context.user
        if user.is_user() and self.user == user or user.is_admin():
            if delivery_address is not None:
                self.delivery_address = delivery_address
            if items_price is not None:
                self.items_price = items_price
            if delivery_price is not None:
                self.delivery_price = delivery_price
            self.save()
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")
