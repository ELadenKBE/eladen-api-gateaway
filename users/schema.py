import graphene
from graphene_django import DjangoObjectType

from app.authorization import grant_authorization
from app.permissions import permission, Admin, Seller, User
from users.models import ExtendedUser
from users.user_service import UserService


class UserType(DjangoObjectType):
    class Meta:
        model = ExtendedUser


user_service = UserService()


class Query(graphene.ObjectType):
    users = graphene.List(UserType,
                          search=graphene.String(),
                          searched_id=graphene.Int())

    @grant_authorization
    def resolve_users(self, info, searched_id=None, search=None, **kwargs):
        """
        TODO add docs

        :param info:
        :param searched_id:
        :param search:
        :param kwargs:
        :return:
        """
        return user_service.get_users(info=info)


class CreateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    role = graphene.Int(required=True)
    address = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    image = graphene.String()
    sub = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        role = graphene.Int(required=True)
        address = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()
        image = graphene.String()
        sub = graphene.String(required=True)

#    @grant_authorization
 #   @permission(roles=[Admin, User, Seller])
    def mutate(self, info, **kwargs):
        """
        TODO add docs

        :param info:
        :return:
        """
        user = user_service.create_user(info)
        return CreateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            address=user.address,
            lastname=user.lastName,
            firstname=user.firstName,
            image=user.image,
            sub=user.sub
        )


class UpdateUser(graphene.Mutation):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    role = graphene.Int()
    address = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    image = graphene.String()

    class Arguments:
        user_id = graphene.Int(required=True)
        email = graphene.String()
        address = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()
        image = graphene.String()

    @grant_authorization
    @permission(roles=[Admin, Seller, User])
    def mutate(self,
               info,
               **kwargs):
        """
        TODO add docs

        :param info:
        :param user_id:
        :param email:
        :param image:
        :param address:
        :param firstname:
        :param lastname:
        :return:
        """
        user: ExtendedUser = user_service.update_user(info)
        return UpdateUser(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            address=user.address,
            firstname=user.firstName,
            lastname=user.lastName,
            image=user.image
        )


class DeleteUser(graphene.Mutation):
    id = graphene.Int(required=True)

    class Arguments:
        user_id = graphene.Int(required=True)

    @grant_authorization
    @permission(roles=[Admin, Seller, User])
    def mutate(self, info, user_id):
        """
        TODO add docs

        :param info:
        :param user_id:
        :return:
        """
        user_service.delete_user(info)
        return DeleteUser(
            id=user_id
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
