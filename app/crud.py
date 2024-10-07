"""
MODULO DONDE ESTA LA LOGICA DE MANEJO
DE LAS TRANSACCIONES DE LA BD
"""
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from .schemas import *
from .models import *
from .database import connect_to_mongo
from datetime import datetime, timedelta
import uuid

db = connect_to_mongo()

"""
CRUD PARA CREAR TRANSACCIONES, SUBSCRIPCION Y CANCELACION, POR USUARIO 
"""
def create_subscripcion(id_user: str, id_fondo: int):
    #verificamos que exista el fondo y el usuario
    fondo = get_fondo_by_id(id_fondo)    
    user = get_user_by_id(id_user)
    if fondo is None:
        return{"success": False, "error":"El fondo no ha sido encontrado, verifique que exista"}
    
    if user is None:
        return{"success": False, "error":"El usuario no ha sido encontrado, verifique que exista"}
    
    # verificamos que el monto disponible en usuario cubra el minimo para la vinculacion
    user_balance = user.get('balance', 0)
    fondo_monto = float(fondo.get('monto', 0))    
    if user_balance < fondo_monto:
        return {"success": False,"error": f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}"}

    try:
        #creamos el id unico con UUID
        transaction_id = str(uuid.uuid4())
        new_subcrip = {"user_id" : id_user,
                        "fondo_id" : id_fondo,
                        "monto" : fondo_monto,
                        "is_deleted" : False,
                        "transaction_type" : "apertura",
                        "transaction_id" : transaction_id,
                        "created_at" : datetime.now()
                    }            
        # actualizacmos el saldo del usuario
        new_balance = user_balance - fondo_monto
        update_user_id(str(ObjectId(id_user)), {"balance": new_balance})
        #insertamos la transaccionnde apertura
        db.Transacciones.insert_one(new_subcrip)
        return {"success": True ,"message":f"Vinculado al fondo {fondo['nombre']}. Transacción ID: {transaction_id}"}
        
    except PyMongoError as e:
        print(f"Error al crear la suscripción: {e}")  
        return {"success": False, "message":f"el usuario: {user['nombre']}, ha sido vinculado al fondo {fondo['nombre']}. Transacción ID: {transaction_id}"}


def create_cancelacion(id_user: str, id_fondo:int):
    #verificamos que exista el fondo y el usuario sino devolvemos el error
    fondo = get_fondo_by_id(id_fondo)
    user = get_user_by_id(id_user)
    if not fondo:
        return{"success": False, "error":"El fondo no ha sido encontrado, verifique que exista"}
    
    if not user:
        return{"success": False, "error":"El usuario no ha sido encontrado, verifique que exista"}
    
    #verificacmos que el usuario tenga un fondo activo
    transacciones_count = db.Transacciones.count_documents({"user_id": id_user, "is_deleted": False, "fondo_id":id_fondo})
    if transacciones_count > 0:
        user_balance = user.get('balance', 0)
        fondo_monto = float(fondo.get('monto', 0))  
        try:
            transaction_id = str(uuid.uuid4())
            new_cancel = {"user_id" : id_user,
                            "fondo_id" : id_fondo,
                            "monto" : (fondo_monto)*-1,
                            "is_deleted" : False,
                            "transaction_type" : "cancelacion",
                            "transaction_id" : transaction_id,
                            "created_at" : datetime.now()
                        } 
            #devolvemos el monto al usuario
            new_balance = user_balance + fondo_monto
            update_user_id(str(ObjectId(id_user)), {"balance": new_balance})        
            #insertamos una transaccion de cancelacion
            db.Transacciones.insert_one(new_cancel)
            return {"success": True ,"message":f"Vinculado al fondo {fondo['nombre']}. Transacción ID: {transaction_id}"}
            
        except PyMongoError as e:
            print(f"Error al crear la suscripción: {e}")  
            return {"success": False, "message":f"el usuario: {user['nombre']}, ha sido vinculado al fondo {fondo['nombre']}. Transacción ID: {transaction_id}"}
    else:
        return{"success": False, "error":"El usuario no posee fondos activos, verifique que exista por favor"}

"""
CONSULTAS DE HISTORIAL DE TRANSACCIONES 
"""
def get_transacciones_by_user(user_id: str):
    transacciones = db.Transacciones.find({"user_id": user_id})
    trans_list = []
    for trans in transacciones:
        trans['fondo_id'] = str(trans['fondo_id'])
        del trans['_id'] 
        trans_list.append(trans)
    
    return trans_list


def get_transaccciones_by_date(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    transacciones = db.Transacciones.find({
        "created_at": {"$gte": start, "$lte": end}
    })
    trans_list = []
    for trans in transacciones:
        trans['fondo_id'] = str(trans['fondo_id'])
        del trans['_id'] 
        trans_list.append(trans)

    return trans_list


def get_transacciones_by_period(period: str):
    now = datetime.now()
    if period == "semana":
        start = now - timedelta(weeks=1)
    elif period == "mes":
        start = now - timedelta(weeks=4)
    elif period == "semestre":
        start = now - timedelta(weeks=26)
    else:
        return {"error": "Periodo no válido"}

    transacciones = db.Transacciones.find({
        "created_at": {"$gte": start, "$lte": now}
    })
    trans_list = []
    for trans in transacciones:
        trans['fondo_id'] = str(trans['fondo_id'])
        del trans['_id'] 
        trans_list.append(trans)
        
    return trans_list


"""
LISTADOs DE LA COLLECCION DE FONDOS DE PENSION
"""   
def get_fondos_list():
    fondos = list(db.FondosDocument.find({}))
    fondos_list = []
    for fondo in fondos:
        fondo['_id'] = str(fondo['_id'])
        fondos_list.append(fondo)
    return fondos_list

def get_fondo_by_id(id_fondo: int):
    fondo = db.FondosDocument.find_one({"id": id_fondo})
    return fondo

"""
CRUD PARA EL MANEJO DE USUARIOS 
"""
def create_new_user(user_data: dict):
    user_data['user_id'] = str(uuid.uuid4())  
    user_data['is_deleted'] = False  # Asegura que el usuario no está eliminado
    try:
        user_id = db.Users.insert_one(user_data).inserted_id
        return {"success": True, "message": f"Usuario con ID {user_id} nombre {user_data['nombre']} ha sido creado."}
    except PyMongoError as error:
        return {error}


def update_user_id(user_id: str, user_data: dict):
    try:
        # Convertir el user_id a ObjectId
        user_object_id = ObjectId(user_id)        
        # Verificar si el usuario existe y no ha sido eliminado previamente
        user = db.Users.find_one({"_id": user_object_id, "is_deleted": False})
        if not user:
            return {"error": f"No se encontró el usuario con ID {user_id}."}
        else:
            result = db.Users.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
            if result.matched_count:
                return {"success": f"Usuario con ID {user_id} actualizado."}
            
    except PyMongoError as error:
        return {"error": {error}}

"""
Para eliminar el usuario uso el medoto de borrado logico
usando un campo de la coleccion is_deleted == True 
"""

def delete_user_id(user_id: str):
    try:
        # Convertir el user_id a ObjectId
        user_object_id = ObjectId(user_id)
        
        # Verificar si el usuario existe y no ha sido eliminado previamente
        user = db.Users.find_one({"_id": user_object_id, "is_deleted": False})
        if not user:
            return {"error": f"No se encontró el usuario con ID {user_id}."}
        
        # Verificar si el usuario tiene transacciones asociadas
        transacciones_count = db.Transacciones.count_documents({"user_id": user_id, "is_deleted": False})
        
        # Si el usuario tiene transacciones, se eliminan lógicamente
        if transacciones_count > 0:
            db.Transacciones.update_many({"user_id": user_id}, {"$set": {"is_deleted": True}})
        
        # Borrar lógicamente el usuario
        result = db.Users.update_one({"_id": user_object_id}, {"$set": {"is_deleted": True}})
        
        if result.matched_count > 0:
            return {"success": f"Usuario con ID {user_id} eliminado junto con sus transacciones asociadas."}
        else:
            return {"error": f"al borrar el usuario v con ID {user_id}."}
    except PyMongoError as error:
        return {"error": error}
    


def get_user_by_id(id_user: str):
    user = db.Users.find_one({"_id": ObjectId(id_user)})
    if user:
        user['id'] = str(user['_id'])
        del user["_id"]
        return user
    else:
        return {"error": f"No se encontró el usuario con ID {id_user}."}


def get_users_list():
    users = list(db.Users.find({}))
    users_list = []
    for user in users:
        user['id'] = str(user['_id'])
        del user["_id"]  
        users_list.append(user)
    return users_list
