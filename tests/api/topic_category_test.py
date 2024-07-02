import pytest
from fastapi.testclient import TestClient

    
@pytest.fixture()
def test_app():
    from api.main import app

    with TestClient(app) as client:
        yield client

@pytest.mark.integration
def test_add_topic_category_with_success(test_app):
    item = {
        "name": "data science",
    }

    response = test_app.post("/topic_category/", json=item)
    assert response.status_code == 201

    expected_response = {
        "name": "data science",
    }
    assert response.json() == expected_response