from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP
from app.domain.validators import validar_ubicacion_dip


class AddRecord:
    def __init__(self, repository: RecordRepository) -> None:
        self._repository = repository

    def execute(self, record: RegistroDIP) -> RegistroDIP:
        record.ubicacion_dip = validar_ubicacion_dip(record.dip, record.ubicacion_dip)
        return self._repository.save(record)
