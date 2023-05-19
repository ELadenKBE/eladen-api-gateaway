from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # roles are: 1-user. 2-seller. 3-admin
    role = models.IntegerField(blank=False, default=1, validators=[
        MinValueValidator(1), MaxValueValidator(3)])
    address = models.CharField(max_length=256)

    def is_user(self):
        return self.role == 1

    def is_seller(self):
        return self.role == 2

    def is_admin(self):
        return self.role == 3
