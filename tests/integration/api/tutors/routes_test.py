import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.tutors.router import router
from src.api.users.models import Role, User
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker

from tests.integration.api.helper import ApiHelper

PREFIX = "/tutors"


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
    helper = ApiHelper()
    helper.create_period("1C2024")

    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    params = {"period": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", params=params, files=files)

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
    params = {"period": "1C2O24"}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files, params=params)
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
    params = {"period": "1C2O24"}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files, params=params)
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
    params = {"period": "1C2O24"}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", files=files, params=params)

    # Assert
    assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@pytest.mark.integration
def test_upload_file_with_existing_tutors(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "12345678", "juan.perez@fi.uba.ar")
    helper.create_tutor("Paula", "Diaz", "33456789", "paula.diaz@fi.uba.ar")

    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    params = {"period": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/upload", params=params, files=files)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 15


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
    helper = ApiHelper()
    helper.create_period("1C2024")
    body = {"id": "1C2024"}

    # Act
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
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_period("2C2024")
    helper.create_period("1C2025")

    # Act
    response = fastapi.get(f"{PREFIX}/periods", params={"order": "ASC"})
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

    # Act
    response = fastapi.get(f"{PREFIX}/periods", params={"order": "DESC"})
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

    # Act
    response = fastapi.get(f"{PREFIX}/periods")
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert data[2]["id"] == "1C2024"
    assert data[1]["id"] == "2C2024"
    assert data[0]["id"] == "1C2025"


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
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "10600", "email@fi.uba.ar")
    params = {"period_id": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/{10600}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_if_id_is_not_tutor_raises_a_404(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_student("Juan", "Perez", "105600", "email@fi.uba.ar")
    params = {"period_id": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/{105600}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_add_same_period_to_two_tutors_with_success(fastapi, tables):

    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")
    helper.create_tutor("Juan", "Perez", "105601", "email2@fi.uba.ar")
    params = {"period_id": "1C2024"}

    # Act
    response1 = fastapi.post(f"{PREFIX}/{105600}/periods", params=params)
    response2 = fastapi.post(f"{PREFIX}/{105601}/periods", params=params)

    # Assert
    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_tutors_period_with_success(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")
    helper.create_tutor_period("105600", "1C2024")

    # Act
    response = fastapi.get(f"{PREFIX}/{105600}/periods")

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
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")
    helper.create_tutor_period("105600", "1C2024")
    params = {"period_id": "1C2024"}

    # Act
    response = fastapi.post(f"{PREFIX}/{105600}/periods", params=params)

    # Assert
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.integration
def test_new_upload_override_tutor_periods(fastapi, tables):
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_tutor("Juan", "Perez", "12345678", "juan.perez@fi.uba.ar")
    helper.create_tutor_period("12345678", "1C2024", 5)

    tutor = helper.get_tutor_by_tutor_id(12345678)
    assert tutor.periods[0].capacity == 5

    with open("tests/integration/api/tutors/data/test_data.csv", "rb") as file:
        content = file.read()

    filename = "test_data"
    content_type = "text/csv"
    files = {"file": (filename, content, content_type)}
    params = {"period": "1C2024"}

    response = fastapi.post(f"{PREFIX}/upload", files=files, params=params)
    assert response.status_code == status.HTTP_201_CREATED

    response = fastapi.get(f"{PREFIX}/{12345678}/periods")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["periods"][0]["capacity"] == 1


@pytest.mark.integration
def test_delete_tutor_no_affects_global_periods(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    periods = ["1C2024", "2C2024", "1C2025"]
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")

    for p in periods:
        helper.create_period(p)
        helper.create_tutor_period("105600", p)

    tutor = helper.get_tutor_by_tutor_id(105600)
    assert len(tutor.periods) == 3

    # Act
    response = fastapi.delete(f"{PREFIX}/{105600}")

    # Assert
    assert response.status_code == status.HTTP_202_ACCEPTED

    response = fastapi.get(f"{PREFIX}/periods")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.integration
def test_delete_tutor_by_id_deletes_its_related_periods_also(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    periods = ["1C2024", "2C2024", "1C2025"]
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")

    for p in periods:
        helper.create_period(p)
        helper.create_tutor_period("105600", p)

    tutor = helper.get_tutor_by_tutor_id(105600)
    assert len(tutor.periods) == 3

    # Act
    response = fastapi.delete(f"{PREFIX}/{105600}")

    # Assert
    assert response.status_code == status.HTTP_202_ACCEPTED

    response = fastapi.get(f"{PREFIX}/{105600}/periods")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_all_topics_from_tutors_in_specific_period(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2024")
    helper.create_period("2C2024")
    helper.create_tutor("Juan", "Perez", "105600", "email@fi.uba.ar")
    helper.create_tutor_period("105600", "1C2024")
    helper.create_tutor_period("105600", "2C2024")

    response = fastapi.get(f"{PREFIX}/periods/1C2024")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data[0]["periods"]) == 1
