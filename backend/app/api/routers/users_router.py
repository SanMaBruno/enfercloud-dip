from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.infrastructure.auth.jwt_handler import hash_password
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.models import UsuarioModel

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def _to_response(u: "UsuarioModel") -> "UsuarioResponse":
    return UsuarioResponse(
        id=u.id, username=u.username,
        nombre=u.nombre, primer_apellido=u.primer_apellido, segundo_apellido=u.segundo_apellido,
        rol=u.rol, sala=u.sala, activo=u.activo,
    )


class UsuarioCreate(BaseModel):
    username: str
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    password: str
    rol: str = "enfermero"
    sala: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_minima(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    rol: Optional[str] = None
    sala: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    username: str
    nombre: Optional[str]
    primer_apellido: Optional[str]
    segundo_apellido: Optional[str]
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
        nombre=body.nombre or None,
        primer_apellido=body.primer_apellido or None,
        segundo_apellido=body.segundo_apellido or None,
        hashed_password=hash_password(body.password),
        rol=body.rol,
        sala=body.sala,
        activo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return _to_response(usuario)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    usuarios = db.query(UsuarioModel).all()
    return [_to_response(u) for u in usuarios]


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int,
    body: UsuarioUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if body.nombre is not None:
        usuario.nombre = body.nombre or None
    if body.primer_apellido is not None:
        usuario.primer_apellido = body.primer_apellido or None
    if body.segundo_apellido is not None:
        usuario.segundo_apellido = body.segundo_apellido or None
    if body.rol is not None:
        if body.rol == "enfermero" and not (body.sala or usuario.sala):
            raise HTTPException(status_code=422, detail="Un enfermero debe tener sala asignada")
        usuario.rol = body.rol
    if body.sala is not None:
        usuario.sala = body.sala or None
    db.commit()
    db.refresh(usuario)
    return _to_response(usuario)


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
    return _to_response(usuario)


@router.patch("/{usuario_id}/reactivar", response_model=UsuarioResponse)
def reactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = True
    db.commit()
    db.refresh(usuario)
    return _to_response(usuario)


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
