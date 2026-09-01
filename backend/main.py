from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routers import records_router, export_router
from app.api.routers import auth_router, users_router
from app.infrastructure.persistence.database import engine, SessionLocal
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.seeder import seed_demo, seed_admin

Base.metadata.create_all(bind=engine)

_db = SessionLocal()
try:
    seed_admin(_db)
    seed_demo(_db)
finally:
    _db.close()

app = FastAPI(
    title="enferCloud — Vigilancia DIP",
    description="Sistema de vigilancia de dispositivos invasivos en pacientes hospitalarios",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(users_router.router, prefix="/api/v1")
app.include_router(records_router.router, prefix="/api/v1")
app.include_router(export_router.router, prefix="/api/v1")

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
