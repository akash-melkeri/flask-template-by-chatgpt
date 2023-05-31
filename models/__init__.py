from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URI)

db = client[config.MONGO_DBNAME]
