import pytest
import requests
from fastapi.testclient import TestClient
from api.main import app
from datetime import datetime
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
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
    def test_add_topic_preferences_with_completed_group(self, test_app):
        """Test POST /topic_preferences/ endpoint."""
        item = TopicPreferencesItem(
            email="test1@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-21T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()

        # Convert datetime to ISO 8601 string format
        item["group_id"] = item["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 201

        expected_response = [
            {
                "email": "test1@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic1": "Topic 2",
                "topic2": "Topic 3",
                "topic3": "Topic 1",
            },
            {
                "email": "test2@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic1": "Topic 2",
                "topic2": "Topic 3",
                "topic3": "Topic 1",
            },
            {
                "email": "test3@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic1": "Topic 2",
                "topic2": "Topic 3",
                "topic3": "Topic 1",
            },
            {
                "email": "test4@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic1": "Topic 2",
                "topic2": "Topic 3",
                "topic3": "Topic 1",
            },
        ]
        assert response.json() == expected_response

    @pytest.mark.api
    def test_add_duplicate_topic_preferences(self, test_app):
        """Test POST /topic_preferences/ endpoint."""
        item = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-21T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()
        item["group_id"] = item["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 409

    @pytest.mark.api
    # @pytest.mark.skip(reason="Debug")
    def test_update_topic_preferences(self, test_app):
        """Test PUT /topic_preferences/ endpoint."""
        updated_item = TopicPreferencesUpdatedItem(
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-25T12:00:00",
            topic1="Topic 1",
            topic2="Topic 2",
            topic3="Topic 3",
        ).model_dump()
        updated_item["group_id"] = updated_item["group_id"].isoformat()

        response = test_app.put(
            "/topic_preferences/test1@example.com", json=updated_item
        )
        assert response.status_code == 200

        expected_response = [
            {
                "email": "test1@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic1": "Topic 1",
                "topic2": "Topic 2",
                "topic3": "Topic 3",
            },
            {
                "email": "test2@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic1": "Topic 1",
                "topic2": "Topic 2",
                "topic3": "Topic 3",
            },
            {
                "email": "test3@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic1": "Topic 1",
                "topic2": "Topic 2",
                "topic3": "Topic 3",
            },
            {
                "email": "test4@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic1": "Topic 1",
                "topic2": "Topic 2",
                "topic3": "Topic 3",
            },
        ]
        assert response.json() == expected_response
