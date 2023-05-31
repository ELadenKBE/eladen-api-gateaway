from app.errors import UnauthorizedError
from category.models import Category
from .base_api_test import WrapperForBaseTestClass


class CategoryEndpointTests(WrapperForBaseTestClass.BaseEndpointsTests):
    """Test category endpoint.
    """

    model = Category

    mutation_create = '''mutation{{ createCategory(title:"{0}"){{
                                   id
                                   title 
                               }} 
                             }}
                           '''
    mutation_create_name = "createCategory"
    all_query = """query{
                          categories{
                            id
                            title
                          }
                        }
                    """
    by_id_query = """query{
                      categories(searchedId: "1"){
                        id
                        title
                      }
                    }"""
    mutation_update = '''mutation{{
                      updateCategory(id:1, title:"{0}"){{
                        id
                        title
                      }}
                    }}'''
    mutation_update_name = 'updateCategory'

    mutation_delete = '''mutation{{
                      deleteCategory(id:{0}){{
                        id
                        title
                      }}
                    }}
                '''
    plural_name = "categories"

    @staticmethod
    def create_item():
        item = Category(title="title")
        item.save()
        return item

    def test_create_item_as_admin(self):
        """Test. if can be created by admin"""
        self.create_item_as("admin")

    def test_create_item_as_seller(self):
        """Test. if can be created by seller"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("seller")

    def test_create_item_as_user(self):
        """Test. if can be created by user"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as("user")

    def test_create_item_as_anon(self):
        """Test. if can be created by anonymous user"""
        with self.assertRaises(UnauthorizedError):
            self.create_item_as()

    def test_update_by_id_as_admin(self):
        """Test. admin should be allowed to update any entity"""
        self.update_by_id_as(role="admin", fields=["title"])

    def test_update_by_id_as_seller(self):
        """Test. seller should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as(role="seller", fields=["title"])

    def test_update_by_id_as_user(self):
        """Test. user should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as(role="user", fields=["title"])

    def test_update_by_id_as_anon(self):
        """Test. anon should not be allowed to update category entity"""
        with self.assertRaises(UnauthorizedError):
            self.update_by_id_as(fields=["title"])

    def test_delete_by_id_as_admin(self):
        """Test. Admin should be able to delete a category"""
        self.delete_by_id_as("admin")

    def test_delete_by_id_as_seller(self):
        """Test. Seller should not be able to delete a category"""
        with self.assertRaises(UnauthorizedError):
            self.delete_by_id_as("seller")

    def test_delete_by_id_as_user(self):
        """Test. User should not be able to delete a category"""
        with self.assertRaises(UnauthorizedError):
            self.delete_by_id_as("user")

    def test_delete_by_id_as_anon(self):
        """Test. Anonymous user should not be able to delete a category"""
        with self.assertRaises(UnauthorizedError):
            self.delete_by_id_as()
