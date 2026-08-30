from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.ports.record_repository import RecordRepository
from app.application.use_cases.add_record import AddRecord
from app.application.use_cases.export_excel import ExportExcel
from app.application.use_cases.get_summary import GetSummary
from app.application.use_cases.list_records import ListRecords
from app.infrastructure.export.excel_exporter import OpenpyxlExcelExporter
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.sqlite_repository import SQLiteRecordRepository


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
