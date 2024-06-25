import pytest
import requests
from fastapi.testclient import TestClient
from api.main import app
from datetime import datetime
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.exceptions import TopicPreferencesDuplicated
from storage.database import Database
from storage.topic_preferences_table import TopicPreferences


class TestApi:
    # Dependency function for FastAPI
    def get_db(self):
        db = Database()
        try:
            yield db.setup()
        finally:
            db.engine.dispose()

    @pytest.fixture(scope="module")
    def test_app(self):
        """
        Fixture to provide a FastAPI TestClient with a session dependency override.
        """
        db_instance = Database()
        db_session = db_instance.setup()
        db_instance.delete_all_records_from_table(db_session, TopicPreferences)

        def override_get_db():
            try:
                yield db_session
            finally:
                db_session.close()

        app.dependency_overrides[self.get_db] = override_get_db

        with TestClient(app) as c:
            yield c

        # Clean up after all tests are done
        db_instance.delete_all_records_from_table(db_session, TopicPreferences)
        db_instance.engine.dispose()

    @pytest.mark.integration
    def test_root(self, test_app):
        response = test_app.get("/")
        assert response.status_code == 200
        assert response.json() == "Ping"

    @pytest.mark.integration
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

    @pytest.mark.integration
    def test_add_duplicate_topic_preferences(self, test_app):
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
        item["group_id"] = item["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 409
        assert response.json() == {"detail": "Topic preference already exists."}

    @pytest.mark.integration
    def test_recover_from_duplicate_exception(self, test_app):
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
        item["group_id"] = item["group_id"].isoformat()

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 409
        assert response.json() == {"detail": "Topic preference already exists."}

        item = TopicPreferencesItem(
            email="test21@example.com",
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
        assert response.status_code == 201

    @pytest.mark.integration
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

    @pytest.mark.integration
    def test_update_topic_preferences_when_user_not_found(self, test_app):
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
            "/topic_preferences/test100@example.com", json=updated_item
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Student 'test100@example.com' not found."}

    @pytest.mark.integration
    def test_update_topic_preferences_when_student_from_group_not_found(self, test_app):
        """Test PUT /topic_preferences/ endpoint."""
        updated_item = TopicPreferencesUpdatedItem(
            email_student_group_2="test100@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-25T12:00:00",
            topic1="Topic 1",
            topic2="Topic 2",
            topic3="Topic 3",
        ).model_dump()
        updated_item["group_id"] = updated_item["group_id"].isoformat()

        response = test_app.put(
            "/topic_preferences/test100@example.com", json=updated_item
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Student 'test100@example.com' not found."}
