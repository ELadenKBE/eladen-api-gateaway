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
            filter = (
                    Q(title__icontains=search)
            )
            return Category.objects.filter(filter)
        if searched_id:
            Category.objects.get(id=searched_id)
        return Category.objects.all()


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        title = graphene.String()

    @permission(roles=[Admin, Seller])
    def mutate(self, info, title):
        category = Category(title=title)
        category.save()

        return CreateCategory(
            id=category.id,
            title=category.title
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
