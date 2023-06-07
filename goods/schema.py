import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

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
                          searched_id=graphene.Int(),
                          search=graphene.String(),
                          )

    @permission(roles=[All])
    def resolve_goods(self, info, search=None, searched_id=None, **kwargs):
        """
        Return all elements if search arguments are not given.

        :param info: request context information
        :param search: searches in title and description
        :param searched_id: id of searched item
        :return: collection of items
        """
        if search:
            search_filter = (Q(title__icontains=search) |
                             Q(description__icontains=search)
                             )
            return Category.objects.filter(search_filter).all()
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
    image = graphene.String()
    manufacturer = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        address = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        price = graphene.Float(required=True)
        image = graphene.String()
        manufacturer = graphene.String(required=True)

    @permission(roles=[Admin, Seller])
    def mutate(self,
               info,
               title,
               address,
               category_id,
               price,
               manufacturer,
               description=None,
               image=None):
        good = Good.create_with_permission(info,
                                           title,
                                           description,
                                           address,
                                           category_id,
                                           price,
                                           image,
                                           manufacturer)

        return CreateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller,
            price=good.price,
            image=good.image,
            manufacturer=good.manufacturer
        )


class UpdateGood(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)
    image = graphene.String()
    manufacturer = graphene.String()

    class Arguments:
        good_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        price = graphene.Float()
        image = graphene.String()
        manufacturer = graphene.String()

    @permission(roles=[Admin, Seller])
    def mutate(self, info, good_id,
               title=None,
               description=None,
               address=None,
               price=None,
               image=None,
               manufacturer=None):
        # TODO should implement not found?
        good = Good.objects.filter(id=good_id).first()
        good.update_with_permission(info,
                                    title,
                                    description,
                                    address,
                                    price,
                                    image,
                                    manufacturer)

        return UpdateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
            image=good.image
        )


class ChangeCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)
    image = graphene.String()
    manufacturer = graphene.String()

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
            price=good.price,
            image=good.image
        )


class DeleteGood(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        id = graphene.Int(required=True)

    @permission(roles=[Admin, Seller])
    def mutate(self, info, id):
        good = Good.objects.filter(id=id).first()
        good.delete_with_permission(info)
        return DeleteGood(
            id=id
        )


class Mutation(graphene.ObjectType):
    create_good = CreateGood.Field()
    change_category = ChangeCategory.Field()
    update_good = UpdateGood.Field()
    delete_good = DeleteGood.Field()
