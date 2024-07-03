import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem, TopicItem
from api.services.topic_service import TopicService
from api.repositories.topic_repository import TopicRepository
from api.exceptions import TopicCategoryDuplicated, TopicCategoryNotFound


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_repository):
    return TopicService(mock_repository)


@pytest.mark.integration
def test_add_topic_category_with_success(service, mock_repository):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_repository.get_topic_category_by_name.return_value = None
    mock_repository.add_topic_category.return_value = {"id": 1, "name": "category 1"}
    assert service.add_topic_category(topic_category) == {
        "id": 1,
        "name": "category 1",
    }


@pytest.mark.integration
def test_add_topic_category_duplicated(service, mock_repository):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_repository.get_topic_category_by_name.return_value = {
        "id": 1,
        "name": "category 1",
    }

    mock_repository.add_topic_category.side_effect = TopicCategoryDuplicated()
    with pytest.raises(TopicCategoryDuplicated):
        service.add_topic_category(topic_category)


@pytest.mark.integration
def test_add_topic_with_success(service, mock_repository):
    topic = TopicItem(name="topic 1", category="category 1")

    mock_repository.add_topic.return_value = topic
    assert service.add_topic(topic) == topic


@pytest.mark.integration
def test_add_topic_not_found(service, mock_repository):
    topic = TopicItem(name="topic 1", category="category 2")

    mock_repository.get_topic_category_by_name.return_value = None
    mock_repository.add_topic_category.side_effect = TopicCategoryNotFound()
    with pytest.raises(TopicCategoryNotFound):
        service.add_topic(topic)
