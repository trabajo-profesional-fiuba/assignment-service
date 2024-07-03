import pytest
from unittest.mock import create_autospec
from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.topic_preferences_repository import TopicPreferencesRepository
from api.services.topic_preferences_service import TopicPreferencesService
from api.exceptions import TopicPreferencesDuplicated


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicPreferencesRepository)


@pytest.fixture
def service(mock_repository):
    return TopicPreferencesService(mock_repository)


@pytest.mark.integration
def test_add_topic_preferences(service, mock_repository):
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

    mock_repository.add_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
    ]

    result = service.add_topic_preferences(topic_preferences)
    expected_result = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test2@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1=": "Topic 2",
            "topic_2=": "Topic 3",
            "topic_3=": "Topic 1",
        },
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_topic_preferences_duplicated_exception(service, mock_repository):
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

    mock_repository.add_topic_preferences.side_effect = TopicPreferencesDuplicated(
        "Duplicated entry"
    )

    with pytest.raises(TopicPreferencesDuplicated) as err:
        service.add_topic_preferences(topic_preferences)


@pytest.mark.integration
def test_add_items_with_completed(service, mock_repository):
    emails = [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "test4@example.com",
    ]
    item = TopicPreferencesItem(
        email_sender="test1@example.com",
        email_student_2="test2@example.com",
        email_student_3="test3@example.com",
        email_student_4="test4@example.com",
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_repository.add_topic_preferences.side_effect = [
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
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test4@example.com",
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
        {
            "email": "test3@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
        {
            "email": "test4@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        },
    ]
    assert result == expected_result


@pytest.mark.integration
def test_add_items_with_uncompleted(service, mock_repository):
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

    mock_repository.add_topic_preferences.side_effect = [
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
def test_add_items_without(service, mock_repository):
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

    mock_repository.add_topic_preferences.side_effect = [
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


@pytest.mark.integration
def test_update_items_with_completed(service, mock_repository):
    emails = [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com",
        "test4@example.com",
    ]
    updated_item = TopicPreferencesUpdatedItem(
        email_student_2="test2@example.com",
        email_student_3="test3@example.com",
        email_student_4="test4@example.com",
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_repository.update_topic_preferences.side_effect = [
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

    result = service.update_items(emails, updated_item)
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
def test_update_items_with_uncompleted(service, mock_repository):
    emails = ["test1@example.com", "test2@example.com", None, None]
    updated_item = TopicPreferencesUpdatedItem(
        email_student_2="test2@example.com",
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_repository.update_topic_preferences.side_effect = [
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
    ]

    result = service.update_items(emails, updated_item)
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
    ]
    assert result == expected_result


@pytest.mark.integration
def test_update_items_without(service, mock_repository):
    emails = ["test1@example.com", None, None, None]
    updated_item = TopicPreferencesUpdatedItem(
        email_student_2=None,
        email_student_3=None,
        email_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="Topic 1",
        topic_2="Topic 2",
        topic_3="Topic 3",
    )

    mock_repository.update_topic_preferences.side_effect = [
        {
            "email": "test1@example.com",
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "Topic 1",
            "topic_2": "Topic 2",
            "topic_3": "Topic 3",
        }
    ]

    result = service.update_items(emails, updated_item)
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
