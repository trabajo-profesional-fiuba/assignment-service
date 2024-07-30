import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.tutors.router import router
from src.api.users.model import Role, User
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker


PREFIX = "/tutors"


def creates_user():

    Session = sessionmaker(engine)
    with Session() as sess:
        user = User(
            id=10600,
            name="Juan",
            last_name="Perez",
            email="email@fi.uba.ar",
            password="fake",
            rol=Role.STUDENT,
        )
        sess.add(user)
        sess.commit()


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
def test_upload_file_and_create_tutors(fastapi, tables):

    # Arrange
    with open("tests/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 15


@pytest.mark.integration
def test_upload_file_with_invalid_columns_raise_exception(fastapi, tables):

    # Arrange
    with open("tests/api/tutors/data/wrong_data.csv", "rb") as file:
        content = file.read()

    filename = "wrong_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)
    http_exception = response.json()

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert http_exception.get("detail") == "Columns don't match with expected ones"


@pytest.mark.integration
def test_upload_file_with_duplicates_rows_in_csv_raise_exception(fastapi, tables):

    # Arrange
    with open("tests/api/tutors/data/duplicate_data.csv", "rb") as file:
        content = file.read()

    filename = "duplicate_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)
    http_exception = response.json()

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert http_exception.get("detail") == "Duplicate values inside the csv file"


@pytest.mark.integration
def test_upload_file_with_duplicates_rows_in_db_raise_exception(fastapi, tables):

    # Arrange
    with open("tests/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response_ok = fastapi.post(f"{PREFIX}/upload", files=files)
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    http_exception = response.json()

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert http_exception.get("detail") == "Duplicated tutor"


@pytest.mark.integration
def test_upload_file_raise_execption_if_type_is_not_csv(fastapi, tables):

    # Arrange
    filename = "test_data"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    # Assert
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.integration
def test_add_new_global_period(fastapi, tables):

    # Arrange
    body = {"id": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/periods", json=body)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_all_periods_order_by_asc(fastapi, tables):

    # Arrange
    body = {"id": "1C2024"}
    body2 = {"id": "2C2024"}
    body3 = {"id": "1C2025"}

    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    _ = fastapi.post(f"{PREFIX}/periods", json=body2)
    _ = fastapi.post(f"{PREFIX}/periods", json=body3)

    # Act
    response = fastapi.get(f"{PREFIX}/periods", params={"order": "ASC"})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[0]["id"] == body["id"]


@pytest.mark.integration
def test_get_all_periods_order_by_desc(fastapi, tables):

    # Arrange
    body = {"id": "1C2024"}
    body2 = {"id": "2C2024"}
    body3 = {"id": "1C2025"}

    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    _ = fastapi.post(f"{PREFIX}/periods", json=body2)
    _ = fastapi.post(f"{PREFIX}/periods", json=body3)

    # Act
    response = fastapi.get(f"{PREFIX}/periods", params={"order": "DESC"})
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[0]["id"] == body3["id"]


@pytest.mark.integration
def test_get_all_periods_order_by_default_desc(fastapi, tables):

    # Arrange
    body = {"id": "1C2024"}
    body2 = {"id": "2C2024"}
    body3 = {"id": "1C2025"}

    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    _ = fastapi.post(f"{PREFIX}/periods", json=body2)
    _ = fastapi.post(f"{PREFIX}/periods", json=body3)

    # Act
    response = fastapi.get(f"{PREFIX}/periods")
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[0]["id"] == body3["id"]


@pytest.mark.integration
def test_get_all_periods_is_empty(fastapi, tables):

    # Act
    response = fastapi.get(f"{PREFIX}/periods")
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 0


@pytest.mark.integration
def test_add_new_tutor_period(fastapi, tables):

    # Arrange
    creates_user()
    tutor_id = 10600
    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    response = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
