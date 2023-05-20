import graphene
import jwt
from graphene_django import DjangoObjectType

from app.errors import UnauthorizedError
from category.models import Category
from users.models import ExtendedUser


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        user: ExtendedUser = info.context.user or None
        # encoded_jwt = info.context.META.get('HTTP_AUTHORIZATION')
        # print(jwt.decode(encoded_jwt, algorithms=["HS256"]))
        if user.is_user():
            raise UnauthorizedError("Unauthorised")
        return Category.objects.all()


# TODO add good to category
class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        title = graphene.String()

    def mutate(self, info, title):
        user: ExtendedUser = info.context.user or None
        category = Category(title=title)
        category.save()

        return CreateCategory(
            id=category.id,
            title=category.title
        )


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
