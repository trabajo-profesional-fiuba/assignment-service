import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status

from src.api.topic.router import router as topic_router
from src.api.tutors.router import router as tutor_router

PREFIX = "/topics"
TUTOR_PREFIX = "/tutors"


@pytest.fixture(scope="function")
def tables():
    from src.config.database.database import create_tables, drop_tables

    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


@pytest.fixture(scope="session")
def fastapi():
    app = FastAPI()
    app.include_router(topic_router)
    app.include_router(tutor_router)
    client = TestClient(app)
    yield client


@pytest.fixture
def tutors():
    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.mark.integration
def test_add_topics_with_tutor_not_found(fastapi, tables):
    with open("tests/integration/api/topics/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tutor 'juan.perez@fi.uba.ar' not found."}


@pytest.mark.integration
def test_add_topics_with_period_not_found(fastapi, tables, tutors):
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    with open("tests/integration/api/topics/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tutor 'juan.perez@fi.uba.ar' has no period."}


@pytest.mark.integration
def test_add_topics_with_diff_categories_success(fastapi, tables, tutors):
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
    assert response.status_code == status.HTTP_201_CREATED

    with open("tests/integration/api/topics/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 2"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]


def test_add_topics_with_same_category_success(fastapi, tables, tutors):
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
    assert response.status_code == status.HTTP_201_CREATED

    with open("tests/integration/api/topics/data/duplicated_category.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 1"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]


@pytest.mark.integration
def test_add_existing_topic_with_success(fastapi, tables, tutors):
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

    with open("tests/integration/api/topics/data/duplicated_topic.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 2


@pytest.mark.integration
def test_upload_wrong_type_file(fastapi, tables):
    filename = "test_data"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)

    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.integration
def test_upload_wrong_format_file(fastapi, tables):
    with open("tests/integration/api/topics/data/wrong_format.csv", "rb") as file:
        content = file.read()

    filename = "wrong_format"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_get_topics_with_success(fastapi, tables, tutors):
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
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.get(f"{PREFIX}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    with open("tests/integration/api/topics/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.get(f"{PREFIX}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 2"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]
