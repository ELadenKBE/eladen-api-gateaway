from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    time_of_order = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=256)
    items_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_status = models.CharField(max_length=256)
    payment_status = models.CharField(max_length=256)
