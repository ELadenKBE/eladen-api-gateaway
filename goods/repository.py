from django.db.models import QuerySet, Q
from graphql import GraphQLResolveInfo

from app.errors import UnauthorizedError
from app.repository_base import RepositoryBase, IRepository
from category.models import Category
from goods.models import Good
from users.models import ExtendedUser


class GoodRepository(RepositoryBase, IRepository):

    model = Good

    @staticmethod
    def create_item(info: GraphQLResolveInfo, **kwargs) -> [QuerySet]:
        user: ExtendedUser = info.context.user or None
        if user.is_seller() or user.is_admin():
            return super(GoodRepository, GoodRepository). \
                create_item_with_no_relations_base(GoodRepository,
                                                   seller_id=user.id,
                                                   **kwargs)
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")


    @staticmethod
    def get_all_items() -> [QuerySet]:
        return super(GoodRepository, GoodRepository). \
            get_all_items_base(GoodRepository)

    @staticmethod
    def get_items_by_filter(search_filter: Q) -> [QuerySet]:
        return super(GoodRepository, GoodRepository).\
            get_items_by_filter_base(GoodRepository, search_filter)

    @staticmethod
    def get_by_id(searched_id: str) -> [QuerySet]:
        return super(GoodRepository, GoodRepository).\
            get_by_id_base(GoodRepository, searched_id)

    @staticmethod
    def update_item(info: GraphQLResolveInfo, item_id, **kwargs) -> [QuerySet]:
        user: ExtendedUser = info.context.user or None
        good = Good.objects.filter(id=item_id).first()
        if user.is_admin() or user == good.seller:
            return super(GoodRepository, GoodRepository).\
                update_item_base(GoodRepository, item_id=item_id, **kwargs)
        else:
            raise UnauthorizedError(
                "Not enough permissions to call this endpoint")

    @staticmethod
    def delete_item(info: GraphQLResolveInfo, searched_id: str):
        user: ExtendedUser = info.context.user or None
        good = Good.objects.filter(id=searched_id).first()
        if user.is_admin() or user.id == good.seller_id:
            super(GoodRepository, GoodRepository). \
                delete_item_base(GoodRepository, searched_id)

    @staticmethod
    def change_category(info: GraphQLResolveInfo,
                        searched_id: str,
                        category_id: str) -> [QuerySet]:
        category = Category.objects.filter(id=category_id).first()
        good = Good.objects.filter(id=searched_id).first()
        user: ExtendedUser = info.context.user or None
        if user.is_admin() or user == good.seller:
            good.category = category
            good.save()
        return good
