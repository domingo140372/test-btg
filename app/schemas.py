from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class UserResponse(BaseModel):
    id: Optional[str]
    nombre: str
    email: str
    phone: str
    is_deleted: bool = Field(default=False)
    balance: float
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    nombre: str
    email: str
    phone: str
    balance: float
    created_at: datetime


class FondosDocumentResponse(BaseModel):
    id: int
    nombre: str
    monto: float
    monto_minimo_vinculacion: str
    categoria: str

    class Config:
        orm_mode = True


class TransaccionesResponse(BaseModel):
    user_id: str
    fondo_id: str
    monto: float
    is_deleted : bool
    transaction_type: str 
    transaction_id: Optional[str]
    create_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class TransaccionesCreate(BaseModel):  
    create_at: datetime = datetime.now()

