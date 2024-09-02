from bson import json_util
import pymongo as mdb
import json
import os

class Database:
    def __init__(self, database_name, collection_name):
        self.client = mdb.MongoClient('localhost:27017', tlsAllowInvalidCertificates=True)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add(self, data):
        self.collection.insert_one(data)

    def get(self):
        return self.collection.find()
    
    def resetAll(self):
        try:
            self.clusterConnection.drop_database(self.db)
        except Exception as e:
            print(e)

    def __del__(self):
        self.client.close()
