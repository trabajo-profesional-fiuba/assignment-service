import pytest
import requests
from fastapi.testclient import TestClient
from api.main import app
from datetime import datetime
from api.models import TopicPreferencesItem
from api.exceptions import TopicPreferencesDuplicated


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
        payload = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-21T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()
        # Convert datetime.datetime to ISO 8601 string format
        payload["group_id"] = payload["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=payload)
        assert response.status_code == 201
        assert response.json() == payload

    @pytest.mark.api
    def test_add_duplicate_topic_preferences(self, test_app):
        """Test POST /topic_preferences/ endpoint."""
        payload = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-21T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()
        payload["group_id"] = payload["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=payload)
        assert response.status_code == 409

    @pytest.mark.api
    def test_update_topic_preferences(self, test_app):
        """Test PUT /topic_preferences/ endpoint."""
        payload = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-21T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()
        payload["group_id"] = payload["group_id"].isoformat()
        test_app.post("/topic_preferences/", json=payload)
        topic_preferences_item = TopicPreferencesItem(**payload)

        topic_preferences_item.group_id = "2024-06-25T12:00:00"
        topic_preferences_item.topic1 = "Topic 2"
        topic_preferences_item.topic2 = "Topic 3"
        topic_preferences_item.topic3 = "Topic 4"
        updated_payload = topic_preferences_item.model_dump()

        response = test_app.patch(
            "/topic_preferences/test@example.com", json=updated_payload
        )
        assert response.status_code == 200
        assert response.json() == updated_payload
