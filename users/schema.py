from django.contrib.auth import get_user_model

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from app.permissions import permission, Admin, Anon, Seller, User
from goods_list.models import GoodsList
from users.models import ExtendedUser


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


class Query(graphene.ObjectType):
    users = graphene.List(UserType,
                          search=graphene.String(),
                          searched_id=graphene.Int())

    def resolve_users(self, info, searched_id=None, search=None, **kwargs):
        if search:
            search_filter = (Q(username__icontains=search))
            return [ExtendedUser.objects.filter(search_filter).first()]
        if searched_id:
            return [ExtendedUser.objects.filter(id=searched_id).first()]
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

    @permission(roles=[Admin, Anon])
    def mutate(self,
               info,
               username,
               password,
               email,
               role,
               address=None,
               firstname=None,
               lastname=None):
        validate_role(role)
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
            cart_list = GoodsList(
                title="cart",
                user=user
            )
            cart_list.save()
        if user.is_seller():
            goods_to_sell = GoodsList(
                title="goods to sell",
                user=user
            )
            goods_to_sell.save()
        return CreateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            address=user.address,
            lastname=user.lastname,
            firstname=user.firstname
        )


class UpdateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    role = graphene.Int()
    address = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()

    class Arguments:
        user_id = graphene.Int(required=True)
        email = graphene.String()
        address = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()

    @permission(roles=[Admin, Seller, User])
    def mutate(self,
               info,
               user_id,
               email,
               address=None,
               firstname=None,
               lastname=None):
        user: ExtendedUser = ExtendedUser.objects.filter(id=user_id).first()
        user.update_with_permissions(info,
                                     email,
                                     address,
                                     firstname,
                                     lastname)
        return UpdateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            address=user.address,
            firstname=user.firstname,
            lastname=user.lastname
        )


def validate_role(role):
    if role < 1 or role > 3:
        raise ValueError("role is not defined")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
