import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.dates.router import router
from src.config.database.database import create_tables, drop_tables

from tests.integration.api.helper import ApiHelper

PREFIX = "/dates"


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
    app.include_router(router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_add_new_dates(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}

    body = [
        {
            "start": "2024-10-07T12:00:00.000Z",
            "end": "2024-10-07T16:00:00.000Z",
        },  # 4 slots
        {
            "start": "2024-10-07T18:00:00.000Z",
            "end": "2024-10-07T22:00:00.000Z",
        },  # 4 slots
        {
            "start": "2024-10-08T12:00:00.000Z",
            "end": "2024-10-08T14:00:00.000Z",
        },  # 2 slots
        {
            "start": "2024-10-09T12:00:00.000Z",
            "end": "2024-10-09T18:00:00.000Z",
        },  # 6 slots
    ]
    expected_slots = 4 + 4 + 2 + 6
    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots


@pytest.mark.integration
def test_only_admin_can_add_new_dates(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    student_token = helper.create_student_token()

    params = {"period": "1C2024"}

    body = [
        {"start": "2024-10-07T12:00:00.000Z", "end": "2024-10-07T16:00:00.000Z"},
    ]
    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {student_token.access_token}"},
    )

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization"


@pytest.mark.integration
def test_period_needs_to_exits(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    admin_token = helper.create_admin_token()

    params = {"period": "1C2023"}

    body = [
        {"start": "2024-10-07T12:00:00.000Z", "end": "2024-10-07T16:00:00.000Z"},
    ]
    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == 400


@pytest.mark.integration
def test_add_group_dates(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_tutor("Celeste", "Perez", "105000", "cdituro@fi.uba.ar")
    period = helper.create_tutor_period("105000", "2C2024")
    helper.create_student("Victoria", "A", "105001", "vlopez@fi.uba.ar")
    helper.create_student("Ivan", "B", "105002", "ipfaab@fi.uba.ar")
    helper.create_student("Joaquin", "C", "105003", "joagomez@fi.uba.ar")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="2C2024",
    )
    user_token = helper.create_student_token(105001)
    expected_slots = 4 + 4

    body = [
        {
            "start": "2024-10-07T12:00:00.000Z",
            "end": "2024-10-07T16:00:00.000Z",
        },  # 4 slots
        {
            "start": "2024-10-07T18:00:00.000Z",
            "end": "2024-10-07T22:00:00.000Z",
        },  # 4 slots
    ]
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots

    params = {"group_id": group.id}
    # Act
    response = fastapi.post(
        f"{PREFIX}/groups",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots


@pytest.mark.integration
def test_add_tutor_dates(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_tutor("Celeste", "Perez", "105000", "cdituro@fi.uba.ar")
    helper.create_tutor_period("105000", "2C2024")
    tutor_token = helper.create_tutor_token(105000)
    expected_slots = 4 + 4

    body = [
        {
            "start": "2024-10-07T12:00:00.000Z",
            "end": "2024-10-07T16:00:00.000Z",
        },  # 4 slots
        {
            "start": "2024-10-07T18:00:00.000Z",
            "end": "2024-10-07T22:00:00.000Z",
        },  # 4 slots
    ]
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots

    params = {"period": "2C2024"}
    # Act
    response = fastapi.post(
        f"{PREFIX}/tutors",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {tutor_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots


@pytest.mark.integration
def test_add_group_dates_fails_if_student_not_in_group(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_tutor("Celeste", "Perez", "105000", "cdituro@fi.uba.ar")
    period = helper.create_tutor_period("105000", "2C2024")
    helper.create_student("Victoria", "A", "105001", "vlopez@fi.uba.ar")
    helper.create_student("Ivan", "B", "105002", "ipfaab@fi.uba.ar")
    helper.create_student("Joaquin", "C", "105003", "joagomez@fi.uba.ar")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="2C2024",
    )
    user_token = helper.create_student_token(11111)
    expected_slots = 4 + 4

    body = [
        {
            "start": "2024-10-07T12:00:00.000Z",
            "end": "2024-10-07T16:00:00.000Z",
        },  # 4 slots
        {
            "start": "2024-10-07T18:00:00.000Z",
            "end": "2024-10-07T22:00:00.000Z",
        },  # 4 slots
    ]
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == expected_slots

    params = {"group_id": group.id}
    # Act
    response = fastapi.post(
        f"{PREFIX}/groups",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_get_empty_list_of_available_slots(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("2C2024")
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}
    response = fastapi.get(
        f"{PREFIX}",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_get_list_of_available_slots(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("2C2024")
    admin_token = helper.create_admin_token()

    body = [
        {
            "start": "2024-10-07T12:00:00.000Z",
            "end": "2024-10-07T16:00:00.000Z",
        },
        {
            "start": "2024-10-07T18:00:00.000Z",
            "end": "2024-10-07T22:00:00.000Z",
        },
    ]
    admin_token = helper.create_admin_token()

    params = {"period": "2C2024"}
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    expected_slots = response.json()
    assert response.status_code == status.HTTP_201_CREATED

    params = {"period": "2C2024"}
    response = fastapi.get(
        f"{PREFIX}",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(expected_slots)
