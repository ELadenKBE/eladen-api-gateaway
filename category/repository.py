from django.db.models import QuerySet, Q
from graphql import GraphQLResolveInfo

from app.repository_base import RepositoryBase, IRepository
from category.models import Category
from users.models import ExtendedUser


class CategoryRepository(RepositoryBase, IRepository):

    model = Category

    @staticmethod
    def create_item(**kwargs) -> [QuerySet]:
        return super(CategoryRepository, CategoryRepository). \
            create_item_with_no_relations_base(CategoryRepository, **kwargs)

    @staticmethod
    def get_all_items() -> [QuerySet]:
        return super(CategoryRepository, CategoryRepository). \
            get_all_items_base(CategoryRepository)

    @staticmethod
    def get_items_by_filter(search_filter: Q) -> [QuerySet]:
        return super(CategoryRepository, CategoryRepository).\
            get_items_by_filter_base(CategoryRepository, search_filter)

    @staticmethod
    def get_by_id(searched_id: str) -> [QuerySet]:
        return super(CategoryRepository, CategoryRepository).\
            get_by_id_base(CategoryRepository, searched_id)

    @staticmethod
    def update_item(item_id, **kwargs) -> [QuerySet]:
        return super(CategoryRepository, CategoryRepository).\
            update_item_base(CategoryRepository, item_id=item_id, **kwargs)

    @staticmethod
    def delete_item(info: GraphQLResolveInfo, searched_id: str):
        user: ExtendedUser = info.context.user or None
        if user.is_admin():
            return super(CategoryRepository, CategoryRepository). \
                delete_item_base(CategoryRepository, searched_id)
