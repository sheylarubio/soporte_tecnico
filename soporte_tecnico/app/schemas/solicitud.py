from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class PrioridadEnum(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class EstadoEnum(str, Enum):
    pendiente = "pendiente"
    en_proceso = "en_proceso"
    resuelta = "resuelta"

class SolicitudBase(BaseModel):
    codigo: str
    solicitante_nombre: str
    solicitante_email: EmailStr
    descripcion: str
    categoria_id: int
    prioridad: PrioridadEnum
    estado: EstadoEnum = EstadoEnum.pendiente
    observaciones: Optional[str] = None

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(BaseModel):
    solicitante_nombre: Optional[str] = None
    solicitante_email: Optional[EmailStr] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    prioridad: Optional[PrioridadEnum] = None
    estado: Optional[EstadoEnum] = None
    observaciones: Optional[str] = None

class SolicitudResponse(SolicitudBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True