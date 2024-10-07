from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FondosDocument(BaseModel):
    id: int
    nombre: str
    monto:float
    monto_minimo_vinculacion: str
    categoria: str


class Users(BaseModel):
    id: Optional[str]
    nombre: str
    email: str
    phone: str
    is_deleted: bool = False
    balance: float = 500000 
    create_at: datetime = datetime.now()


class Transacciones(BaseModel):
    user_id: str 
    fondo_id: str
    monto: float
    is_deleted: bool = False
    transaction_type: str  # "apertura" o "cancelacion"
    transaction_id: Optional[str]
    create_at: datetime = datetime.now()