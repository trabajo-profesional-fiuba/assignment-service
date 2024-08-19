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


@pytest.fixture
def topics(request):
    filename = request.param
    with open(f"tests/integration/api/topics/data/{filename}.csv", "rb") as file:
        content = file.read()

    content_type = "text/csv"
    return {"file": (filename, content, content_type)}


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_add_topics_with_tutor_not_found(fastapi, tables, topics):
    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tutor 'juan.perez@fi.uba.ar' not found."}


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_add_topics_with_period_not_found(fastapi, tables, tutors, topics):
    # add tutors
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tutor 'juan.perez@fi.uba.ar' has no period."}


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_add_topics_with_diff_categories_success(fastapi, tables, tutors, topics):
    # add tutors
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    # add period
    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED

    # assign period to tutors
    for tutor_id in ["12345678", "23456789"]:
        response = fastapi.post(
            f"{TUTOR_PREFIX}/{tutor_id}/periods", params={"period_id": "1C2024"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 2"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["duplicated_category"], indirect=True)
def test_add_topics_with_same_category_success(fastapi, tables, tutors, topics):
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

    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 1"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["duplicated_topic"], indirect=True)
def test_add_existing_topic_with_success(fastapi, tables, tutors, topics):
    # add tutors
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    # add period
    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED

    # assign period to tutors
    for tutor_id in ["12345678", "23456789"]:
        response = fastapi.post(
            f"{TUTOR_PREFIX}/{tutor_id}/periods", params={"period_id": "1C2024"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 2


@pytest.mark.integration
def test_upload_wrong_type_file(fastapi, tables):
    # add topics
    filename = "test_data"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.parametrize("topics", ["wrong_format"], indirect=True)
@pytest.mark.integration
def test_upload_wrong_format_file(fastapi, tables, topics):
    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_get_topics_with_success(fastapi, tables, tutors, topics):
    # add tutors
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    # add period
    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})
    assert response.status_code == status.HTTP_201_CREATED

    # assign period to tutors
    for tutor_id in ["12345678", "23456789"]:
        response = fastapi.post(
            f"{TUTOR_PREFIX}/{tutor_id}/periods", params={"period_id": "1C2024"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    # get topics
    response = fastapi.get(f"{PREFIX}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": "category 1"},
        {"id": 2, "name": "topic 2", "category": "category 2"},
        {"id": 3, "name": "topic 3", "category": "category 3"},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_update_topics_csv_with_success(fastapi, tables, tutors, topics):
    # add tutors
    response = fastapi.post(f"{TUTOR_PREFIX}/upload", files=tutors)
    assert response.status_code == status.HTTP_201_CREATED

    # add period
    response = fastapi.post(f"{TUTOR_PREFIX}/periods", json={"id": "1C2024"})

    # assign period to tutors
    for tutor_id in ["12345678", "23456789"]:
        assert response.status_code == status.HTTP_201_CREATED
        response = fastapi.post(
            f"{TUTOR_PREFIX}/{tutor_id}/periods", params={"period_id": "1C2024"}
        )

    # add topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED

    # update topics
    response = fastapi.post(f"{PREFIX}/upload", files=topics)
    assert response.status_code == status.HTTP_201_CREATED
