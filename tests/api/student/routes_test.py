import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.student.router import router


@pytest.fixture()
def test_app():
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        yield client

@pytest.mark.integration
def test_root(test_app):
    response = test_app.get("/students/")
    assert response.status_code == 200