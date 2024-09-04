import datetime as dt
import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.config.database.database import create_tables, drop_tables
from tests.integration.api.helper import ApiHelper
from src.api.assigments.router import router as assigment_router

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
    app.include_router(assigment_router)
    client = TestClient(app)
    yield client


PREFIX = "/assigments"

@pytest.mark.integration
def test_resolve_assigment_of_incomplete_groups(fastapi, tables):

    # Arrange
    helper = ApiHelper()
    helper.create_period("2C2024")
    helper.create_student("Juan","Perez", "105285","juanperez@fi.uba.ar")
    helper.create_student("Pedro","Perez", "105286","pedroperez@fi.uba.ar")
    helper.create_student("alejo","vil", "105287","av@fi.uba.ar")
    helper.create_student("gael","vil", "105288","gv@fi.uba.ar")
    helper.create_tutor("Tutor1", "Apellido","1010","email@fi.uba.ar")
    helper.create_tutor_period(1010, "2C2024", 1)
    helper.create_default_topics(["t1","t2","t3","t4"])
    helper.add_tutor_to_topic("2C2024","email@fi.uba.ar", ["t1","t2","t3","t4"], [1,1,1,1] )
    helper.register_answer([105285,105286],["t1","t2","t3"])
    helper.register_answer([105287,105288],["t4","t2","t3"])
    admin_token = helper.create_admin_token()

    response = fastapi.post(
        f"{PREFIX}/incomplete-groups",
        params={"period_id": "2C2024"},
        headers={"Authorization": f"Bearer {admin_token.access_token}"},
    )
 
    groups = helper.get_groups()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert len(groups) == 1





