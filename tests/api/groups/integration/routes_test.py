import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient


from src.api.topic.models import Category
from src.api.topic.repository import TopicRepository
from src.api.groups.router import router

from src.api.tutors.model import Period
from src.api.tutors.repository import TutorRepository
from src.api.users.model import User, Role
from src.api.users.repository import UserRepository
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

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
    topic_repository = TopicRepository(Session)
    topic_repository.add_category(Category(name="default"))
    tutor_repository = TutorRepository(Session)
    tutor_repository.add_period(Period(id="1C2025"))

    user_repository = UserRepository(Session)
    tutor = User(
        id=3,
        name="Pedro",
        last_name="Pipo",
        email="tutor@fi,uba.ar",
        password="password1",
        role=Role.TUTOR,
    )
    student1 = User(
        id=1,
        name="Juan",
        last_name="Perez",
        email="1@fi,uba.ar",
        password="password",
        role=Role.STUDENT,
    )
    student2 = User(
        id=2,
        name="Pedro",
        last_name="Pipo",
        email="2@fi,uba.ar",
        password="password1",
        role=Role.STUDENT,
    )
    user_repository.add_tutors([tutor])
    user_repository.add_students([student1, student2])

    tutor_repository.add_tutor_period(3, "1C2025")

    body = {
        "students": [1, 2],
        "tutor_email": "tutor@fi,uba.ar",
        "topic": {"name": "Custom topic", "category": "default"},
    }
    params = {"period": "1C2025"}

    response = fastapi.post(f"{PREFIX}/", json=body, params=params)
    assert response.status_code == status.HTTP_201_CREATED
