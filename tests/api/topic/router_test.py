import pytest
from unittest.mock import create_autospec
from src.api.topic.schemas import (
    TopicCategoryRequest,
    TopicRequest,
)
from src.api.topic.router import TopicController
from src.api.topic.service import TopicService
from src.api.topic.exceptions import TopicCategoryDuplicated, TopicCategoryNotFound


@pytest.fixture
def mock_service(mocker):
    return create_autospec(TopicService)


@pytest.fixture
def controller(mock_service):
    return TopicController(mock_service)


@pytest.mark.integration
def test_add_topic_category_with_success(controller, mock_service):
    topic_category = TopicCategoryRequest(
        name="category 1",
    )

    mock_service.add_topic_category.return_value = topic_category
    assert controller.add_topic_category(topic_category) == {"name": "category 1"}


@pytest.mark.integration
def test_add_topic_category_duplicated(controller, mock_service):
    topic_category = TopicCategoryRequest(
        name="category 1",
    )

    mock_service.add_topic_category.side_effect = TopicCategoryDuplicated()

    with pytest.raises(TopicCategoryDuplicated):
        controller.add_topic_category(topic_category)


@pytest.mark.integration
def test_add_topic_with_success(controller, mock_service):
    topic = TopicRequest(name="topic 1", category="category 1")

    mock_service.add_topic.return_value = topic
    assert controller.add_topic(topic) == topic


@pytest.mark.integration
def test_add_topic_not_found(controller, mock_service):
    topic = TopicRequest(name="topic 1", category="category 2")

    mock_service.add_topic.side_effect = TopicCategoryNotFound("category 2")

    with pytest.raises(TopicCategoryNotFound):
        controller.add_topic(topic)


@pytest.mark.integration
def test_get_all_topic_categories_with_success(controller, mock_service):
    topic_categories = [
        {"name": "category 1"},
        {"name": "category 2"},
        {"name": "category 3"},
    ]
    mock_service.get_all_topic_categories.return_value = topic_categories

    result = controller.get_all_topic_categories()
    assert len(result) == 3
    assert result == topic_categories


def test_empty_all_topic_categories_with_success(controller, mock_service):
    topic_categories = []
    mock_service.get_all_topic_categories.return_value = topic_categories

    result = controller.get_all_topic_categories()
    assert len(result) == 0
    assert result == topic_categories