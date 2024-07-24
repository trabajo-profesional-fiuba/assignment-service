import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.student.router import router
from fastapi import status
from src.config.database import create_tables, drop_tables

PREFIX = "/students"


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
def test_upload_file_and_create_students_respond_201(fastapi, tables):

    # Arrange
    with open("tests/api/student/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    # Assert
    assert response.status_code == 201


@pytest.mark.integration
def test_upload_file_and_create_students(fastapi, tables):

    # Arrange
    with open("tests/api/student/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    # Assert
    assert len(response.json()) == 3


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
def test_get_student_by_ids(fastapi, tables):
    with open("tests/api/student/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    _ = fastapi.post(f"{PREFIX}/upload", files=files)
    
    # Act
    response = fastapi.get(f"{PREFIX}/", params={"uids": ["123456789", "12344321"]})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.integration
def test_get_wrongs_student_by_ids_response_404(fastapi, tables):

    # Act
    response = fastapi.get(f"{PREFIX}/", params={"uids": ["1", "2"]})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_get_duplicate_student_by_ids_response_409(fastapi, tables):

    # Act
    response = fastapi.get(f"{PREFIX}/", params={"uids": ["1", "1"]})

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT