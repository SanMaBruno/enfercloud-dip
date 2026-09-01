from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.infrastructure.auth.jwt_handler import hash_password
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.models import UsuarioModel

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


class UsuarioCreate(BaseModel):
    username: str
    password: str
    rol: str = "enfermero"
    sala: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    rol: str
    sala: Optional[str]
    activo: bool


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    body: UsuarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    if db.query(UsuarioModel).filter(UsuarioModel.username == body.username).first():
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    if body.rol == "enfermero" and not body.sala:
        raise HTTPException(status_code=422, detail="Un enfermero debe tener sala asignada")

    usuario = UsuarioModel(
        username=body.username,
        hashed_password=hash_password(body.password),
        rol=body.rol,
        sala=body.sala,
        activo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return UsuarioResponse(
        id=usuario.id,
        username=usuario.username,
        rol=usuario.rol,
        sala=usuario.sala,
        activo=usuario.activo,
    )


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    usuarios = db.query(UsuarioModel).all()
    return [
        UsuarioResponse(id=u.id, username=u.username, rol=u.rol, sala=u.sala, activo=u.activo)
        for u in usuarios
    ]


@router.patch("/{usuario_id}/desactivar", response_model=UsuarioResponse)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.username == current["sub"]:
        raise HTTPException(status_code=400, detail="No puedes desactivar tu propio usuario")
    usuario.activo = False
    db.commit()
    db.refresh(usuario)
    return UsuarioResponse(id=usuario.id, username=usuario.username, rol=usuario.rol, sala=usuario.sala, activo=usuario.activo)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.username == current["sub"]:
        raise HTTPException(status_code=400, detail="No puedes eliminar tu propio usuario")
    db.delete(usuario)
    db.commit()
