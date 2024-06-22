import pytest
import requests
from fastapi.testclient import TestClient
from api.main import app
from datetime import datetime


class TestApi:
    @pytest.fixture(scope="module")
    def test_app(self):
        """Create a FastAPI test client."""
        return TestClient(app)

    def test_root(self, test_app):
        response = test_app.get("/")
        assert response.status_code == 200
        assert response.json() == "Ping"

    @pytest.mark.api
    def test_add_topic_preferences(self, test_app):
        """Test POST /topic_preferences/ endpoint."""
        payload = {
            "email": "test@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic1": "Topic 1",
            "topic2": "Topic 2",
            "topic3": "Topic 3",
        }

        response = test_app.post("/topic_preferences/", json=payload)
        assert response.status_code == 201
        assert response.json() == payload

    @pytest.mark.api
    def test_add_duplicate_topic_preferences(self, test_app):
        """Test POST /topic_preferences/ endpoint."""
        payload = {
            "email": "test@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic1": "Topic 1",
            "topic2": "Topic 2",
            "topic3": "Topic 3",
        }

        test_app.post("/topic_preferences/", json=payload)
        response = test_app.post("/topic_preferences/", json=payload)
        assert response.status_code == 201
        assert response.json() == payload

    @pytest.mark.api
    def test_update_topic_preferences(self, test_app):
        """Test PUT /topic_preferences/ endpoint."""
        payload = {
            "email": "test@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic1": "Topic 2",
            "topic2": "Topic 3",
            "topic3": "Topic 1",
        }
        test_app.post("/topic_preferences/", json=payload)
        updated_payload = {
            "email": "test@example.com",
            "group_id": "2024-06-25T12:00:00",
            "topic1": "Topic 2",
            "topic2": "Topic 3",
            "topic3": "Topic 1",
        }
        response = test_app.patch("/topic_preferences/test@example.com", json=payload)
        assert response.status_code == 200
        assert response.json() == payload
