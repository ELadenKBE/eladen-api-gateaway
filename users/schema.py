from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

from goods_list.models import GoodsList
from users.models import ExtendedUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return ExtendedUser.objects.all()


class CreateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    role = graphene.Int(required=True)
    address = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.Int(required=True)
        address = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()

    def mutate(self, info, username, password, email, role, address, firstname,
               lastname):
        self.validate_role(role)
        user = ExtendedUser(
            username=username,
            email=email,
            role=role,
            address=address,
            lastname=lastname,
            firstname=firstname
        )
        user.set_password(password)
        user.save()
        if user.is_user():
            liked_list = GoodsList(
                title="liked",
                user=user
            )
            liked_list.save()
            cart_list = GoodsList(
                title="liked",
                user=user
            )
            cart_list.save()
        if user.is_seller():
            goods_to_sell = GoodsList(
                title="goods to sell",
                user=user
            )
            goods_to_sell.save()
        return CreateUser(user=user)

    def validate_role(self, role):
        if role < 1 or role > 2:
            raise ValueError("role ")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
