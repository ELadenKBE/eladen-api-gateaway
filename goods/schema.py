import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
from app.permissions import permission, All, Seller, Admin
from category.models import Category
from category.schema import CategoryType
from users.schema import UserType
from .models import Good


class GoodType(DjangoObjectType):
    class Meta:
        model = Good


class Query(graphene.ObjectType):
    goods = graphene.List(GoodType,
                          searched_id=graphene.String(),
                          search=graphene.String(),
                          )

    @permission(roles=[All])
    def resolve_goods(self, info, search=None,  searched_id=None, **kwargs):
        """
        Return all elements if search arguments are not given.

        :param info: request context information
        :param search: searches in title and description
        :param searched_id: id of searched item
        :return: collection of items
        """
        if search:
            search_filter = (Q(title__icontains=search)|
                             Q(description__icontains=search)
                             )
            return Category.objects.filter(search_filter)
        if searched_id:
            data_to_return = Good.objects.get(id=searched_id)
            return [data_to_return]
        return Good.objects.all()


class CreateGood(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        category_id = graphene.Int()
        price = graphene.Float()

    @permission(roles=[Admin, Seller])
    def mutate(self, info, title, description, address, category_id, price):
        seller = info.context.user or None
        if seller is None:
            raise UnauthorizedError("Unauthorized access!")
        good = Good(title=title,
                    description=description,
                    address=address,
                    category=Category.objects.get(id=category_id),
                    seller=seller,
                    price=price
                    )
        good.save()

        return CreateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller,
            price=good.price
        )


class UpdateGood(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)

    class Arguments:
        good_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        price = graphene.Float()

    @permission(roles=[Admin, Seller])
    # TODO: seller allowed to update only his goods
    def mutate(self, info, good_id, title, description, address, price):
        # TODO should implement not found?
        good = Good.objects.filter(id=good_id).first()
        good.title = title
        good.description = description
        good.address = address
        good.price = price
        good.save()

        return UpdateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category
        )


class ChangeCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)

    class Arguments:
        category_id = graphene.Int()
        good_id = graphene.Int()

    @permission(roles=[Admin, Seller])
    def mutate(self, category_id, good_id):
        category = Category.objects.get(id=category_id)
        good = Good.objects.get(id=good_id)
        good.category = category
        good.save()

        return ChangeCategory(
            id=good.id,
            title=good.title,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller,
            price=good.price
        )


class Mutation(graphene.ObjectType):
    create_good = CreateGood.Field()
    change_category = ChangeCategory.Field()
    update_good = UpdateGood.Field()
