from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import RegistroDIP


class RecordRepository(ABC):
    @abstractmethod
    def save(self, record: RegistroDIP) -> RegistroDIP: ...

    @abstractmethod
    def find_by_id(self, record_id: int) -> Optional[RegistroDIP]: ...

    @abstractmethod
    def find_all(self) -> list[RegistroDIP]: ...

    @abstractmethod
    def find_activos(self) -> list[RegistroDIP]: ...

    @abstractmethod
    def update(self, record: RegistroDIP) -> RegistroDIP: ...

    @abstractmethod
    def delete(self, record_id: int) -> None: ...
