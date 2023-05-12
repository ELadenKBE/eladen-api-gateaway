import graphene
from graphene_django import DjangoObjectType

from category.schema import CategoryType
from users.schema import UserType
from .models import Good


class GoodType(DjangoObjectType):
    class Meta:
        model = Good


class Query(graphene.ObjectType):
    goods = graphene.List(GoodType)

    def resolve_goods(self, info, **kwargs):
        return Good.objects.all()


class CreateGood(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    seller = graphene.Field(UserType)
    address = graphene.String()
    category = graphene.Field(CategoryType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        address = graphene.String()
        category = graphene.Field(CategoryType)

    def mutate(self, info, title, description, address, category):
        seller = info.context.user or None

        good = Good(title=title,
                    description=description,
                    address=address,
                    category=category,
                    seller=seller
                    )
        good.save()

        return CreateGood(
            id=good.id,
            description=good.description,
            address=good.address,
            category=good.category,
            seller=good.seller
        )


#4
class Mutation(graphene.ObjectType):
    create_good = CreateGood.Field()
