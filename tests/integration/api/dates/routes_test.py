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
        {"start": "2024-10-07T12:00:00.000Z", "end": "2024-10-07T16:00:00.000Z"}, # 4 slots
        {"start": "2024-10-07T18:00:00.000Z", "end": "2024-10-07T22:00:00.000Z"}, # 4 slots
        {"start": "2024-10-08T12:00:00.000Z", "end": "2024-10-08T14:00:00.000Z"}, # 2 slots
        {"start": "2024-10-09T12:00:00.000Z", "end": "2024-10-09T18:00:00.000Z"}, # 6 slots
    ]                                                                             
    expected_slots = 4+4+2+6
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
