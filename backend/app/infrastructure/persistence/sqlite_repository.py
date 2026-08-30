from typing import Optional

from sqlalchemy.orm import Session

from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP
from app.domain.enums import DIPTipo, Estado
from app.infrastructure.persistence.models import RegistroDIPModel


class SQLiteRecordRepository(RecordRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, record: RegistroDIP) -> RegistroDIP:
        model = self._to_model(record)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def find_by_id(self, record_id: int) -> Optional[RegistroDIP]:
        model = self._session.get(RegistroDIPModel, record_id)
        return self._to_entity(model) if model else None

    def find_all(self) -> list[RegistroDIP]:
        models = self._session.query(RegistroDIPModel).order_by(RegistroDIPModel.id).all()
        return [self._to_entity(m) for m in models]

    def find_activos(self) -> list[RegistroDIP]:
        models = (
            self._session.query(RegistroDIPModel)
            .filter(
                RegistroDIPModel.fecha_retiro.is_(None),
                RegistroDIPModel.estado == Estado.INCLUIDO.value,
            )
            .order_by(RegistroDIPModel.cama)
            .all()
        )
        return [self._to_entity(m) for m in models]

    def update(self, record: RegistroDIP) -> RegistroDIP:
        model = self._session.get(RegistroDIPModel, record.id)
        if model is None:
            raise ValueError(f"Registro {record.id} no encontrado")
        self._apply_to_model(record, model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def delete(self, record_id: int) -> None:
        model = self._session.get(RegistroDIPModel, record_id)
        if model is None:
            raise ValueError(f"Registro {record_id} no encontrado")
        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_model(record: RegistroDIP) -> RegistroDIPModel:
        return RegistroDIPModel(
            servicio=record.servicio,
            sala=record.sala,
            cama=record.cama,
            rut=record.rut,
            nombre=record.nombre,
            edad=record.edad,
            procedencia=record.procedencia,
            dip=record.dip.value,
            ubicacion_dip=record.ubicacion_dip,
            fecha_ingreso_sala=record.fecha_ingreso_sala,
            fecha_instalacion=record.fecha_instalacion,
            fecha_retiro=record.fecha_retiro,
            observaciones=record.observaciones,
            estado=record.estado.value,
        )

    @staticmethod
    def _apply_to_model(record: RegistroDIP, model: RegistroDIPModel) -> None:
        model.servicio = record.servicio
        model.sala = record.sala
        model.cama = record.cama
        model.rut = record.rut
        model.nombre = record.nombre
        model.edad = record.edad
        model.procedencia = record.procedencia
        model.dip = record.dip.value
        model.ubicacion_dip = record.ubicacion_dip
        model.fecha_ingreso_sala = record.fecha_ingreso_sala
        model.fecha_instalacion = record.fecha_instalacion
        model.fecha_retiro = record.fecha_retiro
        model.observaciones = record.observaciones
        model.estado = record.estado.value

    @staticmethod
    def _to_entity(model: RegistroDIPModel) -> RegistroDIP:
        return RegistroDIP(
            id=model.id,
            servicio=model.servicio,
            sala=model.sala,
            cama=model.cama,
            rut=model.rut,
            nombre=model.nombre,
            edad=model.edad,
            procedencia=model.procedencia,
            dip=DIPTipo(model.dip),
            ubicacion_dip=model.ubicacion_dip,
            fecha_ingreso_sala=model.fecha_ingreso_sala,
            fecha_instalacion=model.fecha_instalacion,
            fecha_retiro=model.fecha_retiro,
            observaciones=model.observaciones,
            estado=Estado(model.estado),
        )
