import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import datetime as dt

from src.api.form.router import router as form_router
from src.api.student.router import router as student_router
from src.api.tutors.router import router as tutor_router
from src.api.topic.router import router as topic_router
from src.config.database.database import create_tables, drop_tables

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
    app.include_router(tutor_router)
    app.include_router(topic_router)
    client = TestClient(app)
    yield client


@pytest.fixture
def topics():
    with open("tests/integration/api/topics/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.fixture
def students():
    with open("tests/integration/api/forms/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.fixture
def tutors():
    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.mark.integration
def test_add_answers_with_topic_not_found(fastapi, tables):
    today = str(dt.datetime.today())
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic1",
        "topic_2": "topic2",
        "topic_3": "topic3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Topic 'topic1' not found."}


@pytest.mark.integration
def test_add_answers_with_student_not_found(fastapi, tables, topics, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    today = str(dt.datetime.today())
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Be sure that the id: 105285 is a valid student."
    }


@pytest.mark.integration
def test_add_answers_with_success(fastapi, tables, topics, students, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "user_id": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]


@pytest.mark.integration
def test_add_answers_with_invalid_role(fastapi, tables, topics, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 12345678,
        "user_id_student_2": 23456789,
        "user_id_student_3": 34567890,
        "user_id_student_4": 45678901,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Be sure that the id: 12345678 is a valid student."
    }


@pytest.mark.integration
def test_add_answers_duplicated(fastapi, tables, topics, students, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "user_id": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]

    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "The answer already exists."}


@pytest.mark.integration
def test_add_not_duplicated_answers(fastapi, tables, topics, students, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "user_id": 105285,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105286,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105287,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
        {
            "user_id": 105288,
            "answer_id": today,
            "topic_1": "topic 1",
            "topic_2": "topic 2",
            "topic_3": "topic 3",
        },
    ]

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 2",
        "topic_2": "topic 3",
        "topic_3": "topic 1",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {
            "user_id": 105285,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "user_id": 105286,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "user_id": 105287,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
        {
            "user_id": 105288,
            "answer_id": today,
            "topic_1": "topic 2",
            "topic_2": "topic 3",
            "topic_3": "topic 1",
        },
    ]


@pytest.mark.integration
def test_delete_answers_with_success(fastapi, tables, topics, students, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/12345678/periods", params={"period_id": "1C2024"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.post(
        f"{TUTOR_PREFIX}/23456789/periods", params={"period_id": "1C2024"}
    )

    response = fastapi.post(f"{TOPIC_PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{STUDENT_PREFIX}/upload", files=students)
    assert response.status_code == status.HTTP_201_CREATED

    today = dt.datetime.today().isoformat()
    body = {
        "user_id_sender": 105285,
        "user_id_student_2": 105286,
        "user_id_student_3": 105287,
        "user_id_student_4": 105288,
        "answer_id": today,
        "topic_1": "topic 1",
        "topic_2": "topic 2",
        "topic_3": "topic 3",
    }
    response = fastapi.post(f"{PREFIX}/answers", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    response = fastapi.delete(f"{PREFIX}/answers/{today}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_delete_answers_not_found(fastapi, tables, topics, students):
    today = dt.datetime.today().isoformat()
    response = fastapi.delete(f"{PREFIX}/answers/{today}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_get_answers_with_success(fastapi, tables, topics):
    response = fastapi.get(f"{PREFIX}/answers")
    assert response.status_code == status.HTTP_200_OK
