import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    from api.main import app

    with TestClient(app) as client:
        yield client


@pytest.mark.integration
def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "Ping"


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


@pytest.mark.integration
def test_update_topic_preferences_success(test_app):
    updated_topic_preferences = {
        "email_student_2": "test2@example.com",
        "email_student_3": "test3@example.com",
        "email_student_4": "test4@example.com",
        "group_id": "2024-08-25T12:00:00",
        "topic_1": "Topic 1",
        "topic_2": "Topic 2",
        "topic_3": "Topic 3",
    }

    response = test_app.put(
        "/topic_preferences/test1@example.com", json=updated_topic_preferences
    )
    assert response.status_code == 200

    expected_response = [
        {
            "email": "test1@example.com",
            "group_id": "2024-08-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-08-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-08-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-08-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
    ]
    assert response.json() == expected_response


@pytest.mark.integration
def test_update_topic_preferences_not_found(test_app):
    updated_topic_preferences = {
        "email_student_2": "test2@example.com",
        "email_student_3": "test3@example.com",
        "email_student_4": "test4@example.com",
        "group_id": "2024-06-25T12:00:00",
        "topic_1": "Topic 1",
        "topic_2": "Topic 2",
        "topic_3": "Topic 3",
    }

    response = test_app.put(
        "/topic_preferences/not_found@example.com", json=updated_topic_preferences
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Topic preferences of 'not_found@example.com' not found."
    }


# @pytest.mark.integration
# def test_update_topic_preferences_when_student_from_group_not_found_success(test_app):
#     updated_topic_preferences = {
#         "email_student_2": "not_found@example.com",
#         "email_student_3": "test3@example.com",
#         "email_student_4": "test4@example.com",
#         "group_id": "2024-06-25T12:00:00",
#         "topic_1": "Topic 1",
#         "topic_2": "Topic 2",
#         "topic_3": "Topic 3",
#     }

#     response = test_app.put(
#         "/topic_preferences/test1@example.com", json=updated_topic_preferences
#     )
#     assert response.status_code == 200
