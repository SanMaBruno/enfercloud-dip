import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.auth.jwt_handler import create_access_token, hash_password
from app.infrastructure.persistence.database import Base, get_db
from app.infrastructure.persistence.models import UsuarioModel
from main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    admin = UsuarioModel(
        username="admin_test",
        hashed_password=hash_password("admin1234"),
        rol="admin",
        sala=None,
        activo=True,
    )
    db_session.add(admin)
    db_session.commit()
    token = create_access_token(admin.username, admin.rol, admin.sala)

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers["Authorization"] = f"Bearer {token}"
        c.test_token = token
        yield c
    app.dependency_overrides.clear()
