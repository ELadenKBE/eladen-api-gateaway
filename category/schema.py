import graphene
from graphene_django import DjangoObjectType

from category.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()


# TODO add good to category
class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title,):
        seller = info.context.user or None
        #TODO check if user is seller or admin
        category = Category(title=title)
        category.save()

        return CreateCategory(
            id=category.id,
            title=category.title
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
