from django.db import models

# Create your models here.


class Good(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    title = models.CharField(max_length=256)
    #TODO seller_id
    address = models.CharField(max_length=256)
    #TODO category_ids
    price = models.DecimalField(max_digits=6, decimal_places=2)
