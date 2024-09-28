import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.groups.router import router
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tests.integration.api.helper import ApiHelper

PREFIX = "/groups"


@pytest.fixture(scope="function")
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
def test_add_assigned_group_and_get_one_group(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")

    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
def test_get_groups_by_period(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    user_token = helper.create_student_token()
    admin_token = helper.create_admin_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Act
    params = {"period": "1C2025"}
    response = fastapi.get(
        f"{PREFIX}/",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1


@pytest.mark.integration
def test_post_groups_with_tutor_not_in_db_returns_not_found(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "The tutor does not exist or this period is not present"
    )


@pytest.mark.integration
def test_post_groups_with_one_student_not_in_db_returns_not_found(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    user_token = helper.create_student_token()

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Some ids are not in database"


@pytest.mark.integration
def test_post_groups_without_token(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")

    body = {
        "students_ids": [105001, 105002, 105003],
        "tutor_email": "perez@gmail.com",
        "topic": "My custom topic",
    }
    params = {"period": "1C2025"}
    response = fastapi.post(f"{PREFIX}/", json=body, params=params)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_put_confirmed_groups(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    helper.create_topic("Basic topic")
    group = helper.create_basic_group([105001, 105002, 105003], [1, 2, 3], "1C2025")
    admin_token = helper.create_admin_token()

    body = [{"id": group.id, "tutor_period_id": 1, "topic_id": 1}]
    params = {"period": "1C2025"}
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    groups = response.json()
    assert len(groups) == 1
    first = groups[0]
    assert first["id"] == 1
    assert first["topic_id"] == 1
    assert first["tutor_period_id"] == 1


@pytest.mark.integration
def test_put_confirmed_groups_tutor_period_id_not_exist(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    helper.create_topic("Basic topic")
    group = helper.create_basic_group([105001, 105002, 105003], [1, 2, 3], "1C2025")
    admin_token = helper.create_admin_token()

    body = [{"id": group.id, "tutor_period_id": 10, "topic_id": 1}]
    params = {"period": "1C2025"}
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_put_confirmed_groups_topic_id_not_exist(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    helper.create_topic("Basic topic")
    group = helper.create_basic_group([105001, 105002, 105003], [1, 2, 3], "1C2025")
    admin_token = helper.create_admin_token()

    body = [{"id": group.id, "tutor_period_id": 1, "topic_id": 3}]
    params = {"period": "1C2025"}
    response = fastapi.put(
        f"{PREFIX}/",
        json=body,
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_post_groups_initial_project(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    period = helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="1C2025",
    )
    user_token = helper.create_student_token()

    with open("tests/test.pdf", "rb") as file:
        content = file.read()

    filename = "test"
    content_type = "application/pdf"
    files = {"file": (filename, content, content_type)}
    response = fastapi.post(
        f"{PREFIX}/{group.id}/initial-project",
        files=files,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_download_group_initial_project(fastapi):
    # Arrange
    helper = ApiHelper()
    admin_token = helper.create_admin_token()
    params = {"period": "1C2025"}

    response = fastapi.get(
        f"{PREFIX}/1/initial-project",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    with open("tests/test.pdf", "rb") as file:
        expected_file = file.read()
    assert expected_file == response.content


@pytest.mark.integration
def test_all_groups_initial_project_details(fastapi):
    # Arrange
    helper = ApiHelper()
    admin_token = helper.create_admin_token()
    params = {"period": "1C2025"}

    response = fastapi.get(
        f"{PREFIX}/initial-project",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    blob = response.json()[0]
    blob["name"] = "1C2025/1/initial-project.pdf"
    blob["container"] = "dev"


@pytest.mark.integration
def test_get_groups_by_id(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    period = helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="1C2025",
    )
    user_token = helper.create_student_token(105001)
    params = {"period": "1C2025"}

    response = fastapi.get(
        f"{PREFIX}/states/{group.id}",
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_get_groups_by_id_fails_if_user_doesnt_belong_to_group(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    period = helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="1C2025",
    )
    user_token = helper.create_student_token(105001)
    params = {"period": "1C2025"}

    response = fastapi.get(
        f"{PREFIX}/states/{10}",
        params=params,
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
def test_get_groups_by_id_being_admin(fastapi, tables):
    # Arrange
    helper = ApiHelper()
    helper.create_period("1C2025")
    helper.create_tutor("Juan", "Perez", "105000", "perez@gmail.com")
    period = helper.create_tutor_period("105000", "1C2025")
    helper.create_student("Pedro", "A", "105001", "a@gmail.com")
    helper.create_student("Alejo", "B", "105002", "b@gmail.com")
    helper.create_student("Tomas", "C", "105003", "c@gmail.com")
    topic = helper.create_topic("TopicCustom")
    group = helper.create_group(
        ids=[105001, 105002, 105003],
        tutor_period_id=period.id,
        topic_id=topic.id,
        period_id="1C2025",
    )
    admin_token = helper.create_admin_token()
    params = {"period": "1C2025"}

    response = fastapi.get(
        f"{PREFIX}/states/{group.id}",
        params=params,
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
