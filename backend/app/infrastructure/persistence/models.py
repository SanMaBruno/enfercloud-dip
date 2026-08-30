from datetime import date
from typing import Optional

from sqlalchemy import Date, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DIPTipo, Estado
from app.infrastructure.persistence.database import Base


class RegistroDIPModel(Base):
    __tablename__ = "registros_dip"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    servicio: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sala: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cama: Mapped[str] = mapped_column(String(20), nullable=False)
    rut: Mapped[str] = mapped_column(String(20), nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    edad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    procedencia: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    dip: Mapped[str] = mapped_column(String(50), nullable=False)
    ubicacion_dip: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fecha_ingreso_sala: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_instalacion: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_retiro: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="INCLUIDO")
