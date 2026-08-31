from abc import ABC, abstractmethod
from typing import Optional

from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP


class ExcelExporter(ABC):
    @abstractmethod
    def export(self, records: list[RegistroDIP], titulo: str) -> bytes: ...


class ExportExcel:
    def __init__(self, repository: RecordRepository, exporter: ExcelExporter) -> None:
        self._repository = repository
        self._exporter = exporter

    def execute(self, servicio: Optional[str] = None, sala: Optional[str] = None) -> bytes:
        records = self._repository.find_all()
        if servicio:
            records = [r for r in records if r.servicio == servicio]
        if sala:
            records = [r for r in records if r.sala == sala]
        titulo = sala or servicio or "Todos los servicios"
        return self._exporter.export(records, titulo)
