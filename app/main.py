""" 
MANIZALES 7 OCT 2024
REALIZADO POR: DOMINGO UTRERA
PARA BTG-PACTUAL
TEST PARA INGRESO A PUESTO DE TRABAJO
"""
from fastapi import FastAPI, HTTPException
from .database import connect_to_mongo
from .crud import *
from .schemas import *
from .models import *
from .notifications import *

app = FastAPI(
    title="Api_BTG",  
    description="API para la gestión de fondos de pensiones",  # Puedes agregar una descripción opcional
    version="1.1.0",  # Especifica la versión de tu API
)

# Connect to MongoDB
connect_to_mongo()

@app.post("/fondos/subscribise")
def subscribe_to_fund( tipo_notificacion: str, id_user:str, id_fondo:int):
    create_subs = create_subscripcion(id_user=id_user, id_fondo=id_fondo)
    user = get_user_by_id(id_user=id_user)
    if create_subs['success'] == True:
        if tipo_notificacion == "email":
            send_email(user['email'], "Notifiacion del Fondo de inversiones", f"Sr {user['nombre']} usted se ha suscrito al fondo")
            return dict({"success": True, "message": f"La subscripcion ha sido realizada con exito"})
        elif tipo_notificacion == "sms":
            send_sms(user.phone, "usted a realizado una subcripcion al fondo de inversiones")
            return dict({"success": True, "message": f"La subscripcion ha sido realizada con exito"})
        else:
            raise HTTPException(status_code=400, detail="Preferencia de notificación no válida")    
    return create_subs


@app.post("/fondos/cancelar")
def cancel_fund(tipo_notificacion, id_user:str, id_fondo:int):
    create_cancel = create_cancelacion(id_user=id_user, id_fondo=id_fondo)
    user = get_user_by_id(id_user=id_user)
    if create_cancel['success'] == True:
        if tipo_notificacion == "email":
            send_email(user['email'], "Notifiacion del Fondo de inversiones", f"Sr {user['nombre']} usted ha cancelado su subscripcion fondo")
            return dict({"success": True, "message": f"La subscripcion ha sido cancelada con exito"})
        elif tipo_notificacion == "sms":
            send_sms(user['phone'], "usted a realizado una cancelacion al fondo de inversiones")
            return dict({"success": True, "message": f"La subscripcion ha sido cancelada con exito"})
        else:
            raise HTTPException(status_code=400, detail="Preferencia de notificación no válida")
    return create_cancel


"""
LISTADO DE TRACCIONES 
"""
@app.get("/transacciones/user/{user_id}", response_model = list[TransaccionesResponse])
def get_user_transactions(user_id: str):
    transactions = get_transacciones_by_user(user_id)
    return transactions


@app.get("/transacciones/date", response_model = list[TransaccionesResponse])
def get_transacciones_by_date(start_date: str, end_date: str):
    transactions = get_transacciones_by_date(start_date, end_date)
    return transactions


@app.get("/transactciones/period/{period}", response_model = list[TransaccionesResponse])
def get_transactions_by_period(period: str):
    transactions = get_transacciones_by_period(period)
    return transactions


"""
MANEJO DE USUARIOS 
"""
@app.post("/users/")
def create_user(user: UserCreate):
    user_data = user.dict()
    user_id = create_new_user(user_data)
    return {"success": f"Usuario creado con ID: {user_id}"}


@app.put("/users/{user_id}")
def update_user(user_id: str, user: Users):
    result = update_user_id(user_id, user.dict())
    return result


@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = delete_user_id(user_id)
    return result


@app.get("/user/{user_id}")
def get_user(user_id):
    user = get_user_by_id(user_id)
    return user

@app.get("/users/", response_model=list[Users])
async def get_users():
    users =  get_users_list()
    return list(users)

"""
LISTADO DE FONDOS DISPONIBLES 
"""
@app.get("/fondos/", response_model=list[FondosDocument])
async def get_fondos():
    fondos =  get_fondos_list()
    return list(fondos)
