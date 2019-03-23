from pymongo import MongoClient


class DatabaseHelper:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Revisor
    
    def insert_Data(self, collection, document):
        _collection = self.db[collection]
        _id = _collection.insert_one(document).inserted_id
        return _id