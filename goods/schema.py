import graphene
from graphene_django import DjangoObjectType

from .models import Good


class GoodType(DjangoObjectType):
    class Meta:
        model = Good


class Query(graphene.ObjectType):
    goods = graphene.List(GoodType)

    def resolve_goods(self, info, **kwargs):
        return Good.objects.all()
