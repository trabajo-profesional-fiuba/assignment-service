import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.students.router import router as student_router
from src.api.periods.router import router as period_router
from src.config.database.database import create_tables, drop_tables

from tests.integration.api.helper import ApiHelper

PREFIX = "/students"
PERIOD_PREFIX = "/periods"


@pytest.fixture(scope="module")
def tables():

    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


@pytest.fixture(scope="session")
def fastapi():
    app = FastAPI()
    app.include_router(student_router)
    app.include_router(period_router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_upload_file_and_create_students(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")

    token = helper.create_admin_token()
    with open("tests/integration/api/students/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    # Act
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == 201
    assert len(response.json()) == 30


@pytest.mark.integration
def test_upload_file_raise_exception_if_type_is_not_csv(fastapi, tables):

    # Arrange
    helper = ApiHelper()
    token = helper.create_admin_token()
    filename = "test_data"
    content_type = "application/json"
    files = {"file": (filename, "test".encode(), content_type)}

    # Act
    response = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.integration
def test_get_student_by_ids(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    with open("tests/integration/api/students/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    _ = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Act
    response = fastapi.get(
        f"{PREFIX}/",
        params={"user_ids": ["105001", "105002"], "period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.integration
def test_get_wrongs_student_by_ids_response_404(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()

    # Act
    response = fastapi.get(
        f"{PREFIX}/",
        params={"user_ids": ["1", "2"], "period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_get_duplicate_student_by_ids_response_409(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    # Act
    response = fastapi.get(
        f"{PREFIX}/",
        params={"user_ids": ["1", "1"], "period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.integration
def test_get_all_students(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    with open("tests/integration/api/students/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    _ = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Act
    response = fastapi.get(
        f"{PREFIX}/",
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 30


@pytest.mark.integration
def test_update_student_file_with_success(fastapi, tables):
    helper = ApiHelper()

    token = helper.create_admin_token()
    with open("tests/integration/api/students/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert len(response.json()) == 30

    response = fastapi.post(
        f"{PREFIX}/upload",
        files=files,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert len(response.json()) == 30


@pytest.mark.integration
def test_get_personal_info_without_form_answers(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_student_token(100)

    helper.create_student("Juan", "Perez", "100", "juanperez@fi.uba.ar")
    helper.create_student_period(100, "2C2024")

    response = fastapi.get(
        f"{PREFIX}/info/me", headers={"Authorization": f"Bearer {token.access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == 100
    assert not response.json()["form_answered"]


@pytest.mark.integration
def test_get_personal_info_with_form_answers_and_without_groups(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_student_token(100)
    helper.create_tutor("Tutor1", "Apellido", "1000", "email@fi.uba.ar")
    helper.create_tutor_period(1000, "2C2024", 1)
    helper.create_default_topics(["t1", "t2", "t3", "t4"])
    helper.add_tutor_to_topic(
        "2C2024", "email@fi.uba.ar", ["t1", "t2", "t3", "t4"], [1, 1, 1, 1]
    )
    helper.register_answer([100], ["t1", "t2", "t3"])

    response = fastapi.get(
        f"{PREFIX}/info/me", headers={"Authorization": f"Bearer {token.access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == 100
    assert response.json()["form_answered"]


@pytest.mark.integration
def test_get_existing_period_by_id(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    student_token = helper.create_student_token(100)

    response = fastapi.get(
        f"{PERIOD_PREFIX}/2C2024",
        headers={"Authorization": f"Bearer {student_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    period = response.json()
    assert period["id"] == "2C2024"
    assert period["form_active"] is True
    assert period["initial_project_active"] is False
    assert period["intermediate_project_active"] is False
    assert period["final_project_active"] is False


@pytest.mark.integration
def test_create_student(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    student = {
        "id": 110000,
        "name": "Juan",
        "last_name": "Perez",
        "email": "juanperez123@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 110000
    assert response.json()["name"] == "Juan"
    assert response.json()["last_name"] == "Perez"
    assert response.json()["email"] == "juanperez123@fi.uba.ar"


@pytest.mark.integration
def test_create_duplicated_student(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_admin_token()
    student = {
        "id": 110001,
        "name": "Jose",
        "last_name": "Perez",
        "email": "joseperez@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 110001
    assert response.json()["name"] == "Jose"
    assert response.json()["last_name"] == "Perez"
    assert response.json()["email"] == "joseperez@fi.uba.ar"

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Duplicated student"


@pytest.mark.integration
def test_create_student_with_invalid_token(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_student_token()
    student = {
        "id": 110002,
        "name": "Josefa",
        "last_name": "Perez",
        "email": "josefaperez@fi.uba.ar",
    }

    response = fastapi.post(
        f"{PREFIX}",
        json=student,
        params={"period": "2C2024"},
        headers={"Authorization": f"Bearer {token.access_token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Authorization"
