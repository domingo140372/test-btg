import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client['pension_funds']
fondo = db['FondosDocument']
users = db['Users']
trans = db['Transacciones']

fondo.delete_many({})
print("se han elininado los documentos de fondos de pensiones")