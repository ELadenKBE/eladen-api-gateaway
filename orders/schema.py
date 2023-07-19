import graphene

from app.authorization import grant_authorization
from orders.order_service import OrderType, OrderService
from app.permissions import permission, Admin, User
from goods.schema import GoodType

order_service = OrderService()


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType, searched_id=graphene.Int())

    @grant_authorization
    @permission(roles=[Admin, User])
    def resolve_orders(self, info, **kwargs):
        """
        TODO add docstring


        :param info:
        :param kwargs:
        :return:
        """
        return order_service.get_orders(info=info)


class CreateOrder(graphene.Mutation):
    id = graphene.Int()
    time_of_order = graphene.String()
    items_price = graphene.Float()
    delivery_price = graphene.Float()
    user_id = graphene.Int()
    delivery_status = graphene.String()
    payment_status = graphene.String()
    goods = graphene.List(GoodType)
    delivery_address = graphene.String()

    class Arguments:
        time_of_order = graphene.String()
        delivery_address = graphene.String()

    @grant_authorization
    @permission(roles=[Admin, User])
    def mutate(self, info, **kwargs):
        """
        TODO finish docs

        :param info:
        :return:
        """
        order = order_service.create_order(info)

        return CreateOrder(
            id=order.id,
            delivery_address=order.delivery_address,
            items_price=order.items_price,
            delivery_price=order.delivery_price,
            time_of_order=order.time_of_order,
            user_id=order.user_id,
            delivery_status=order.delivery_status,
            payment_status=order.payment_status,
            goods=order.goods
        )


class UpdateOrder(graphene.Mutation):
    id = graphene.Int()
    time_of_order = graphene.String()
    delivery_address = graphene.String()
    items_price = graphene.Float()
    delivery_price = graphene.Float()
    user_id = graphene.Int()
    delivery_status = graphene.String()
    payment_status = graphene.String()

    class Arguments:
        order_id = graphene.Int(required=True)
        delivery_address = graphene.String()

    @grant_authorization
    @permission(roles=[Admin])
    def mutate(self, info, **kwargs):
        """
        TODO add docs

        :param info:
        """
        order = order_service.update_order(info)

        return UpdateOrder(
            id=order.id,
            delivery_address=order.delivery_address,
            items_price=order.items_price,
            delivery_price=order.delivery_price,
            time_of_order=order.time_of_order,
            user_id=order.user_id,
            delivery_status=order.delivery_status,
            payment_status=order.payment_status
        )


class DeleteOrder(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        order_id = graphene.Int(required=True)

    @grant_authorization
    @permission(roles=[Admin])
    def mutate(self, info, order_id):
        """
        TODO add docs

        :param info:
        :param order_id:
        :return:
        """
        order_service.delete_order(info)
        return DeleteOrder(
            id=order_id
        )


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
