import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def test_app():
    from api.main import app

    with TestClient(app) as client:
        yield client


@pytest.mark.integration
def test_add_topic_category_with_success(test_app):
    topic_category = {
        "name": "category 1",
    }

    response = test_app.post("/topic_category/", json=topic_category)
    assert response.status_code == 201

    expected_response = {
        "name": "category 1",
    }
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_category_duplicated(test_app):
    topic_category = {
        "name": "category 1",
    }

    response = test_app.post("/topic_category/", json=topic_category)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic category 'category 1' already exists."}


@pytest.mark.integration
def test_add_topic_with_success(test_app):
    topic = {
        "name": "topic 1",
        "category": "category 1",
    }

    response = test_app.post("/topic/", json=topic)
    assert response.status_code == 201

    expected_response = {
        "name": "topic 1",
        "category": "category 1",
    }
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_not_found(test_app):
    topic = {
        "name": "topic 2",
        "category": "category 2",
    }
    response = test_app.post("/topic/", json=topic)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic category 'category 2' not found."}
