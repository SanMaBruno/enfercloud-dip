from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_add_record, get_list_records, get_repository, get_summary
from app.api.schemas import (
    RegistroDIPCreate,
    RegistroDIPResponse,
    RegistroDIPUpdate,
    ResumenResponse,
)
from app.application.ports.record_repository import RecordRepository
from app.application.use_cases.add_record import AddRecord
from app.application.use_cases.get_summary import GetSummary
from app.application.use_cases.list_records import ListRecords
from app.domain.entities import RegistroDIP
from app.domain.validators import UbicacionInvalidaError, DIPNoPermitidoEnSalaError, validar_ubicacion_dip

router = APIRouter(prefix="/registros", tags=["registros"])


def _entity_to_response(entity: RegistroDIP) -> RegistroDIPResponse:
    return RegistroDIPResponse(
        id=entity.id,
        servicio=entity.servicio,
        sala=entity.sala,
        cama=entity.cama,
        rut=entity.rut,
        nombre=entity.nombre,
        edad=entity.edad,
        procedencia=entity.procedencia,
        dip=entity.dip.value,
        ubicacion_dip=entity.ubicacion_dip,
        fecha_ingreso_sala=entity.fecha_ingreso_sala,
        fecha_instalacion=entity.fecha_instalacion,
        fecha_retiro=entity.fecha_retiro,
        dias_dispositivo=entity.dias_dispositivo,
        dias_hospitalizacion=entity.dias_hospitalizacion,
        estado=entity.estado.value,
        observaciones=entity.observaciones,
    )


@router.post("/", response_model=RegistroDIPResponse, status_code=status.HTTP_201_CREATED)
def crear_registro(
    body: RegistroDIPCreate,
    use_case: AddRecord = Depends(get_add_record),
):
    entity = RegistroDIP(
        servicio=body.servicio,
        sala=body.sala,
        cama=body.cama,
        rut=body.rut,
        nombre=body.nombre,
        edad=body.edad,
        procedencia=body.procedencia,
        dip=body.dip,
        ubicacion_dip=body.ubicacion_dip,
        fecha_ingreso_sala=body.fecha_ingreso_sala,
        fecha_instalacion=body.fecha_instalacion,
        fecha_retiro=body.fecha_retiro,
        observaciones=body.observaciones,
        estado=body.estado,
    )
    try:
        saved = use_case.execute(entity)
    except (UbicacionInvalidaError, DIPNoPermitidoEnSalaError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    return _entity_to_response(saved)


@router.get("/", response_model=list[RegistroDIPResponse])
def listar_registros(
    solo_activos: bool = False,
    use_case: ListRecords = Depends(get_list_records),
):
    return [_entity_to_response(r) for r in use_case.execute(solo_activos)]


@router.get("/resumen", response_model=ResumenResponse)
def obtener_resumen(use_case: GetSummary = Depends(get_summary)):
    resumen = use_case.execute()
    return ResumenResponse(
        total_registros=resumen.total_registros,
        total_incluidos=resumen.total_incluidos,
        total_excluidos=resumen.total_excluidos,
        por_dip=resumen.por_dip,
        dias_promedio_dispositivo=resumen.dias_promedio_dispositivo,
        registros_sin_retiro=resumen.registros_sin_retiro,
    )


@router.get("/{record_id}", response_model=RegistroDIPResponse)
def obtener_registro(
    record_id: int,
    repo: RecordRepository = Depends(get_repository),
):
    entity = repo.find_by_id(record_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return _entity_to_response(entity)


@router.patch("/{record_id}", response_model=RegistroDIPResponse)
def actualizar_registro(
    record_id: int,
    body: RegistroDIPUpdate,
    repo: RecordRepository = Depends(get_repository),
):
    entity = repo.find_by_id(record_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if body.cama is not None:
        entity.cama = body.cama
    if body.servicio is not None:
        entity.servicio = body.servicio
    if body.sala is not None:
        entity.sala = body.sala
    if body.edad is not None:
        entity.edad = body.edad
    if body.procedencia is not None:
        entity.procedencia = body.procedencia
    if body.ubicacion_dip is not None:
        try:
            entity.ubicacion_dip = validar_ubicacion_dip(entity.dip, body.ubicacion_dip)
        except UbicacionInvalidaError as e:
            raise HTTPException(status_code=422, detail=str(e))
    if body.fecha_ingreso_sala is not None:
        entity.fecha_ingreso_sala = body.fecha_ingreso_sala
    if body.fecha_retiro is not None:
        entity.fecha_retiro = body.fecha_retiro
    if body.observaciones is not None:
        entity.observaciones = body.observaciones
    if body.estado is not None:
        entity.estado = body.estado

    updated = repo.update(entity)
    return _entity_to_response(updated)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_registro(
    record_id: int,
    repo: RecordRepository = Depends(get_repository),
):
    if repo.find_by_id(record_id) is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    repo.delete(record_id)
