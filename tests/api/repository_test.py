import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from api.repository import Repository
from api.models import TopicPreferencesItem
from api.exceptions import TopicPreferencesDuplicated


class TestRepository:
    @pytest.fixture
    def mock_repository(self):
        mock_db_session = Mock(spec=Session)
        repo = Repository(mock_db_session)
        yield repo

    def test_add_topic_preferences(self, mock_repository):
        payload = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-25T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()

        topic_preferences_item = TopicPreferencesItem(**payload)
        result = mock_repository.add_topic_preferences(
            topic_preferences_item.email, topic_preferences_item
        )

        assert result.email == topic_preferences_item.email
        assert result.group_id == topic_preferences_item.group_id
        assert result.topic1 == topic_preferences_item.topic1
        assert result.topic2 == topic_preferences_item.topic2
        assert result.topic3 == topic_preferences_item.topic3

    def test_update_all_topic_preferences(self, mock_repository):
        payload = TopicPreferencesItem(
            email="test@example.com",
            email_student_group_2="test2@example.com",
            email_student_group_3="test3@example.com",
            email_student_group_4="test4@example.com",
            group_id="2024-06-22T12:00:00",
            topic1="Topic 2",
            topic2="Topic 3",
            topic3="Topic 1",
        ).model_dump()
        payload["group_id"] = payload["group_id"].isoformat()
        topic_preferences_item = TopicPreferencesItem(**payload)
        mock_repository.add_topic_preferences(
            topic_preferences_item.email, topic_preferences_item
        )

        topic_preferences_item.group_id = "2024-06-25T12:00:00"
        topic_preferences_item.topic1 = "Topic 2"
        topic_preferences_item.topic2 = "Topic 3"
        topic_preferences_item.topic3 = "Topic 4"
        updated_payload = topic_preferences_item.model_dump()

        update_topic_preferences_item = TopicPreferencesItem(**updated_payload)
        result = mock_repository.update_topic_preferences(
            topic_preferences_item.email, update_topic_preferences_item
        )

        assert result.email == topic_preferences_item.email
        assert result.group_id == update_topic_preferences_item.group_id
        assert result.topic1 == topic_preferences_item.topic1
        assert result.topic2 == topic_preferences_item.topic2
        assert result.topic3 == topic_preferences_item.topic3
