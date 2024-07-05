import pytest
from unittest.mock import create_autospec
from api.models import (
    TopicCategoryItem,
    TopicItem,
    TopicPreferencesItem
)
from api.services.topic_service import TopicService
from api.repositories.topic_preferences_repository import TopicPreferencesRepository
from api.repositories.topic_repository import TopicRepository
from api.exceptions import TopicCategoryDuplicated, TopicCategoryNotFound


@pytest.fixture
def mock_topic_preferences_repository(mocker):
    return create_autospec(TopicPreferencesRepository)


@pytest.fixture
def mock_topic_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_topic_repository, mock_topic_preferences_repository):
    return TopicService(mock_topic_repository, mock_topic_preferences_repository)


@pytest.mark.integration
def test_add_topic_category_with_success(service, mock_topic_repository):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_topic_repository.get_topic_category_by_name.return_value = None
    mock_topic_repository.add_topic_category.return_value = {
        "id": 1,
        "name": "category 1",
    }
    assert service.add_topic_category(topic_category) == {
        "id": 1,
        "name": "category 1",
    }


@pytest.mark.integration
def test_add_topic_category_duplicated(service, mock_topic_repository):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_topic_repository.get_topic_category_by_name.return_value = {
        "id": 1,
        "name": "category 1",
    }

    mock_topic_repository.add_topic_category.side_effect = TopicCategoryDuplicated()
    with pytest.raises(TopicCategoryDuplicated):
        service.add_topic_category(topic_category)


@pytest.mark.integration
def test_add_topic_with_success(service, mock_topic_repository):
    topic = TopicItem(name="topic 1", category="category 1")

    mock_topic_repository.get_topic_category_by_name.return_value = {
        "id": 1,
        "name": "category 1",
    }
    mock_topic_repository.get_topic.return_value = None
    mock_topic_repository.add_topic.return_value = topic
    assert service.add_topic(topic) == topic


@pytest.mark.integration
def test_add_topic_not_found(service, mock_topic_repository):
    topic = TopicItem(name="topic 1", category="category 2")

    mock_topic_repository.get_topic_category_by_name.return_value = None
    mock_topic_repository.add_topic_category.side_effect = TopicCategoryNotFound()
    with pytest.raises(TopicCategoryNotFound):
        service.add_topic(topic)


@pytest.mark.integration
def test_add_topic_preferences_with_completed_group_success(
    service, mock_topic_preferences_repository
):
    topic_preferences = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2="test2@example.com",
        email_student_3="test3@example.com",
        email_student_4="test4@example.com",
        group_id="2024-06-21T12:00:00",
        topic_1="Topic 2",
        topic_2="Topic 3",
        topic_3="Topic 1",
    )

    mock_topic_preferences_repository.get_topic_preferences_by_email.return_value = None
    mock_topic_preferences_repository.add_topic_preferences.side_effect = [
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

    result = service.add_topic_preferences(topic_preferences)
    expected_result = [
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
    assert result == expected_result


@pytest.mark.integration
def test_add_items_with_uncompleted_group_success(
    service, mock_topic_preferences_repository
):
    emails = ["test1@example.com", "test2@example.com", None, None]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2="test2@example.com",
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_topic_preferences_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
    ]

    result = service.add_items(emails, item)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_items_without_group_success(service, mock_topic_preferences_repository):
    emails = ["test1@example.com", None, None, None]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2=None,
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_topic_preferences_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }
    ]

    result = service.add_items(emails, item)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }
    ]
    assert result == expected_result
