import graphene

from app.authorization import grant_authorization
from app.permissions import permission, All, Seller, Admin
from app.product_service import ProductService, GoodType
from category.schema import CategoryType
from users.schema import UserType

product_service = ProductService()


class Query(graphene.ObjectType):
    goods = graphene.List(GoodType,
                          searched_id=graphene.Int(),
                          search=graphene.String(),
                          )

    @grant_authorization
    @permission(roles=[All])
    def resolve_goods(self, info, **kwargs):
        """
        Return all elements if search arguments are not given.

        :param info: request context information
        :return: collection of items
        """
        return product_service.get_goods(info=info)


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
    url = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        address = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        price = graphene.Float(required=True)
        image = graphene.String()
        manufacturer = graphene.String(required=True)
        amount = graphene.Int()
        url = graphene.String()

    @grant_authorization
    @permission(roles=[Admin, Seller])
    def mutate(self, info, **kwargs):
        """
        TODO add docs

        :param info:
        :return:
        """
        good = product_service.create_good(info=info)

        return CreateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller,
            price=good.price,
            image=good.image,
            manufacturer=good.manufacturer,
            url=good.url
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
    url = graphene.String()

    class Arguments:
        good_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        price = graphene.Float()
        image = graphene.String()
        manufacturer = graphene.String()
        amount = graphene.Int()
        url = graphene.String()

    @grant_authorization
    @permission(roles=[Admin, Seller])
    def mutate(self, info, **kwargs):
        """
        TODO add docs

        :param info:
        :return:
        """
        # TODO should implement not found?
        # TODO url not null??
        good = product_service.update_good(info=info)

        return UpdateGood(
            id=good.id,
            title=good.title,
            description=good.description,
            seller=good.seller,
            address=good.address,
            price=good.price,
            category=good.category,
            image=good.image,
            amount=good.amount,
            url=good.url
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
    url = graphene.String()

    class Arguments:
        category_id = graphene.Int()
        good_id = graphene.Int()

    @grant_authorization
    @permission(roles=[Admin, Seller])
    def mutate(self, info, category_id, good_id):
        """
        TODO add docs

        :param info:
        :param category_id:
        :param good_id:
        :return:
        """
        good = product_service.change_goods_category(info)

        return ChangeCategory(
            id=good.id,
            title=good.title,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller,
            price=good.price,
            image=good.image,
            amount=good.amount,
            url=good.url
        )


class DeleteGood(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        id = graphene.Int(required=True)

    @grant_authorization
    @permission(roles=[Admin, Seller])
    def mutate(self, info, id):
        """
        TODO add docs

        :param info:
        :param id:
        :return:
        """
        # TODO fix delete as admin
        product_service.delete_good(info)
        return DeleteGood(
            id=id
        )


class Mutation(graphene.ObjectType):
    create_good = CreateGood.Field()
    change_category = ChangeCategory.Field()
    update_good = UpdateGood.Field()
    delete_good = DeleteGood.Field()
