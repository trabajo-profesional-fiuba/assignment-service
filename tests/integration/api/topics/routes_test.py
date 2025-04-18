import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, status

from src.api.topics.router import router as topic_router
from src.api.tutors.router import router as tutor_router
from tests.integration.api.helper import ApiHelper

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
    helper = ApiHelper()
    token = helper.create_admin_token()
    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Tutor 'juan.perez@fi.uba.ar' not found."}


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_add_topics_with_diff_categories_success(fastapi, tables, tutors, topics):
    # add tutors
    helper = ApiHelper()
    token = helper.create_admin_token()
    helper.create_period("1C2024")
    response = fastapi.post(
        f"{TUTOR_PREFIX}/upload",
        files=tutors,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": {"name": "category 1"}},
        {"id": 2, "name": "topic 2", "category": {"name": "category 2"}},
        {"id": 3, "name": "topic 3", "category": {"name": "category 3"}},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["duplicated_category"], indirect=True)
def test_add_topics_with_same_category_success(fastapi, tables, tutors, topics):
    helper = ApiHelper()
    token = helper.create_admin_token()
    helper.create_period("1C2024")
    response = fastapi.post(
        f"{TUTOR_PREFIX}/upload",
        files=tutors,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": {"name": "category 1"}},
        {"id": 2, "name": "topic 2", "category": {"name": "category 1"}},
        {"id": 3, "name": "topic 3", "category": {"name": "category 3"}},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["duplicated_topic"], indirect=True)
def test_add_existing_topic_with_success(fastapi, tables, tutors, topics):
    # add tutors
    helper = ApiHelper()
    token = helper.create_admin_token()
    helper.create_period("1C2024")
    response = fastapi.post(
        f"{TUTOR_PREFIX}/upload",
        files=tutors,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 2


@pytest.mark.integration
def test_upload_wrong_type_file(fastapi, tables):
    # add topics
    helper = ApiHelper()
    token = helper.create_admin_token()
    filename = "test_data"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    response = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.parametrize("topics", ["wrong_format"], indirect=True)
@pytest.mark.integration
def test_upload_wrong_format_file(fastapi, tables, topics):
    helper = ApiHelper()
    token = helper.create_admin_token()
    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_get_topics_with_success(fastapi, tables, tutors, topics):
    # add tutors
    helper = ApiHelper()
    token = helper.create_admin_token()
    helper.create_period("1C2024")
    response = fastapi.post(
        f"{TUTOR_PREFIX}/upload",
        files=tutors,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # get topics
    response = fastapi.get(
        f"{PREFIX}/", headers={"Authorization": f"Bearer {token.access_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "topic 1", "category": {"name": "category 1"}},
        {"id": 2, "name": "topic 2", "category": {"name": "category 2"}},
        {"id": 3, "name": "topic 3", "category": {"name": "category 3"}},
    ]


@pytest.mark.integration
@pytest.mark.parametrize("topics", ["test_data"], indirect=True)
def test_update_topics_csv_with_success(fastapi, tables, tutors, topics):
    # add tutors
    helper = ApiHelper()
    token = helper.create_admin_token()
    helper.create_period("1C2024")
    response = fastapi.post(
        f"{TUTOR_PREFIX}/upload",
        files=tutors,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # add topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # update topics
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=topics,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_add_category_withot_csv_file(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2024")
    admin_token = helper.create_admin_token()

    category_request = {
        "name": "FakeCategory",
    }

    response = fastapi.post(
        f"{PREFIX}/category",
        json=category_request,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 2, "name": "FakeCategory"}


@pytest.mark.integration
def test_add_topics_withot_csv_file(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_category("Fake")
    helper.create_tutor("Celeste", "Perez", "105000", "cdituro@fi.uba.ar")
    helper.create_tutor_period("105000", "1C2024")
    admin_token = helper.create_admin_token()

    topic_request = {
        "name": "My custom topic",
        "category": "Fake",
        "tutor_email": "cdituro@fi.uba.ar",
        "capacity": 2,
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=topic_request,
        params={"period": "1C2024"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "name": "My custom topic",
        "category": {"name": "Fake"},
    }


@pytest.mark.integration
def test_delete_topic_by_id(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_category("Fake")
    helper.create_topic("topic1", 2)
    helper.create_topic("topic2", 2)
    topic = helper.create_topic("topic3", 2)
    helper.create_topic("topic4", 2)

    admin_token = helper.create_admin_token()

    response = fastapi.get(
        f"{PREFIX}",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert len(response.json()) == 4
    response = fastapi.delete(
        f"{PREFIX}/{topic.id}",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_202_ACCEPTED

    response = fastapi.get(
        f"{PREFIX}",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert len(response.json()) == 3
