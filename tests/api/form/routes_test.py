import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import datetime as dt

from src.api.form.router import router as form_router
from src.api.student.router import router as student_router
from src.api.tutors.router import router as tutors_router
from src.api.topic.router import router as topic_router
from src.config.database import create_tables, drop_tables

PREFIX = "/forms"
TOPIC_PREFIX = "/topics"
STUDENT_PREFIX = "/students"
TUTOR_PREFIX = "/tutors"


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
    app.include_router(form_router)
    app.include_router(student_router)
    app.include_router(tutors_router)
    app.include_router(topic_router)
    client = TestClient(app)
    yield client


@pytest.fixture
def topics():
    with open("tests/api/topic/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.fixture
def students():
    with open("tests/api/form/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.fixture
def tutors():
    with open("tests/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.mark.integration
def test_add_group_form_with_topic_not_found(fastapi, tables):
    today = str(dt.datetime.today())
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic1",
        "topic_2": "topic2",
        "topic_3": "topic3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Topic 'topic1' not found."}


@pytest.mark.integration
def test_add_group_form_with_student_not_found(fastapi, tables, topics):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    today = str(dt.datetime.today())
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Student with uid '105285' not found."}


@pytest.mark.integration
def test_add_group_form_with_success(fastapi, tables, topics, students):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "uid": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]


@pytest.mark.integration
def test_add_group_form_with_invalid_role(fastapi, tables, topics, tutors):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 12345678,
        "uid_student_2": 23456789,
        "uid_student_3": 34567890,
        "uid_student_4": 45678901,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "The student must have the role 'student'."}


@pytest.mark.integration
def test_add_group_form_duplicated(fastapi, tables, topics, students):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "uid": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]

    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "The answer already exists."}


@pytest.mark.integration
def test_add_not_duplicated_group_form(fastapi, tables, topics, students):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "uid": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "uid": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 2",
        "topic_2": "topic 3",
        "topic_3": "topic 1",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "uid": 105285,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "uid": 105286,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "uid": 105287,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "uid": 105288,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
    ]


@pytest.mark.integration
def test_delete_group_form_with_success(fastapi, tables, topics, students):
    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.delete(f"{PREFIX}/groups/{today}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_delete_group_form_not_found(fastapi, tables, topics, students):
    today = dt.datetime.today().isoformat()
    response = fastapi.delete(f"{PREFIX}/groups/{today}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_get_group_forms_with_success(fastapi, tables, topics):
    response = fastapi.get(f"{PREFIX}/groups")
    assert response.status_code == status.HTTP_200_OK
