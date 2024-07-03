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
        "name": "data science",
    }

    response = test_app.post("/topic_category/", json=topic_category)
    assert response.status_code == 201

    expected_response = {
        "name": "data science",
    }
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_category_duplicated(test_app):
    topic_category = {
        "name": "data science",
    }

    response = test_app.post("/topic_category/", json=topic_category)
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Topic category 'data science' already exists."
    }


@pytest.mark.integration
def test_add_topic_with_success(test_app):
    topic = {
        "name": "investigation",
        "category": "data science",
    }

    response = test_app.post("/topic/", json=topic)
    assert response.status_code == 201

    expected_response = {
        "name": "investigation",
        "category": "data science",
    }
    assert response.json() == expected_response
