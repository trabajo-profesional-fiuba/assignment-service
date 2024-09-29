import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.periods.router import router
from src.config.database.database import create_tables, drop_tables

from tests.integration.api.helper import ApiHelper

PREFIX = "/periods"


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
def test_add_new_global_period(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    admin_token = helper.create_admin_token()
    body = {"id": "1C2024"}

    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_duplicates_global_periods_raise_exception(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    admin_token = helper.create_admin_token()
    body = {"id": "1C2024"}

    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Period already exist"


@pytest.mark.integration
def test_period_with_invalid_pattern_raise_exception(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    admin_token = helper.create_admin_token()
    body = {"id": "1c25"}

    # Act
    response = fastapi.post(
        f"{PREFIX}",
        json=body,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"]
        == "Period id should follow patter nC20year, ie. 1C2024"
    )


@pytest.mark.integration
def test_get_all_periods_order_by_asc(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_period("2C2024")
    helper.create_period("1C2025")
    admin_token = helper.create_admin_token()

    # Act
    response = fastapi.get(
        f"{PREFIX}",
        params={"order": "ASC"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[0]["id"] == "1C2024"
    assert data[1]["id"] == "2C2024"
    assert data[2]["id"] == "1C2025"


@pytest.mark.integration
def test_get_all_periods_order_by_desc(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_period("2C2024")
    helper.create_period("1C2025")
    admin_token = helper.create_admin_token()

    # Act
    response = fastapi.get(
        f"{PREFIX}",
        params={"order": "DESC"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[2]["id"] == "1C2024"
    assert data[1]["id"] == "2C2024"
    assert data[0]["id"] == "1C2025"


@pytest.mark.integration
def test_get_all_periods_order_by_default_desc(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_period("2C2024")
    helper.create_period("1C2025")
    admin_token = helper.create_admin_token()

    # Act
    response = fastapi.get(
        f"{PREFIX}",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[2]["id"] == "1C2024"
    assert data[1]["id"] == "2C2024"
    assert data[0]["id"] == "1C2025"


@pytest.mark.integration
def test_get_all_periods_is_empty(fastapi, tables):
    helper = ApiHelper()
    admin_token = helper.create_admin_token()

    # Act
    response = fastapi.get(
        f"{PREFIX}",
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 0


@pytest.mark.integration
def test_update_existing_period(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2025")
    admin_token = helper.create_admin_token()

    body = {
        "id": "1C2025",
        "form_active": False,
        "initial_project_active": True,
        "intermediate_project_active": True,
        "final_project_active": True,
        "groups_assignment_completed": True,
        "topics_tutors_assignment_completed": True,
        "presentation_dates_assignment_completed": True,
    }
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_update_period_not_found(fastapi, tables):
    helper = ApiHelper()
    admin_token = helper.create_admin_token()

    body = {"id": "3C2025", "form_active": False}
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_student_cant_update_existing_period(fastapi, tables):
    helper = ApiHelper()
    student_token = helper.create_student_token()

    body = {"id": "1C2025", "form_active": False}
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        headers={"Authorization": f"Bearer {student_token.access_token}"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
