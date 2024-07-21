import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.api.topic.router import router

PREFIX = "/topics"


@pytest.fixture(scope="function")
def tables():
    from src.config.database import create_tables, drop_tables 
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
def test_add_topic_category_with_success(fastapi, tables):
    category = {
        "name": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/categories", json=category)
    assert response.status_code == 201

    expected_response = {
        "id": 1,
        "name": "category 1",
    }
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_category_duplicated(fastapi, tables):
    category = {
        "name": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/categories", json=category)
    response = fastapi.post(f"{PREFIX}/categories", json=category)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic category 'category 1' already exists."}


@pytest.mark.integration
def test_add_topic_with_success(fastapi, tables):
    category = {
        "name": "category 1",
    }
    topic = {
        "name": "topic 1",
        "category": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/categories", json=category)
    response = fastapi.post(f"{PREFIX}/", json=topic)

    assert response.status_code == 201

    expected_response = {
        "id": 1,
        "name": "topic 1",
        "category_id": 1,
    }
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_not_found(fastapi):
    topic = {
        "name": "topic 2",
        "category": "category 2",
    }
    response = fastapi.post(f"{PREFIX}/", json=topic)
    assert response.status_code == 409


@pytest.mark.integration
def test_add_topic_duplicated(fastapi):
    topic = {
        "name": "topic 1",
        "category": "category 1",
    }
    response = fastapi.post(f"{PREFIX}/", json=topic)
    assert response.status_code == 409
    # assert response.json() == {"detail": "Topic 'topic 1, category 1' already exists."}
