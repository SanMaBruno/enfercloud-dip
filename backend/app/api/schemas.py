from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator

from app.domain.enums import DIPTipo, Estado


class RegistroDIPCreate(BaseModel):
    cama: str
    rut: str
    nombre: str
    dip: DIPTipo
    fecha_instalacion: date
    estado: Estado = Estado.INCLUIDO
    servicio: Optional[str] = None
    sala: Optional[str] = None
    edad: Optional[int] = None
    procedencia: Optional[str] = None
    ubicacion_dip: Optional[str] = None
    fecha_ingreso_sala: Optional[date] = None
    fecha_retiro: Optional[date] = None
    observaciones: Optional[str] = None

    @field_validator("cama", "rut", "nombre")
    @classmethod
    def no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo es requerido")
        return v.strip()


class RegistroDIPUpdate(BaseModel):
    cama: Optional[str] = None
    servicio: Optional[str] = None
    sala: Optional[str] = None
    edad: Optional[int] = None
    procedencia: Optional[str] = None
    ubicacion_dip: Optional[str] = None
    fecha_ingreso_sala: Optional[date] = None
    fecha_retiro: Optional[date] = None
    observaciones: Optional[str] = None
    estado: Optional[Estado] = None


class RegistroDIPResponse(BaseModel):
    id: int
    servicio: Optional[str]
    sala: Optional[str]
    cama: str
    rut: str
    nombre: str
    edad: Optional[int]
    procedencia: Optional[str]
    dip: str
    ubicacion_dip: Optional[str]
    fecha_ingreso_sala: Optional[date]
    fecha_instalacion: date
    fecha_retiro: Optional[date]
    dias_dispositivo: int
    dias_hospitalizacion: Optional[int]
    estado: str
    observaciones: Optional[str]

    class Config:
        from_attributes = True


class ResumenResponse(BaseModel):
    total_registros: int
    total_incluidos: int
    total_excluidos: int
    por_dip: dict[str, int]
    dias_promedio_dispositivo: float
    registros_sin_retiro: int
