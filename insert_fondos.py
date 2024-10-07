import csv
import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client['pension_funds']
fondo = db['FondosDocument']
# Función para leer el CSV e insertar en MongoDB
def insert_funds_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Convertir cada fila en un documento de MongoDB
            fondos_document = {
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "monto": float(row["monto"]),
                "monto_minimo_vinculacion": row["monto_minimo"],
                "categoria": row["categoria"]
            }
            # Insertar en la colección
            fondo.insert_one(fondos_document)
            print(f"Fondo {row['nombre']} insertado correctamente.")

# Llamar a la función con el archivo CSV
insert_funds_from_csv("fondos_pensiones.csv")
