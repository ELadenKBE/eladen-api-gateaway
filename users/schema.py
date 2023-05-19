from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from users.models import ExtendedUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return ExtendedUser.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.Int(required=True)

    def mutate(self, info, username, password, email, role):
        user = ExtendedUser(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
