import unittest
from pymongo import MongoClient
from bson import ObjectId
from database_handler import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        # database for testing
        self.test_db_connection_string = "mongodb+srv://MY_USERNAME:MY_PASSWORD@MYCLUSTER.dlrkkr2.mongodb.net/?retryWrites=true&w=majority"
        self.test_db_name = "test_db"
        self.test_collection_name = "test_collection"

        # Initialize the DatabaseHandler with the test database
        self.db_handler = DatabaseHandler(
            self.test_db_connection_string, self.test_db_name, self.test_collection_name
        )

    def tearDown(self):
        # Drop the test collection after each test
        self.db_handler.drop_collection()

    def test_insert_recipe(self):
        # Test the insert_recipe method
        recipe_data = {"name": "Test Recipe", "ingredients": ["Ingredient1", "Ingredient2"]}
        inserted_id = self.db_handler.insert_recipe(recipe_data)
        self.assertIsNotNone(inserted_id)

    def test_get_recipe_by_id(self):
        # Test the get_recipe_by_id method
        recipe_data = {"name": "Test Recipe", "ingredients": ["Ingredient1", "Ingredient2"]}
        inserted_id = self.db_handler.insert_recipe(recipe_data)

        # Retrieve the recipe using the inserted_id
        retrieved_recipe = self.db_handler.get_recipe_by_id(inserted_id)

        # Assert that the retrieved recipe is not None and has the expected name
        self.assertIsNotNone(retrieved_recipe)
        self.assertEqual(retrieved_recipe["name"], "Test Recipe")


if __name__ == "__main__":
    unittest.main()
