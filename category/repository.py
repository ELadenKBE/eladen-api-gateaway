from django.db.models import QuerySet

from app.repository_base import RepositoryBase
from category.models import Category


class CategoryRepository(RepositoryBase):
    model = Category
    
    @staticmethod
    def get_by_id():
        super().get_by_id(model)

    

    
