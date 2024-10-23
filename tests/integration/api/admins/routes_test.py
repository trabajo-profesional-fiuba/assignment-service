import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.admins.router import router as admin_router
from src.config.database.database import create_tables, drop_tables

from tests.integration.api.helper import ApiHelper

PREFIX = "/admins"


@pytest.fixture(scope="module")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


@pytest.fixture(scope="session")
def fastapi():
    app = FastAPI()
    app.include_router(admin_router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_create_admin(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    admin = {
        "id": 105285,
        "name": "Alejo",
        "last_name": "Admin",
        "email": "adminale@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=admin,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 105285
    assert response.json()["name"] == "Alejo"
    assert response.json()["last_name"] == "Admin"
    assert response.json()["email"] == "adminale@fi.uba.ar"


@pytest.mark.integration
def test_create_duplicated_admin(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    student = {
        "id": 110001,
        "name": "Jose",
        "last_name": "Perez",
        "email": "joseperez@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 110001
    assert response.json()["name"] == "Jose"
    assert response.json()["last_name"] == "Perez"
    assert response.json()["email"] == "joseperez@fi.uba.ar"

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Duplicated admin"


@pytest.mark.integration
def test_create_admin_with_invalid_token(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_student_token()
    admin = {
        "id": 110002,
        "name": "Josefa",
        "last_name": "Perez",
        "email": "josefaperez@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=admin,
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization"
