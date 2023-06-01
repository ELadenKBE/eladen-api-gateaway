from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Q

from goods.models import Good
from users.models import ExtendedUser


class GoodsList(models.Model):
    title = models.CharField(max_length=256, blank=False)
    user = models.ForeignKey(ExtendedUser,
                             on_delete=models.CASCADE,
                             blank=False)
    goods = models.ManyToManyField(Good)

    @staticmethod
    def get_all_with_permission(info) -> QuerySet:
        user: ExtendedUser = info.context.user
        if user.is_user() or user.is_seller():
            return GoodsList.objects.filter(user=user).all()
        if user.is_admin():
            return GoodsList.objects.all()

    @staticmethod
    def get_all_filtered_with_permission(info, search) -> QuerySet:
        user: ExtendedUser = info.context.user
        search_filter = (Q(title__icontains=search))
        if user.is_user() or user.is_seller():
            return GoodsList.objects.filter(search_filter & user == user).all()
        else:
            return GoodsList.objects.filter(search_filter).all()

