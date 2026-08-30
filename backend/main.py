from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routers import records_router, export_router
from app.infrastructure.persistence.database import engine
from app.infrastructure.persistence.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="enferCloud — Vigilancia DIP",
    description="Sistema de vigilancia de dispositivos invasivos en pacientes hospitalarios",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router.router, prefix="/api/v1")
app.include_router(export_router.router, prefix="/api/v1")

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
