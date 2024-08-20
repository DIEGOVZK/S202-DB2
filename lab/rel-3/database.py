from data import dataset
import pymongo as mdb

from bson import json_util
import json
import os


class Database:
    '''Classe provida no documento de aula'''

    def __init__(self, database, collection):
        self.connect(database, collection)

    def connect(self, database, collection):
        try:
            connectionString = "localhost:27017"
            self.clusterConnection = mdb.MongoClient(
                connectionString,
                tlsAllowInvalidCertificates=True
            )
            self.db = self.clusterConnection[database]
            self.collection = self.db[collection]
        except Exception as e:
            print(e)

    def resetDatabase(self):
        try:
            self.db.drop_collection(self.collection)
            self.collection.insert_many(dataset)
        except Exception as e:
            print(e)


def mklog(data, name: str):
    '''Função provida no documento da aula'''

    parsed_json = json.loads(json_util.dumps(data))

    if not os.path.isdir("./logs"):
        os.makedirs("./logs")

    with open(f"./logs/{name}.json", 'w') as json_file:
        json.dump(parsed_json, json_file,
                  indent=4,
                  separators=(',', ': '))

    return parsed_json
