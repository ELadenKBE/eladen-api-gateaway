import graphene
from graphene_django import DjangoObjectType

from .models import GoodsList


class GoodsListType(DjangoObjectType):
    class Meta:
        model = GoodsList


class Query(graphene.ObjectType):
    goods_lists = graphene.List(GoodsListType)

    def resolve_goods_lists(self, info, **kwargs):
        return GoodsList.objects.all()
