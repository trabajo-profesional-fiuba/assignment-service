import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestApi:
    @pytest.fixture(scope="module")
    def test_app(db_session):
        from api.main import app
        with TestClient(app) as client:
            yield client
    
    def test_root(self, test_app):
        response = test_app.get("/")
        assert response.status_code == 200
        assert response.json() == "Ping"

    
    def test_add_topic_preferences_with_completed(self, test_app):
        item = {
            "email_sender": "test1@example.com",
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        }

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 201

        expected_response = [
            {
                "email": "test1@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic_1": "Topic 2",
                "topic_2": "Topic 3",
                "topic_3": "Topic 1",
            },
            {
                "email": "test2@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic_1": "Topic 2",
                "topic_2": "Topic 3",
                "topic_3": "Topic 1",
            },
            {
                "email": "test3@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic_1": "Topic 2",
                "topic_2": "Topic 3",
                "topic_3": "Topic 1",
            },
            {
                "email": "test4@example.com",
                "group_id": "2024-06-21T12:00:00",
                "topic_1": "Topic 2",
                "topic_2": "Topic 3",
                "topic_3": "Topic 1",
            },
        ]
        assert response.json() == expected_response

    
    def test_add_duplicate_topic_preferences(self, test_app):
        item = {
            "email_sender": "test1@example.com",
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        }

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 409
        assert response.json() == {"detail": "Topic preference already exists."}

    
    def test_recover_from_duplicate_exception(self, test_app):
        item = {
            "email_sender": "test1@example.com",
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        }

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 409
        assert response.json() == {"detail": "Topic preference already exists."}

        item = {
            "email_sender": "test21@example.com",
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 2",
            "topic_2": "Topic 3",
            "topic_3": "Topic 1",
        }

        response = test_app.post("/topic_preferences/", json=item)
        assert response.status_code == 201

    
    def test_update_topic_preferences(self, test_app):
        updated_item = {
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }

        response = test_app.put(
            "/topic_preferences/test1@example.com", json=updated_item
        )
        assert response.status_code == 200

        expected_response = [
            {
                "email": "test1@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic_1": "Topic 1",
                "topic_2": "Topic 2",
                "topic_3": "Topic 3",
            },
            {
                "email": "test2@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic_1": "Topic 1",
                "topic_2": "Topic 2",
                "topic_3": "Topic 3",
            },
            {
                "email": "test3@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic_1": "Topic 1",
                "topic_2": "Topic 2",
                "topic_3": "Topic 3",
            },
            {
                "email": "test4@example.com",
                "group_id": "2024-06-25T12:00:00",
                "topic_1": "Topic 1",
                "topic_2": "Topic 2",
                "topic_3": "Topic 3",
            },
        ]
        assert response.json() == expected_response

    
    def test_update_topic_preferences_when_user_not_found(self, test_app):
        updated_item = {
            "email_student_2": "test2@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }

        response = test_app.put(
            "/topic_preferences/test100@example.com", json=updated_item
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Student 'test100@example.com' not found."}

    
    def test_update_topic_preferences_when_student_from_not_found(self, test_app):
        updated_item = {
            "email_student_2": "test100@example.com",
            "email_student_3": "test3@example.com",
            "email_student_4": "test4@example.com",
            "group_id": "2024-06-25T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }

        response = test_app.put(
            "/topic_preferences/test100@example.com", json=updated_item
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Student 'test100@example.com' not found."}
