import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from app.permissions import permission, All, Seller, Admin
from category.models import Category
from category.schema import CategoryType
from users.schema import UserType
from .models import Good
from .repository import GoodRepository


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
                             Q(description__icontains=search))
            return GoodRepository.get_items_by_filter(search_filter)
        if searched_id:
            return GoodRepository.get_by_id(searched_id)
        return GoodRepository.get_all_items()


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
    amount = graphene.Int()

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        address = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        price = graphene.Float(required=True)
        image = graphene.String()
        manufacturer = graphene.String(required=True)
        amount = graphene.Int()

    @permission(roles=[Admin, Seller])
    def mutate(self,
               info,
               title,
               address,
               category_id,
               price,
               manufacturer,
               amount=None,
               description=None,
               image=None):
        """
        TODO add docs

        :param info:
        :param title:
        :param address:
        :param category_id:
        :param price:
        :param manufacturer:
        :param amount:
        :param description:
        :param image:
        :return:
        """
        good = GoodRepository.create_item(info=info,
                                          title=title,
                                          address=address,
                                          category_id=category_id,
                                          price=price,
                                          manufacturer=manufacturer,
                                          amount=amount,
                                          description=description,
                                          image=image)

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
    amount = graphene.Int()

    class Arguments:
        good_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        price = graphene.Float()
        image = graphene.String()
        manufacturer = graphene.String()
        amount = graphene.Int()

    @permission(roles=[Admin, Seller])
    def mutate(self, info, good_id,
               title=None,
               description=None,
               address=None,
               price=None,
               image=None,
               manufacturer=None,
               amount=None,
               ):
        """
        TODO add docs

        :param info:
        :param good_id:
        :param title:
        :param description:
        :param address:
        :param price:
        :param image:
        :param manufacturer:
        :param amount:
        :return:
        """
        # TODO should implement not found?
        good = Good.objects.filter(id=good_id).first()
        good.update_with_permission(info,
                                    title,
                                    description,
                                    address,
                                    price,
                                    image,
                                    manufacturer,
                                    amount)

        return UpdateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
            image=good.image,
            amount=good.amount
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
    amount = graphene.Int()

    class Arguments:
        category_id = graphene.Int()
        good_id = graphene.Int()

    @permission(roles=[Admin, Seller])
    def mutate(self, category_id, good_id):
        """
        TODO add docs

        :param category_id:
        :param good_id:
        :return:
        """
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
            image=good.image,
            amount=good.amount
        )


class DeleteGood(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        id = graphene.Int(required=True)

    @permission(roles=[Admin, Seller])
    def mutate(self, info, id):
        """
        TODO add docs

        :param info:
        :param id:
        :return:
        """
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
