import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.tutors.router import router
from src.api.users.models import Role, User
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker


PREFIX = "/tutors"


def creates_user(n, email, role=Role.TUTOR):

    Session = sessionmaker(engine)
    with Session() as sess:
        user = User(
            id=n,
            name="Juan",
            last_name="Perez",
            email=email,
            password="fake",
            role=role,
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
    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
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
    with open("tests/integration/api/tutors/data/wrong_data.csv", "rb") as file:
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
    with open("tests/integration/api/tutors/data/duplicate_data.csv", "rb") as file:
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
def test_upload_file_raise_exception_if_type_is_not_csv(fastapi, tables):
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
def test_duplicates_global_periods_raise_exception(fastapi, tables):
    # Arrange
    body = {"id": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/periods", json=body)
    response = fastapi.post(f"{PREFIX}/periods", json=body)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Period already exist"


@pytest.mark.integration
def test_period_with_invalid_pattern_raise_exception(fastapi, tables):
    # Arrange
    body = {"id": "1c25"}

    # Act
    response = fastapi.post(f"{PREFIX}/periods", json=body)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"]
        == "Period id should follow patter nC20year, ie. 1C2024"
    )


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
def test_add_new_tutor_period_with_success(fastapi, tables):
    # Arrange
    tutor_id = 10600
    creates_user(tutor_id, "email@fi.uba.ar")
    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    response = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_if_id_is_not_tutor_raises_a_404(fastapi, tables):
    # Arrange
    tutor_id = 10600
    creates_user(tutor_id, "email@fi.uba.ar", Role.STUDENT)
    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    response = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_add_same_period_to_two_tutors_with_success(fastapi, tables):

    # Arrange
    tutor_id_1 = 10600
    tutor_id_2 = 10601

    email1 = "tutor1@fi.uba.ar"
    email2 = "tutor2@fi.uba.ar"

    creates_user(tutor_id_1, email1)
    creates_user(tutor_id_2, email2)

    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    response = fastapi.post(f"{PREFIX}/{tutor_id_1}/periods", params=params)
    response2 = fastapi.post(f"{PREFIX}/{tutor_id_2}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_tutors_period_with_success(fastapi, tables):
    # Arrange
    tutor_id = 10600
    creates_user(tutor_id, "fake@fi.ubar.ar")
    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    _ = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)
    response = fastapi.get(f"{PREFIX}/{tutor_id}/periods")

    # Assert
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_raise_404_if_tutor_not_exists(fastapi, tables):
    # Arrange
    tutor_id = 10600

    # Act
    response = fastapi.get(f"{PREFIX}/{tutor_id}/periods")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_add_same_period_to_same_tutor_raise_error(fastapi, tables):
    # Arrange
    tutor_id_1 = 10600
    email1 = "tutor1@fi.uba.ar"

    creates_user(tutor_id_1, email1)

    body = {"id": "1C2024"}
    params = {"period_id": "1C2024"}

    # Act
    _ = fastapi.post(f"{PREFIX}/periods", json=body)
    _ = fastapi.post(f"{PREFIX}/{tutor_id_1}/periods", params=params)
    response2 = fastapi.post(f"{PREFIX}/{tutor_id_1}/periods", params=params)

    # Assert
    assert response2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.integration
def test_update_tutors_and_tutor_period_is_deleted(fastapi, tables):
    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED

    body = {"id": "1C2024"}
    response = fastapi.post(f"{PREFIX}/periods", json=body)
    assert response.status_code == status.HTTP_201_CREATED

    tutor_id = 12345678
    params = {"period_id": "1C2024"}
    response = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.get(f"{PREFIX}/{tutor_id}/periods")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["periods"]) == 0


@pytest.mark.integration
def test_update_tutors_and_period_is_not_deleted(fastapi, tables):
    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED

    body = {"id": "1C2024"}
    response = fastapi.post(f"{PREFIX}/periods", json=body)
    assert response.status_code == status.HTTP_201_CREATED

    tutor_id = 12345678
    params = {"period_id": "1C2024"}
    response = fastapi.post(f"{PREFIX}/{tutor_id}/periods", params=params)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.post(f"{PREFIX}/upload", files=files)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.get(f"{PREFIX}/periods")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
