import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import datetime as dt

from src.api.form.router import router
from src.api.topic.router import router as topic_router
from src.config.database import create_tables, drop_tables
from src.api.form.schemas import GroupFormResponse

PREFIX = "/forms"


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
    app.include_router(topic_router)
    client = TestClient(app)
    yield client


@pytest.mark.integration
def test_add_group_form_with_student_not_found(fastapi, tables):
    today = str(dt.datetime.today())
    body = {
        "uid_sender": 105285,
        "uid_student_2": 105286,
        "uid_student_3": 105287,
        "uid_student_4": 105288,
        "group_id": today,
        "topic_1": "topic1",
        "topic_2": "topic2",
        "topic_3": "topic3",
    }
    response = fastapi.post(f"{PREFIX}/groups", json=body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Student uid not found."}


# @pytest.mark.integration
# def test_add_group_form_with_success(fastapi, tables):
#     content = """
#     NOMBRE,APELLIDO,PADRON,MAIL
#     nombre1,apellido1,105285,mail1@fi.uba.ar
#     nombre2,apellido2,105286,mail2@fi.uba.ar
#     nombre3,apellido3,105287,mail3@fi.uba.ar
#     nombre4,apellido4,105288,mail4@fi.uba.ar
#     """
#     filename = "test_data"
#     content_type = "text/csv"
#     files = {"file": (filename, content, content_type)}

#     response = fastapi.post(f"students/upload", files=files)
#     assert response.status_code == 201

#     today = str(dt.datetime.today())
#     body = {
#         "uid_sender": 105285,
#         "uid_student_2": 105286,
#         "uid_student_3": 105287,
#         "uid_student_4": 105288,
#         "group_id": today,
#         "topic_1": "topic1",
#         "topic_2": "topic2",
#         "topic_3": "topic3",
#     }
#     response = fastapi.post(f"{PREFIX}/groups", json=body)
#     assert response.status_code == 201
#     assert response.json() == [
#         GroupFormResponse(
#             uid=105285,
#             group_id=today,
#             topic_1="topic1",
#             topic_2="topic2",
#             topic_3="topic3",
#         ),
#         GroupFormResponse(
#             uid=105286,
#             group_id=today,
#             topic_1="topic1",
#             topic_2="topic2",
#             topic_3="topic3",
#         ),
#         GroupFormResponse(
#             uid=105287,
#             group_id=today,
#             topic_1="topic1",
#             topic_2="topic2",
#             topic_3="topic3",
#         ),
#         GroupFormResponse(
#             uid=105288,
#             group_id=today,
#             topic_1="topic1",
#             topic_2="topic2",
#             topic_3="topic3",
#         ),
#     ]
