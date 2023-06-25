import graphene

from app.permissions import permission, Admin, Seller, User
from app.product_service import ProductService, GoodsListTransferType
from category.schema import CategoryType
from goods.schema import GoodType
from users.schema import UserType
from .models import GoodsList

product_service = ProductService()


class Query(graphene.ObjectType):
    goods_lists = graphene.List(GoodsListTransferType,
                                search=graphene.String(),
                                searched_id=graphene.Int())

    @permission(roles=[Admin, Seller, User])
    def resolve_goods_lists(self, info, **kwargs):
        """
        TODO write docstring

        :param info: request context
        :param kwargs:
        :return:
        """
        result = product_service.get_good_lists(info=info)
        return result


class CreateGoodsList(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()

    @permission(roles=[Admin, Seller, User])
    def mutate(self, info, title):
        """
        TODO add doctrings
        :param info:
        :param title:
        :return:
        """
        good_list: GoodsList = product_service.create_goods_list(info)

        return CreateGoodsList(
            id=good_list.id,
            title=good_list.title,
            user=good_list.user
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

    @permission(roles=[Admin, User])
    def mutate(self, info, good_id):
        good = GoodType.product_service.add_good_to_cart(info)
        return AddGoodToCart(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
        )


class CleanGoodsList(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        list_id = graphene.Int()

    @permission(roles=[Admin, User, Seller])
    def mutate(self, info, list_id):

        goods_list = product_service.clean_goods_list(info)

        return CleanGoodsList(
            id=goods_list.id,
            title=goods_list.title
        )


class UpdateGoodsList(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        list_id = graphene.Int()
        title = graphene.String()

    @permission(roles=[Admin, Seller, User])
    def mutate(self, info, list_id, title):
        """
        TODO add docs

        :param info:
        :param list_id:
        :param title:
        :return:
        """

        goods_list = product_service.update_goods_list(info=info)

        return UpdateGoodsList(
            id=goods_list.id,
            title=goods_list.title
        )


class DeleteGoodsList(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        list_id = graphene.Int(required=True)

    @permission(roles=[Admin, Seller, User])
    def mutate(self, info, list_id):
        """
        TODO add docs

        :param info:
        :param list_id:
        :return:
        """
        product_service.delete_goods_list(info)
        return DeleteGoodsList(
            id=list_id
        )


class Mutation(graphene.ObjectType):
    create_goods_list = CreateGoodsList.Field()
    add_good_to_cart = AddGoodToCart.Field()
    clean_goods_list = CleanGoodsList.Field()
    update_goods_list = UpdateGoodsList.Field()
    delete_goods_list = DeleteGoodsList.Field()
