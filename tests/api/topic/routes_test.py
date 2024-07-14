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
        "uid_sender": 111111,
        "uid_student_2": 111112,
        "uid_student_3": 111113,
        "uid_student_4": 111114,
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 1",
        "category_1": "category 1",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }

    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 201

    expected_response = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111112,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111113,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111114,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]
    assert response.json() == expected_response


@pytest.mark.integration
def test_add_topic_preferences_duplicated(test_app):
    topic_preferences = {
        "uid_sender": 111111,
        "uid_student_2": 111112,
        "uid_student_3": 111113,
        "uid_student_4": 111114,
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 1",
        "category_1": "category 1",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }
    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 409
    assert response.json() == {"detail": "Student uid '111111' already exists."}


@pytest.mark.integration
def test_add_topic_preferences_with_category_not_found(test_app):
    topic_preferences = {
        "uid_sender": 111115,
        "uid_student_2": 111112,
        "uid_student_3": 111113,
        "uid_student_4": 111114,
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 1",
        "category_1": "category 3",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }
    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic category 'category 3' not found."}


@pytest.mark.integration
def test_add_topic_preferences_with_topic_not_found(test_app):
    topic_preferences = {
        "uid_sender": 111116,
        "uid_student_2": 111112,
        "uid_student_3": 111113,
        "uid_student_4": 111114,
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 3",
        "category_1": "category 1",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }
    response = test_app.post("/topic_preferences/", json=topic_preferences)
    assert response.status_code == 409
    assert response.json() == {"detail": "Topic 'topic 3', 'category 1' not found."}
