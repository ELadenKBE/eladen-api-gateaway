from django.db import models

from category.models import Category


# Create your models here.


class Good(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    title = models.CharField(max_length=256)
    #TODO seller_id
    address = models.CharField(max_length=256)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
