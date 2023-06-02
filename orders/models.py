from django.db import models

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
    def get_all_orders_with_permission(info):
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
