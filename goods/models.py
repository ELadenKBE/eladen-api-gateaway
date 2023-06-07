from django.core.validators import MinValueValidator
from django.db import models
from graphql import GraphQLResolveInfo

from app.errors import UnauthorizedError
from category.models import Category
from users.models import ExtendedUser


# Create your models here.


class Good(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    title = models.CharField(max_length=256)
    seller = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=5000, null=True, blank=True)
    manufacturer = models.CharField(max_length=256, null=True, blank=True)
    amount = models.IntegerField(blank=False,
                                 default=99,
                                 validators=[MinValueValidator(0)],
                                 null=True)

    def delete_with_permission(self, info: GraphQLResolveInfo):
        user: ExtendedUser = info.context.user
        if user.is_admin():
            self.delete()
        elif user.is_seller() and self.seller == user:
            self.delete()
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")

    def update_with_permission(self,
                               info,
                               title,
                               description,
                               address,
                               price,
                               image,
                               manufacturer,
                               amount):
        user: ExtendedUser = info.context.user
        if user.is_admin() or user == self.seller:
            if manufacturer is not None:
                self.manufacturer = manufacturer
            if title is not None:
                self.title = title
            if description is not None:
                self.description = description
            if address is not None:
                self.address = address
            if price is not None:
                self.price = price
            if image is not None:
                self.image = image
            if amount is not None:
                self.amount = amount
            self.save()
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")

    @staticmethod
    def create_with_permission(info, title, description, address,
                               category_id, price, image, manufacturer, amount):
        user: ExtendedUser = info.context.user or None
        if user.is_seller() or user.is_admin():
            good = Good(title=title,
                        description=description,
                        address=address,
                        category=Category.objects.get(id=category_id),
                        seller=user,
                        price=price,
                        image=image,
                        manufacturer=manufacturer,
                        amount=amount
                        )
            good.save()
            return good
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")

