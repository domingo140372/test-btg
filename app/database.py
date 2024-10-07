from pymongo import MongoClient
import os
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/pension_funds") 

client = MongoClient(mongo_uri)
db = client["pension_funds"]

def connect_to_mongo():
    return db
