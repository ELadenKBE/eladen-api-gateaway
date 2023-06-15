import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from app.permissions import permission, Admin, Seller, All
from category.models import Category
from category.repository import CategoryRepository


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType,
                               search=graphene.String(),
                               searched_id=graphene.String(),
                               )

    @permission(roles=[All])
    def resolve_categories(self, info, search=None, searched_id=None, **kwargs):
        """
        Return all elements if search arguments are not given.

        :param info: request context information
        :param search: searches in title
        :param searched_id: id of searched item
        :return:
        """
        if search:
            return CategoryRepository.\
                                get_items_by_filter(Q(title__icontains=search))
        if searched_id:
            return CategoryRepository.get_by_id(searched_id)
        return CategoryRepository.get_all_items()


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String(required=True)

    class Arguments:
        title = graphene.String()

    @permission(roles=[Admin])
    def mutate(self, info, title):
        """
        TODO add docs

        :param info:
        :param title:
        :return:
        """
        created_category = CategoryRepository.create_item(title=title)

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

    @permission(roles=[Admin])
    def mutate(self, info, id, title):
        """
        TODO add docs

        :param info:
        :param id:
        :param title:
        :return:
        """
        category = CategoryRepository.update_item(item_id=id, title=title)

        return UpdateCategory(
            id=category.id,
            title=category.title
        )


class DeleteCategory(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @permission(roles=[Admin])
    def mutate(self, info, id):
        """
        TODO add docs

        :param info:
        :param id:
        :return:
        """
        category = CategoryRepository.delete_item(info=info, searched_id=id)

        return CreateCategory(
            id=id,
            title=category.title
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
