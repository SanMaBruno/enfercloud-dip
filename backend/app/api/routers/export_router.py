from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.api.dependencies import get_export_excel
from app.application.use_cases.export_excel import ExportExcel

router = APIRouter(prefix="/exportar", tags=["exportar"])


@router.get("/excel")
def exportar_excel(
    servicio: Optional[str] = Query(None, description="Filtrar por servicio (UCI, UTI, UHI, Medicina, Cirugía)"),
    sala: Optional[str] = Query(None, description="Filtrar por sala específica"),
    use_case: ExportExcel = Depends(get_export_excel),
):
    contenido = use_case.execute(servicio=servicio, sala=sala)
    nombre_archivo = sala or servicio or "todos"
    nombre_archivo = nombre_archivo.replace(" ", "_").replace("/", "-")
    filename = f"vigilancia_dip_{nombre_archivo}_{date.today().strftime('%Y%m%d')}.xlsx"
    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
