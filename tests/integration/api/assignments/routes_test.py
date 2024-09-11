import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.config.database.database import create_tables, drop_tables
from tests.integration.api.helper import ApiHelper
from src.api.assignments.router import router as assignment_router


@pytest.fixture(scope="function")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


@pytest.fixture(scope="module")
def fastapi():
    app = FastAPI()
    app.include_router(assignment_router)
    client = TestClient(app)
    yield client


PREFIX = "/assignments"


@pytest.mark.integration
def test_resolve_assignment_of_incomplete_groups(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_student("Juan", "Perez", "105285", "juanperez@fi.uba.ar")
    helper.create_student("Pedro", "Perez", "105286", "pedroperez@fi.uba.ar")
    helper.create_student("alejo", "vil", "105287", "av@fi.uba.ar")
    helper.create_student("gael", "vil", "105288", "gv@fi.uba.ar")
    helper.create_tutor("Tutor1", "Apellido", "1010", "email@fi.uba.ar")
    helper.create_tutor_period(1010, "2C2024", 1)
    helper.create_default_topics(["t1", "t2", "t3", "t4"])
    helper.add_tutor_to_topic(
        "2C2024", "email@fi.uba.ar", ["t1", "t2", "t3", "t4"], [1, 1, 1, 1]
    )
    helper.register_answer([105285, 105286], ["t1", "t2", "t3"])
    helper.register_answer([105287, 105288], ["t4", "t2", "t3"])
    admin_token = helper.create_admin_token()

    response = fastapi.post(
        f"{PREFIX}/incomplete-groups",
        params={"period_id": "2C2024"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    groups = helper.get_groups()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert len(groups) == 1


@pytest.mark.integration
def test_resolve_assignment_of_incomplete_groups_more_answers(fastapi, tables):

    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_student("Ana", "Gomez", "100001", "anagomez@example.com")
    helper.create_student("Luis", "Martinez", "100002", "luismartinez@example.com")
    helper.create_student("Maria", "Lopez", "100003", "marialopez@example.com")
    helper.create_student("Juan", "Fernandez", "100004", "juanfernandez@example.com")
    helper.create_student("Laura", "Castro", "100005", "lauracastro@example.com")
    helper.create_student("Carlos", "Sanchez", "100006", "carlossanchez@example.com")
    helper.create_student("Elena", "Rodriguez", "100007", "elenarodriguez@example.com")
    helper.create_student("Oscar", "Vargas", "100008", "oscavargas@example.com")
    helper.create_student("Sofia", "Hernandez", "100009", "sofiahernandez@example.com")
    helper.create_student("Miguel", "Morales", "100010", "miguelmorales@example.com")
    helper.create_tutor("Tutor1", "Apellido", "1010", "email@fi.uba.ar")
    helper.create_tutor("Tutor2", "Apellido", "2222", "email2@fi.uba.ar")
    helper.create_tutor_period(1010, "2C2024", 1)
    helper.create_tutor_period(2222, "2C2024", 2)
    helper.create_default_topics(
        [
            "Introduction to Python",
            "Data Structures and Algorithms",
            "Web Development with Django",
            "Machine Learning Basics",
            "Database Management Systems",
            "Version Control with Git",
        ]
    )
    helper.add_tutor_to_topic(
        "2C2024",
        "email@fi.uba.ar",
        [
            "Introduction to Python",
            "Data Structures and Algorithms",
            "Web Development with Django",
        ],
        [1, 1, 1],
    )
    helper.add_tutor_to_topic(
        "2C2024",
        "email2@fi.uba.ar",
        [
            "Machine Learning Basics",
            "Database Management Systems",
            "Version Control with Git",
        ],
        [1, 1, 1],
    )
    helper.register_answer(
        [100001, 100002],
        [
            "Introduction to Python",
            "Data Structures and Algorithms",
            "Version Control with Git",
        ],
    )
    helper.register_answer(
        [100003, 100004, 100005, 100006],
        [
            "Introduction to Python",
            "Data Structures and Algorithms",
            "Version Control with Git",
        ],
    )
    helper.register_answer(
        [100007, 100008, 100009],
        [
            "Machine Learning Basics",
            "Database Management Systems",
            "Version Control with Git",
        ],
    )
    helper.register_answer(
        [100010],
        [
            "Web Development with Django",
            "Version Control with Git",
            "Introduction to Python",
        ],
    )
    admin_token = helper.create_admin_token()

    response = fastapi.post(
        f"{PREFIX}/incomplete-groups",
        params={"period_id": "2C2024"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    groups = helper.get_groups()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert len(groups) == 3
