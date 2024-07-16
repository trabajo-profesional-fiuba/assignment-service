import pytest
from unittest.mock import create_autospec
from src.api.topic.schemas import (
    TopicCategoryRequest,
    TopicRequest,
    TopicPreferencesRequest,
)
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.api.topic.exceptions import (
    TopicCategoryDuplicated,
    TopicCategoryNotFound,
    UidDuplicated,
    TopicNotFound,
)


@pytest.fixture
def mock_topic_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_topic_repository):
    return TopicService(mock_topic_repository)


@pytest.mark.integration
def test_add_topic_category_with_success(service, mock_topic_repository):
    topic_category = TopicCategoryRequest(
        name="category 1",
    )

    mock_topic_repository.get_topic_category_by_name.return_value = None
    mock_topic_repository.add_category.return_value = {
        "id": 1,
        "name": "category 1",
    }
    assert service.add_category(topic_category) == {
        "id": 1,
        "name": "category 1",
    }


@pytest.mark.integration
def test_add_topic_category_duplicated(service, mock_topic_repository):
    topic_category = TopicCategoryRequest(
        name="category 1",
    )

    mock_topic_repository.get_topic_category_by_name.return_value = {
        "id": 1,
        "name": "category 1",
    }

    mock_topic_repository.add_category.side_effect = TopicCategoryDuplicated()
    with pytest.raises(TopicCategoryDuplicated):
        service.add_category(topic_category)


@pytest.mark.integration
def test_add_topic_with_success(service, mock_topic_repository):
    topic = TopicRequest(name="topic 1", category="category 1")

    mock_topic_repository.get_topic_category_by_name.return_value = (
        TopicCategoryRequest(
            name="category 1",
        )
    )
    mock_topic_repository.get_topic_by_name_and_category.return_value = None
    mock_topic_repository.add_topic.return_value = topic
    assert service.add_topic(topic) == topic


@pytest.mark.integration
def test_add_topic_not_found(service, mock_topic_repository):
    topic = TopicRequest(name="topic 1", category="category 2")

    mock_topic_repository.get_topic_category_by_name.side_effect = (
        TopicCategoryNotFound("category 2")
    )
    with pytest.raises(TopicCategoryNotFound):
        service.add_topic_category_if_not_duplicated(topic)


@pytest.mark.integration
def test_filter_student_uids_without_none_uids(service):
    uids = [111111, 111112, 111113, 111114]
    result = service.filter_student_uids(uids)

    assert len(result) == 4
    assert result == uids


@pytest.mark.integration
def test_filter_student_uids_with_some_none_uids(service):
    uids = [111111, 111112, None, None]
    result = service.filter_student_uids(uids)

    assert len(result) == 2
    assert result == [111111, 111112]


@pytest.mark.integration
def test_filter_student_uids_with_all_none_uids(service):
    uids = [None, None, None, None]
    result = service.filter_student_uids(uids)

    assert len(result) == 0
    assert result == []


@pytest.mark.integration
def test_add_topic_preferences_with_completed_group_success(
    service, mock_topic_repository
):
    topic_preferences = TopicPreferencesRequest(
        uid_sender=111111,
        uid_student_2=111112,
        uid_student_3=111113,
        uid_student_4=111114,
        group_id="2024-06-21T12:00:00",
        topic_1="topic 1",
        category_1="topic 1",
        topic_2="topic 1",
        category_2="topic 1",
        topic_3="topic 1",
        category_3="topic 1",
    )

    mock_topic_repository.get_topic_preferences_by_uid.return_value = None
    mock_topic_repository.add_preferences.side_effect = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111112,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111113,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111114,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]

    result = service.add_preferences(topic_preferences)
    expected_result = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111112,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111113,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111114,
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
    uids = [111111, 111112]
    item = TopicPreferencesRequest(
        uid_sender=111111,
        uid_student_2=111112,
        uid_student_3=None,
        uid_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="topic 1",
        topic_2="topic 1",
        category_2="topic 1",
        topic_3="topic 1",
        category_3="topic 1",
    )

    mock_topic_repository.get_topic_preferences_by_uid.return_value = None
    mock_topic_repository.add_preferences.side_effect = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111112,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
    ]

    result = service.add_all_topic_preferences(uids, item)
    expected_result = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        },
        {
            "uid": 111112,
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
    uids = [111111]
    item = TopicPreferencesRequest(
        uid_sender=111111,
        uid_student_2=None,
        uid_student_3=None,
        uid_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="category 1",
        topic_2="topic 1",
        category_2="category 1",
        topic_3="topic 1",
        category_3="category 1",
    )

    mock_topic_repository.get_topic_preferences_by_uid.return_value = None
    mock_topic_repository.add_preferences.side_effect = [
        {
            "uid": 111111,
            "group_id": "2024-06-21T12:00:00",
            "topic_1": "topic 1",
            "category_1": "category 1",
            "topic_2": "topic 1",
            "category_2": "category 1",
            "topic_3": "topic 1",
            "category_3": "category 1",
        }
    ]

    result = service.add_all_topic_preferences(uids, item)
    expected_result = [
        {
            "uid": 111111,
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
    uids = [111111]
    item = TopicPreferencesRequest(
        uid_sender=111111,
        uid_student_2=None,
        uid_student_3=None,
        uid_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 1",
        category_1="category 1",
        topic_2="topic 1",
        category_2="category 1",
        topic_3="topic 1",
        category_3="category 1",
    )

    mock_topic_repository.get_topic_preferences_by_uid.return_value = {
        "uid": 111111,
        "group_id": "2024-06-21T12:00:00",
        "topic_1": "topic 1",
        "category_1": "category 1",
        "topic_2": "topic 1",
        "category_2": "category 1",
        "topic_3": "topic 1",
        "category_3": "category 1",
    }

    with pytest.raises(UidDuplicated):
        service.add_all_topic_preferences(uids, item)


@pytest.mark.integration
def test_add_topic_preferences_with_topic_not_found(service, mock_topic_repository):
    uids = [111111]
    item = TopicPreferencesRequest(
        uid_sender=111111,
        uid_student_2=None,
        uid_student_3=None,
        uid_student_4=None,
        group_id="2024-06-25T12:00:00",
        topic_1="topic 2",
        category_1="category 1",
        topic_2="topic 1",
        category_2="category 1",
        topic_3="topic 1",
        category_3="category 1",
    )

    mock_topic_repository.get_topic_preferences_by_uid.return_value = None
    mock_topic_repository.add_preferences.side_effect = TopicNotFound(
        "topic 2", "category 1"
    )

    with pytest.raises(TopicNotFound):
        service.add_all_topic_preferences(uids, item)


@pytest.mark.integration
def test_get_all_topic_categories_with_success(service, mock_topic_repository):
    topic_categories = [
        {"name": "category 1"},
        {"name": "category 2"},
        {"name": "category 3"},
    ]

    mock_topic_repository.get_categories.return_value = topic_categories

    result = service.get_categories()
    assert len(result) == 3
    assert result == topic_categories


@pytest.mark.integration
def test_get_empty_all_topic_categories_with_success(service, mock_topic_repository):
    topic_categories = []
    mock_topic_repository.get_categories.return_value = topic_categories

    result = service.get_categories()
    assert len(result) == 0
    assert result == topic_categories
