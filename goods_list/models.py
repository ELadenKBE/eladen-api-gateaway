from django.contrib.auth.models import User
from django.db import models

from goods.models import Good


class GoodsList(models.Model):
    title = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Good)
