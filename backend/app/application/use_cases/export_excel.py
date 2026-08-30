from abc import ABC, abstractmethod

from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP


class ExcelExporter(ABC):
    @abstractmethod
    def export(self, records: list[RegistroDIP]) -> bytes: ...


class ExportExcel:
    def __init__(self, repository: RecordRepository, exporter: ExcelExporter) -> None:
        self._repository = repository
        self._exporter = exporter

    def execute(self) -> bytes:
        records = self._repository.find_all()
        return self._exporter.export(records)
