import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from api.repository import Repository
from api.models import TopicPreferencesItem


class TestRepository:
    @pytest.fixture
    def mock_repository(self):
        mock_db_session = Mock(spec=Session)
        repo = Repository(mock_db_session)
        yield repo

    def test_add_topic_preferences_success(self, mock_repository):
        topic_preferences_data = {
            "email": "test@example.com",
            "group_id": "2024-06-22 12:00:00",
            "topic1": "Technology",
            "topic2": "Science",
            "topic3": "Art",
        }

        topic_preferences_item = TopicPreferencesItem(**topic_preferences_data)
        result = mock_repository.add_topic_preferences(topic_preferences_item)

        assert result.email == topic_preferences_item.email
        assert result.group_id == topic_preferences_item.group_id
        assert result.topic1 == topic_preferences_item.topic1
        assert result.topic2 == topic_preferences_item.topic2
        assert result.topic3 == topic_preferences_item.topic3

    def test_add_duplicate_topic_preferences_success(self, mock_repository):
        topic_preferences_data = {
            "email": "test@example.com",
            "group_id": "2024-06-22 12:00:00",
            "topic1": "Technology",
            "topic2": "Science",
            "topic3": "Art",
        }

        topic_preferences_item = TopicPreferencesItem(**topic_preferences_data)
        result = mock_repository.add_topic_preferences(topic_preferences_item)
        result = mock_repository.add_topic_preferences(topic_preferences_item)

        assert result.email == topic_preferences_item.email
        assert result.group_id == topic_preferences_item.group_id
        assert result.topic1 == topic_preferences_item.topic1
        assert result.topic2 == topic_preferences_item.topic2
        assert result.topic3 == topic_preferences_item.topic3

    def test_update_topic_preferences_success(self, mock_repository):
        topic_preferences_data = {
            "email": "test@example.com",
            "group_id": "2024-06-22 12:00:00",
            "topic1": "Technology",
            "topic2": "Science",
            "topic3": "Art",
        }
        topic_preferences_item = TopicPreferencesItem(**topic_preferences_data)
        result = mock_repository.update_topic_preferences(
            "test@example.com", topic_preferences_item
        )

        update_topic_preferences_data = {
            "email": "test@example.com",
            "group_id": "2024-06-25 12:00:00",
            "topic1": "Technology",
            "topic2": "Science",
            "topic3": "Art",
        }
        update_topic_preferences_item = TopicPreferencesItem(
            **update_topic_preferences_data
        )
        result = mock_repository.update_topic_preferences(
            "test@example.com", update_topic_preferences_item
        )

        assert result.email == topic_preferences_item.email
        assert result.group_id == update_topic_preferences_item.group_id
        assert result.topic1 == topic_preferences_item.topic1
        assert result.topic2 == topic_preferences_item.topic2
        assert result.topic3 == topic_preferences_item.topic3
