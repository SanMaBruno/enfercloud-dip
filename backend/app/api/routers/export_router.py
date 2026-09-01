from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from app.api.dependencies import get_export_excel
from app.application.use_cases.export_excel import ExportExcel
from app.infrastructure.auth.jwt_handler import decode_access_token

router = APIRouter(prefix="/exportar", tags=["exportar"])


@router.get("/excel")
def exportar_excel(
    servicio: Optional[str] = Query(None),
    sala: Optional[str] = Query(None),
    token: Optional[str] = Query(None),
    use_case: ExportExcel = Depends(get_export_excel),
):
    payload = decode_access_token(token or "")
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    if payload.get("rol") == "enfermero":
        sala = payload.get("sala")

    contenido = use_case.execute(servicio=servicio, sala=sala)
    nombre_archivo = sala or servicio or "todos"
    nombre_archivo = nombre_archivo.replace(" ", "_").replace("/", "-")
    filename = f"vigilancia_dip_{nombre_archivo}_{date.today().strftime('%Y%m%d')}.xlsx"
    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
