import graphene
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
from .models import Order


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()


# TODO change delivery status
# TODO change payment status
class CreateOrder(graphene.Mutation):
    id = graphene.Int()
    time_of_order = graphene.String()
    delivery_address = graphene.String()
    items_price = graphene.Float()
    delivery_price = graphene.Float()

    class Arguments:
        time_of_order = graphene.String()
        delivery_address = graphene.String()
        items_price = graphene.Float()
        delivery_price = graphene.Float()

    def mutate(self, info,
               time_of_order,
               delivery_address,
               items_price,
               delivery_price):
        user = info.context.user or None
        if user is None:
            raise UnauthorizedError("Unauthorized access!")
        order = Order(time_of_order=time_of_order,
                      delivery_address=delivery_address,
                      items_price=items_price,
                      delivery_price=delivery_price,
                      user=user)
        order.save()

        return CreateOrder(
            id=order.id,
            delivery_address=order.delivery_address,
            items_price=order.items_price,
            delivery_price=order.delivery_price,
            title=order.title,
            user=user
        )


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
