import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.tutors.router import router
from src.api.tutors.schemas import Tutor
from src.api.auth.hasher import ShaHasher


PREFIX = "/tutors"


@pytest.fixture(scope="function")
def tables():
    from src.config.database import create_tables, drop_tables

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