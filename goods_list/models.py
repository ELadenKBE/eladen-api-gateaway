from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Q

from app.errors import UnauthorizedError
from goods.models import Good
from users.models import ExtendedUser


class GoodsList(models.Model):
    title = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(ExtendedUser,
                             on_delete=models.CASCADE,
                             blank=False)
    goods = models.ManyToManyField(Good)
