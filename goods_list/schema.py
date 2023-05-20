import graphene
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
from category.schema import CategoryType
from goods.models import Good
from users.schema import UserType
from .models import GoodsList


class GoodsListType(DjangoObjectType):
    class Meta:
        model = GoodsList


class Query(graphene.ObjectType):
    goods_lists = graphene.List(GoodsListType)

    def resolve_goods_lists(self, info, **kwargs):
        return GoodsList.objects.all()


class CreateGoodsList(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title):
        user = info.context.user or None
        if user is None:
            raise UnauthorizedError("Unauthorized access!")
        good_list = GoodsList(title=title, user=user)
        good_list.save()

        return CreateGoodsList(
            id=good_list.id,
            title=good_list.title,
            user=user
        )


class AddGoodToLiked(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)

    class Arguments:
        good_id = graphene.Int()

    def mutate(self, info, good_id):
        user = info.context.user or None
        if user is None:
            raise UnauthorizedError("Unauthorized access!")
        good = Good.objects.get(id=good_id)
        liked_list: GoodsList = GoodsList.objects.filter(user=user,
                                                         title="liked")
        liked_list.goods.add(good)
        liked_list.save()

        return AddGoodToLiked(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
        )


class AddGoodToCart(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    price = graphene.Float()
    category = graphene.Field(CategoryType)

    class Arguments:
        good_id = graphene.Int()

    def mutate(self, info, good_id):
        user = info.context.user or None
        if user is None:
            raise UnauthorizedError("Unauthorized access!")
        good = Good.objects.get(id=good_id)
        liked_list: GoodsList = GoodsList.objects.filter(user=user,
                                                         title="cart")
        liked_list.goods.add(good)
        liked_list.save()

        return AddGoodToLiked(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
        )


class Mutation(graphene.ObjectType):
    create_goods_list = CreateGoodsList.Field()
    add_good_to_liked = AddGoodToLiked.Field()
    add_good_to_cart = AddGoodToCart.Field()
