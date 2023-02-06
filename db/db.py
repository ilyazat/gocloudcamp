from pymongo import MongoClient
from pymongo.collection import Collection

from const import CONNECTION_STRING


client: MongoClient = MongoClient(CONNECTION_STRING)
database = client["test"]
collection: Collection = database["test"]
