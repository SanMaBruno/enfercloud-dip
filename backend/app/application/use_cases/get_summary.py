from dataclasses import dataclass

from app.application.ports.record_repository import RecordRepository
from app.domain.entities import RegistroDIP
from app.domain.enums import DIPTipo, Estado


@dataclass
class ResumenVigilancia:
    total_registros: int
    total_incluidos: int
    total_excluidos: int
    por_dip: dict[str, int]
    dias_promedio_dispositivo: float
    registros_sin_retiro: int


class GetSummary:
    def __init__(self, repository: RecordRepository) -> None:
        self._repository = repository

    def execute(self) -> ResumenVigilancia:
        registros = self._repository.find_all()
        incluidos = [r for r in registros if r.estado == Estado.INCLUIDO]
        excluidos = [r for r in registros if r.estado == Estado.EXCLUIDO]

        por_dip: dict[str, int] = {}
        for r in incluidos:
            por_dip[r.dip.value] = por_dip.get(r.dip.value, 0) + 1

        dias_lista = [r.dias_dispositivo for r in incluidos]
        promedio = sum(dias_lista) / len(dias_lista) if dias_lista else 0.0
        sin_retiro = sum(1 for r in incluidos if r.fecha_retiro is None)

        return ResumenVigilancia(
            total_registros=len(registros),
            total_incluidos=len(incluidos),
            total_excluidos=len(excluidos),
            por_dip=por_dip,
            dias_promedio_dispositivo=round(promedio, 1),
            registros_sin_retiro=sin_retiro,
        )
