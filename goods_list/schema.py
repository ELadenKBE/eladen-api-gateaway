import graphene
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
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

# TODO add item to cart
# TODO add item to liked


class Mutation(graphene.ObjectType):
    create_goods_list = CreateGoodsList.Field()
