from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.dependencies import get_export_excel
from app.application.use_cases.export_excel import ExportExcel

router = APIRouter(prefix="/exportar", tags=["exportar"])


@router.get("/excel")
def exportar_excel(use_case: ExportExcel = Depends(get_export_excel)):
    contenido = use_case.execute()
    filename = f"vigilancia_dip_{date.today().strftime('%Y%m%d')}.xlsx"
    return Response(
        content=contenido,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
