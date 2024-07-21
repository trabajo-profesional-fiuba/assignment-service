import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

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
def test_add_topic_category_with_success(fastapi, tables):
    category = {
        "name": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/categories", json=category)
    assert response.status_code == 201
    assert response.json() == category


@pytest.mark.integration
def test_add_topic_category_duplicated(fastapi, tables):
    category = {
        "name": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/categories", json=category)
    response = fastapi.post(f"{PREFIX}/categories", json=category)
    assert response.status_code == 409
    assert response.json() == {"detail": "Category 'category 1' already exists."}


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
    assert response.json() == topic


@pytest.mark.integration
def test_add_topic_with_category_not_found(fastapi):
    topic = {
        "name": "topic 2",
        "category": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/", json=topic)

    assert response.status_code == 404
    assert response.json() == {"detail": "Category 'category 1' not found."}


@pytest.mark.skip
def test_add_already_exist_topic(fastapi):
    topic = {
        "name": "topic 1",
        "category": "category 1",
    }

    response = fastapi.post(f"{PREFIX}/", json=topic)
    response = fastapi.post(f"{PREFIX}/", json=topic)

    assert response.status_code == 409
    assert response.json() == {"detail": "Topic 'topic 1, category 1' already exists."}
