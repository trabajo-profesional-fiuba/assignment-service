import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import status

from src.api.auth.router import router
from src.api.users.model import User, Role
from src.api.auth.hasher import ShaHasher
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker


def creates_user(email, password):
    hash = ShaHasher()
    Session = sessionmaker(engine)
    with Session() as sess:
        user = User(
            id=10600,
            name="Juan",
            last_name="Perez",
            email=email,
            password=hash.hash(password),
            rol=Role.STUDENT,
        )
        sess.add(user)
        sess.commit()


@pytest.fixture(scope="function")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


@pytest.fixture(scope="session")
def fastapi():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_valid_user_gets_201_and_jwt(fastapi, tables):

    creates_user("test@fi.uba.ar", "password")
    data = {"username": "test@fi.uba.ar", "password": "password"}
    response = fastapi.post(f"/connect", data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()


@pytest.mark.integration
def test_if_user_not_found_gets_401(fastapi, tables):
    data = {"username": "test@fi.uba.ar", "password": "wrong"}
    response = fastapi.post(f"/connect", data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
