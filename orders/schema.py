import graphene
from graphene_django import DjangoObjectType

from .models import Order


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()
