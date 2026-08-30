from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domain.enums import DIPTipo, Estado


@dataclass
class RegistroDIP:
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
    id: Optional[int] = field(default=None)

    @property
    def dias_dispositivo(self) -> int:
        fin = self.fecha_retiro or date.today()
        return (fin - self.fecha_instalacion).days

    @property
    def dias_hospitalizacion(self) -> Optional[int]:
        if self.fecha_ingreso_sala is None:
            return None
        fin = self.fecha_retiro or date.today()
        return (fin - self.fecha_ingreso_sala).days
