import graphene

from app.authorization import grant_authorization
from app.permissions import permission, Admin, All
from app.product_service import ProductService, CategoryType

product_service = ProductService()


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType,
                               search=graphene.String(),
                               searched_id=graphene.String(),
                               )

    @grant_authorization
    @permission(roles=[All])
    def resolve_categories(self, info, **kwargs):
        """
        Return all elements if search arguments are not given.

        :param info: request context information
        :return:
        """
        return product_service.get_categories(info)


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String(required=True)

    class Arguments:
        title = graphene.String()

    @grant_authorization
    @permission(roles=[Admin])
    def mutate(self, info, title):
        """
        TODO add docs

        :param info:
        :param title:
        :return:
        """
        created_category = product_service.create_category(info)

        return CreateCategory(
            id=created_category.id,
            title=created_category.title
        )


class UpdateCategory(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()

    @grant_authorization
    @permission(roles=[Admin])
    def mutate(self, info, **kwargs):
        """
        TODO add docs

        :param info:
        :param id:
        :param title:
        :return:
        """
        category = product_service.update_category(info=info)

        return UpdateCategory(
            id=category.id,
            title=category.title
        )


class DeleteCategory(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @grant_authorization
    @permission(roles=[Admin])
    def mutate(self, info, id):
        """
        TODO add docs

        :param info:
        :param id:
        :return:
        """
        product_service.delete_category(info)

        return CreateCategory(
            id=id
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
