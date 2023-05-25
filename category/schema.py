import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from app.permissions import permission, Admin, Seller, All
from category.models import Category


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
        if search:
            search_filter = (Q(title__icontains=search))
            return Category.objects.filter(search_filter)
        if searched_id:
            data_to_return = Category.objects.get(id=searched_id)
            return [data_to_return]
        return Category.objects.all()


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String(required=True)

    class Arguments:
        title = graphene.String()

    @permission(roles=[Admin])
    def mutate(self, info, title):
        category = Category(title=title)
        category.save()

        return CreateCategory(
            id=category.id,
            title=category.title
        )


class UpdateCategory(graphene.Mutation):
    id = graphene.Int(required=True)
    title = graphene.String()

    class Arguments:
        id = graphene.Int()
        title = graphene.String()

    @permission(roles=[Admin])
    def mutate(self, info, id, title):
        category = Category.objects.get(id=id)
        category.title = title
        category.save()

        return UpdateCategory(
            id=category.id,
            title=category.title
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
