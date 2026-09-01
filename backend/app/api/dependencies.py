from __future__ import annotations

from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.application.ports.record_repository import RecordRepository
from app.application.use_cases.add_record import AddRecord
from app.application.use_cases.export_excel import ExportExcel
from app.application.use_cases.get_summary import GetSummary
from app.application.use_cases.list_records import ListRecords
from app.infrastructure.auth.jwt_handler import decode_access_token
from app.infrastructure.export.excel_exporter import OpenpyxlExcelExporter
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.sqlite_repository import SQLiteRecordRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")
    return current_user


def get_repository(db: Session = Depends(get_db)) -> RecordRepository:
    return SQLiteRecordRepository(db)


def get_add_record(repo: RecordRepository = Depends(get_repository)) -> AddRecord:
    return AddRecord(repo)


def get_list_records(repo: RecordRepository = Depends(get_repository)) -> ListRecords:
    return ListRecords(repo)


def get_summary(repo: RecordRepository = Depends(get_repository)) -> GetSummary:
    return GetSummary(repo)


def get_export_excel(repo: RecordRepository = Depends(get_repository)) -> ExportExcel:
    return ExportExcel(repo, OpenpyxlExcelExporter())
