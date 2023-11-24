from pymongo import MongoClient
from bson import ObjectId

class DatabaseHandler:
    def __init__(self, db_connection_string, db_name, collection_name):
        self.client = MongoClient(db_connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_recipe(self, recipe_data):
        return str(self.collection.insert_one(recipe_data).inserted_id)

    def get_recipe_by_id(self, recipe_id):
        return self.collection.find_one({"_id": ObjectId(recipe_id)})

    def drop_collection(self):
        self.collection.drop()



