import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def test_app():
    from src.api.main import app

    with TestClient(app) as client:
        yield client


@pytest.mark.integration
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "Ping"


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


@pytest.mark.integration
def test_add_topic_duplicated(test_app):
    topic = {
        "name": "topic 1",
        "category": "category 1",
    }
    response = test_app.post("/topic/", json=topic)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic 'topic 1, category 1' already exists."}


@pytest.mark.integration
def test_add_topic_preferences_with_completed_group_success(test_app):
    topic_preferences = {
        "email_sender": "test1@example.com",
        "email_student_2": "test2@example.com",
        "email_student_3": "test3@example.com",
        "email_student_4": "test4@example.com",
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "Topic 2",
        "topic_2": "Topic 3",
        "topic_3": "Topic 1",
    }

    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 201

    expected_response = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        },
    ]
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_preferences_duplicated(test_app):
    topic_preferences = {
        "email_sender": "test1@example.com",
        "email_student_2": "test2@example.com",
        "email_student_3": "test3@example.com",
        "email_student_4": "test4@example.com",
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "Topic 2",
        "topic_2": "Topic 3",
        "topic_3": "Topic 1",
    }

    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 201
