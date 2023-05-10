import graphene
from graphene_django import DjangoObjectType

from category.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    goods = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

