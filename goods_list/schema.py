import graphene
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
from app.permissions import permission, Admin, Seller, User
from category.schema import CategoryType
from goods.models import Good
from goods.schema import GoodType
from users.schema import UserType
from .models import GoodsList


class GoodsListType(DjangoObjectType):
    class Meta:
        model = GoodsList


class Query(graphene.ObjectType):
    goods_lists = graphene.List(GoodsListType,
                                search=graphene.String(),
                                searched_id=graphene.Int(), )

    @permission(roles=[Admin, Seller, User])
    def resolve_goods_lists(self, info,
                            searched_id=None,
                            search=None,
                            **kwargs):
        """
        TODO write docstring

        :param info: request context
        :param searched_id:
        :param search:
        :param kwargs:
        :return:
        """
        if search:
            return GoodsList.get_all_filtered_with_permission(info, search)
        if searched_id:
            return [GoodsList.get_by_id_with_permission(info,
                                                        search_id=searched_id)]
        return GoodsList.get_all_with_permission(info)


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
        """
        TODO add doctrings

        :param info:
        :param good_id:
        :return:
        """
        user = info.context.user or None
        if user is None:
            raise UnauthorizedError("Unauthorized access!")
        good = Good.objects.get(id=good_id)
        cart_list: GoodsList = GoodsList.objects.filter(user=user,
                                                        title="cart").first()
        cart_list.goods.add(good)
        cart_list.save()

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
    goods = graphene.List(GoodType)

    class Arguments:
        list_id = graphene.Int()

    @permission(roles=[Admin, User, Seller])
    def mutate(self, info, list_id):
        """
        TODO add doctrings

        :param info:
        :param list_id:
        :return:
        """
        goods_list = GoodsList.objects.filter(id=list_id).first()
        goods_list.clean_goods_with_permission(info)

        return CleanGoodsList(
            id=goods_list.id,
            title=goods_list.title,
            goods=goods_list.goods.all()
        )


class UpdateList(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        list_id = graphene.Int()
        title = graphene.String()

    @permission(roles=[Admin, Seller])
    def mutate(self, info, list_id, title):
        goods_list: GoodsList = GoodsList.objects.filter(id=list_id).first()
        goods_list.update_with_permission(info, title)

        return UpdateList(
            id=goods_list.id,
            title=goods_list.title
        )


class Mutation(graphene.ObjectType):
    create_goods_list = CreateGoodsList.Field()
    add_good_to_cart = AddGoodToCart.Field()
    clean_goods_list = CleanGoodsList.Field()
    update_goods_list = UpdateList.Field()
