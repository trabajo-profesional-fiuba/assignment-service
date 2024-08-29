import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.groups.router import router
from src.api.groups.schemas import GroupList
from src.api.tutors.models import Period
from src.api.tutors.repository import TutorRepository
from src.api.users.models import User, Role
from src.api.users.repository import UserRepository
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.integration.api.helper import ApiHelper

PREFIX = "/groups"


@pytest.fixture(scope="module")
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
def test_add_group(fastapi, tables):
    helper = ApiHelper()
    token = helper.create_student_token()
    tutor_repository = TutorRepository(Session)
    tutor_repository.add_period(Period(id="1C2025"))

    user_repository = UserRepository(Session)
    tutor = User(
        id=3,
        name="Pedro",
        last_name="Pipo",
        email="tutor@fi.uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=10000,
        name="Juan",
        last_name="Perez",
        email="10000@fi.uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=2,
        name="Pedro",
        last_name="Pipo",
        email="2@fi.uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    user_repository.add_tutors([tutor])
    user_repository.add_students([student1, student2])

    tutor_repository.add_tutor_period(3, "1C2025")

    body = {
        "students_ids": [1, 2],
        "tutor_email": "tutor@fi.uba.ar",
        "topic": "Custom topic",
    }
    params = {"period": "1C2025"}

    response = fastapi.post(f"{PREFIX}/", json=body, params=params, headers={'Authorization': f"Bearer {token.access_token}"})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_groups(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez","105000","perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A","105001","a@gmail.com")
    helper.create_student("Alejo", "B","105002","b@gmail.com")
    helper.create_student("Tomas", "C","105003","c@gmail.com")
    user_token = helper.create_student_token()
    admin_token = helper.create_admin_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(f"{PREFIX}/", json=body, params=params, headers={'Authorization': f"Bearer {user_token.access_token}"})
    assert response.status_code == status.HTTP_201_CREATED

    # Act
    response = fastapi.get(f"{PREFIX}/", params=params, headers={'Authorization': f"Bearer {admin_token.access_token}"})

    # Assert 
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert len(data[0]['students']) == 3
    assert data[0]['id'] == 1

