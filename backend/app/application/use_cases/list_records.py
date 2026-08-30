from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP


class ListRecords:
    def __init__(self, repository: RecordRepository) -> None:
        self._repository = repository

    def execute(self, solo_activos: bool = False) -> list[RegistroDIP]:
        if solo_activos:
            return self._repository.find_activos()
        return self._repository.find_all()
