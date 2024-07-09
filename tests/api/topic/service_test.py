import pytest
from unittest.mock import create_autospec
from src.api.topic.schemas import TopicCategoryItem, TopicItem, TopicPreferencesItem
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.api.topic.exceptions import (
    TopicCategoryDuplicated,
    TopicCategoryNotFound,
    StudentEmailDuplicated,
)


@pytest.fixture
def mock_topic_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_topic_repository):
    return TopicService(mock_topic_repository)


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

    mock_topic_repository.get_topic_category_by_name.return_value = TopicCategoryItem(
        name="category 1",
    )
    mock_topic_repository.get_topic_by_name_and_category.return_value = None
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
def test_filter_student_emails_without_none_emails(service):
    emails = ["test1", "test2", "test3", "test4"]
    result = service.filter_student_emails(emails)

    assert len(result) == 4
    assert result == emails


@pytest.mark.integration
def test_filter_student_emails_with_some_none_emails(service):
    emails = ["test1", "test2", None, None]
    result = service.filter_student_emails(emails)

    assert len(result) == 2
    assert result == ["test1", "test2"]


@pytest.mark.integration
def test_filter_student_emails_with_all_none_emails(service):
    emails = [None, None, None, None]
    result = service.filter_student_emails(emails)

    assert len(result) == 0
    assert result == []


@pytest.mark.integration
def test_add_topic_preferences_with_completed_group_success(
    service, mock_topic_repository
):
    topic_preferences = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2="test2@example.com",
        email_student_3="test3@example.com",
        email_student_4="test4@example.com",
        group_id="2024-06-21T12:00:00",
        topic_1="topic 1",
        category_1="topic 1",
        topic_2="topic 1",
        category_2="topic 1",
        topic_3="topic 1",
        category_3="topic 1",
    )

    mock_topic_repository.get_topic_preferences_by_email.side_effect = [
        None,
        None,
        None,
        None,
    ]
    mock_topic_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]

    result = service.add_topic_preferences(topic_preferences)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_topic_preferences_with_uncompleted_group_success(
    service, mock_topic_repository
):
    emails = ["test1@example.com", "test2@example.com"]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2="test2@example.com",
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="topic 1",
        topic_2="topic 1",
        category_2="topic 1",
        topic_3="topic 1",
        category_3="topic 1",
    )

    mock_topic_repository.get_topic_preferences_by_email.side_effect = [
        None,
        None,
        None,
        None,
    ]
    mock_topic_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]

    result = service.add_all_topic_preferences(emails, item)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_topic_preferences_without_group_success(service, mock_topic_repository):
    emails = ["test1@example.com"]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2=None,
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="category 1",
        topic_2="topic 1",
        category_2="category 1",
        topic_3="topic 1",
        category_3="category 1",
    )

    mock_topic_repository.get_topic_preferences_by_email.side_effect = [
        None,
        None,
        None,
        None,
    ]
    mock_topic_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        }
    ]

    result = service.add_all_topic_preferences(emails, item)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        }
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_topic_preferences_duplicated(service, mock_topic_repository):
    emails = ["test1@example.com"]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2=None,
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="category 1",
        topic_2="topic 1",
        category_2="category 1",
        topic_3="topic 1",
        category_3="category 1",
    )

    mock_topic_repository.get_topic_preferences_by_email.return_value = {
        "email": "test1@example.com",
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 1",
        "category_1": "category 1",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }

    with pytest.raises(StudentEmailDuplicated):
        service.add_all_topic_preferences(emails, item)
