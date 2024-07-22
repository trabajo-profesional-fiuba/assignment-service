import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status

from src.api.topic.router import router
from src.config.database import create_tables, drop_tables

PREFIX = "/topics"


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
def test_add_topics_with_different_categories_success(fastapi, tables):
    with open("tests/api/topic/data/data_success.csv", "rb") as file:
        content = file.read()

    filename = "data_success"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"name": "topic 1", "category": "category 1"},
        {"name": "topic 2", "category": "category 2"},
        {"name": "topic 3", "category": "category 3"},
    ]


def test_add_topics_with_same_category_success(fastapi, tables):
    with open("tests/api/topic/data/duplicated_category.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"name": "topic 1", "category": "category 1"},
        {"name": "topic 2", "category": "category 1"},
        {"name": "topic 3", "category": "category 3"},
    ]


@pytest.mark.integration
def test_add_already_exist_topic(fastapi):
    with open("tests/api/topic/data/duplicated_topic.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Topic already exists."}


@pytest.mark.integration
def test_upload_wrong_type_file(fastapi):
    filename = "data_success"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)

    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.integration
def test_upload_wrong_format_file(fastapi):
    with open("tests/api/topic/data/wrong_format.csv", "rb") as file:
        content = file.read()

    filename = "wrong_format"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
