from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

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

    @field_validator("nombre")
    @classmethod
    def nombre_max(cls, v: str) -> str:
        if len(v) > 120:
            raise ValueError("Nombre demasiado largo (máx 120 caracteres)")
        return v

    @field_validator("observaciones")
    @classmethod
    def observaciones_max(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 500:
            raise ValueError("Observaciones demasiado largas (máx 500 caracteres)")
        return v

    @model_validator(mode="after")
    def fechas_coherentes(self) -> "RegistroDIPCreate":
        if self.fecha_retiro and self.fecha_retiro < self.fecha_instalacion:
            raise ValueError("fecha_retiro no puede ser anterior a fecha_instalacion")
        if self.fecha_ingreso_sala and self.fecha_ingreso_sala > self.fecha_instalacion:
            pass  # ingreso puede ser posterior a instalacion en traslados
        return self


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

    @field_validator("observaciones")
    @classmethod
    def observaciones_max(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 500:
            raise ValueError("Observaciones demasiado largas (máx 500 caracteres)")
        return v


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
