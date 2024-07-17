import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.student.router import router
from src.api.student.repository import StudentRepository
from fastapi import status
from src.api.student.model import StudentModel
from src.config.database import create_tables,drop_tables

PREFIX = '/students'

@pytest.fixture(scope='session')
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()

@pytest.fixture(scope='session')
def fastapi(tables):
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    yield client



@pytest.mark.integration
def test_upload_file_and_create_students_respond_201(fastapi):

    # Arrange 
    with open('tests/api/student/test_data.csv', 'rb') as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files  = {'file': (filename, content, content_type)}
    
    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)

    # Assert
    assert response.status_code == 201

@pytest.mark.integration
def test_upload_file_and_create_students(fastapi):

    # Arrange 
    with open('tests/api/student/test_data.csv', 'rb') as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files  = {'file': (filename, content, content_type)}
    
    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)


    # Assert
    assert len(response.json()) == 3



@pytest.mark.integration
def test_upload_file_raise_execption_if_type_is_not_csv(fastapi):

    # Arrange 
    filename = "test_data"
    content_type = "application/json"
    files  = {'file': (filename, "test".encode(), content_type)}
    
    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files)
    

    # Assert
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE