from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infrastructure.auth.jwt_handler import create_access_token, verify_password
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    sala: Optional[str]
    username: str


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.username == form.username).first()
    if not usuario or not verify_password(form.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario desactivado")

    token = create_access_token(usuario.username, usuario.rol, usuario.sala)
    return TokenResponse(
        access_token=token,
        rol=usuario.rol,
        sala=usuario.sala,
        username=usuario.username,
    )
