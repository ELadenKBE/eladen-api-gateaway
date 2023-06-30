import graphene
from decouple import config
from graphql import GraphQLResolveInfo

from app.base_service import BaseService, create_good_filler, \
    create_goods_list_filler
from category.models import Category

from graphene_django import DjangoObjectType

from goods.models import Good
from goods_list.models import GoodsList
from users.schema import UserType


class GoodType(DjangoObjectType):

    class Meta:
        model = Good


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category


class GoodsListType(DjangoObjectType):

    class Meta:
        model = GoodsList


class GoodsListTransferType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    user = graphene.Field(UserType)
    goods = graphene.List(GoodType)

    def __init__(self, id=None, title=None, user=None, goods=None):
        self.id = id
        self.title = title
        self.user = user
        self.goods = goods


class ProductService(BaseService):

    url = config('PRODUCT_SERVICE_URL', default=False, cast=str)

    def get_categories(self, info: GraphQLResolveInfo = None):
        items_list = self._get_data(entity_name='categories', info=info)
        return [Category(**item) for item in items_list]

    def get_goods(self, info: GraphQLResolveInfo = None):
        items_list = self._get_data(entity_name='goods', info=info)
        return [create_good_filler(**item) for item in items_list]

    def get_good_lists(self, info: GraphQLResolveInfo = None):
        items_list = self._get_data(entity_name='goodsLists', info=info)
        return [create_goods_list_filler(**item) for item in items_list]

    def create_good(self, info: GraphQLResolveInfo):
        created_item_dict = self._create_item(info=info,
                                              entity_name="createGood")
        created_item = create_good_filler(**created_item_dict)
        return created_item

    def create_category(self, info: GraphQLResolveInfo):
        created_item_in_dict = self._create_item(info=info,
                                                 entity_name='createCategory')
        return Category(**created_item_in_dict)

    def create_goods_list(self, info: GraphQLResolveInfo):
        created_item_in_dict = self._create_item(info=info,
                                                 entity_name='createGoodsList')
        created_item = create_goods_list_filler(**created_item_in_dict)
        return created_item

    def update_category(self, info: GraphQLResolveInfo):
        created_item_in_dict = self._get_data(entity_name='updateCategory',
                                              info=info)
        return Category(**created_item_in_dict)

    def update_goods_list(self, info: GraphQLResolveInfo):
        created_item_in_dict = self._get_data(entity_name='updateGoodsList',
                                              info=info)
        created_item = create_goods_list_filler(**created_item_in_dict)
        return created_item

    def update_good(self, info: GraphQLResolveInfo):
        created_item_in_dict = self._get_data(entity_name='updateGood',
                                              info=info)
        created_item = create_good_filler(**created_item_in_dict)
        return created_item

    def delete_goods_list(self, info: GraphQLResolveInfo):
        self._get_data(info=info, entity_name='deleteGoodsList')

    def delete_good(self, info: GraphQLResolveInfo):
        self._get_data(info=info, entity_name='deleteGood')

    def delete_category(self, info: GraphQLResolveInfo):
        self._get_data(info=info, entity_name='deleteCategory')

    def change_goods_category(self, info):
        item_in_dict = self._get_data(info=info, entity_name='changeCategory')
        return create_good_filler(**item_in_dict)

    def add_good_to_cart(self, info):
        item_in_dict = self._get_data(info=info, entity_name='addGoodToCart')
        return create_good_filler(**item_in_dict)

    def clean_goods_list(self, info):
        item_in_dict = self._get_data(info=info, entity_name='cleanGoodsList')
        return create_goods_list_filler(**item_in_dict)
