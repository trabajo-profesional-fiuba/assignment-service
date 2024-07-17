import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import datetime as dt

from src.api.form.router import router
from src.api.topic.router import router as topic_router
from src.config.database import create_tables, drop_tables

PREFIX = "/forms"

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
    app.include_router(topic_router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_upload_form_and_create_students_respond_201(fastapi, tables):

    # Arrange
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "group_id": str(dt.datetime.today()),
        "topic_1": "Machine Learning",
        "topic_2": "Fiuba",
        "topic_3": "Topic3"
    }
    # Act
    response = fastapi.post(f"{PREFIX}/groups", json=body)

    # Assert
    assert response.status_code == 201