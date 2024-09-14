import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.groups.router import router
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.integration.api.helper import ApiHelper

PREFIX = "/groups"


@pytest.fixture(scope="function")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


@pytest.fixture(scope="module")
def fastapi():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_add_assigned_group_and_get_one_group(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")

    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_groups_by_period(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    user_token = helper.create_student_token()
    admin_token = helper.create_admin_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Act
    params = {"period": "1C2025"}
    response = fastapi.get(
        f"{PREFIX}/",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1


@pytest.mark.integration
def test_post_groups_with_tutor_not_in_db_returns_not_found(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "The tutor does not exist or this period is not present"
    )


@pytest.mark.integration
def test_post_groups_with_one_student_not_in_db_returns_not_found(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Some ids are not in database"


@pytest.mark.integration
def test_post_groups_without_token(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(f"{PREFIX}/", json=body, params=params)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
