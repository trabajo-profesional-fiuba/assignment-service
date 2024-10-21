import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.groups.dependencies import get_email_sender
from src.api.auth.router import router
from src.config.database.database import create_tables, drop_tables


from tests.integration.api.helper import ApiHelper


class MockSendGrid:

    def send_email(self, to, subject, body, cc = []):
        return 200


async def override_get_email_sender():
    yield MockSendGrid()


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
    app.include_router(router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_valid_user_gets_201_and_jwt(fastapi, tables):

    helper = ApiHelper()
    helper.create_student("Juan", "Perez", "105285", "jperez@gmail.com")
    data = {"username": "jperez@gmail.com", "password": "105285"}
    response = fastapi.post("/connect", data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()


@pytest.mark.integration
def test_if_user_not_found_gets_401(fastapi, tables):
    data = {"username": "jperez@gmail.com", "password": "wrong"}
    response = fastapi.post("/connect", data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_reset_password_of_user(fastapi, tables):
    fastapi.app.dependency_overrides[get_email_sender] = override_get_email_sender
    helper = ApiHelper()
    helper.create_student("Pedro", "Perez", "105288", "alejovillores@gmail.com")
    student_token = helper.create_student_token(105288)

    data = {"old_password": "105288", "new_password": "UpdatedPassword"}
    response = fastapi.post(
        "/reset-password",
        json=data,
        headers={"Authorization": f"Bearer {student_token.access_token}"},
    )

    assert response.status_code == status.HTTP_202_ACCEPTED

    data = {"username": "alejovillores@gmail.com", "password": "UpdatedPassword"}
    response = fastapi.post("/connect", data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
