from __future__ import annotations

import os
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infrastructure.auth.jwt_handler import create_access_token, verify_password
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["auth"])

MAX_INTENTOS = 5
VENTANA_BLOQUEO_SEGUNDOS = 300
_intentos_fallidos: dict[str, list[float]] = {}


def _rate_limit_activo() -> bool:
    return os.getenv("LOGIN_RATE_LIMIT_ENABLED", "false").lower() == "true"


def _bajo_bloqueo(clave: str) -> bool:
    if not _rate_limit_activo():
        return False
    ahora = time.time()
    intentos = [t for t in _intentos_fallidos.get(clave, []) if ahora - t < VENTANA_BLOQUEO_SEGUNDOS]
    _intentos_fallidos[clave] = intentos
    return len(intentos) >= MAX_INTENTOS


def _registrar_intento_fallido(clave: str) -> None:
    if not _rate_limit_activo():
        return
    _intentos_fallidos.setdefault(clave, []).append(time.time())


def _limpiar_intentos(clave: str) -> None:
    _intentos_fallidos.pop(clave, None)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    sala: Optional[str]
    username: str


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    clave_bloqueo = f"{form.username}:{request.client.host if request.client else 'desconocido'}"
    if _bajo_bloqueo(clave_bloqueo):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiados intentos fallidos. Intenta nuevamente en unos minutos.",
        )

    usuario = db.query(UsuarioModel).filter(UsuarioModel.username == form.username).first()
    if not usuario or not verify_password(form.password, usuario.hashed_password):
        _registrar_intento_fallido(clave_bloqueo)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario desactivado")

    _limpiar_intentos(clave_bloqueo)
    token = create_access_token(usuario.username, usuario.rol, usuario.sala)
    return TokenResponse(
        access_token=token,
        rol=usuario.rol,
        sala=usuario.sala,
        username=usuario.username,
    )
