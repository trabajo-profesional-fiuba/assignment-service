import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem, TopicItem
from api.controllers.topic_controller import TopicController
from api.services.topic_service import TopicService
from api.exceptions import TopicCategoryDuplicated


@pytest.fixture
def mock_service(mocker):
    return create_autospec(TopicService)


@pytest.fixture
def controller(mock_service):
    return TopicController(mock_service)


@pytest.mark.integration
def test_add_topic_category_with_success(controller, mock_service):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_service.add_topic_category.return_value = topic_category
    assert controller.add_topic_category(topic_category) == {"name": "category 1"}


@pytest.mark.integration
def test_add_topic_category_duplicated(controller, mock_service):
    topic_category = TopicCategoryItem(
        name="category 1",
    )

    mock_service.add_topic_category.side_effect = TopicCategoryDuplicated()

    with pytest.raises(TopicCategoryDuplicated):
        controller.add_topic_category(topic_category)


@pytest.mark.integration
def test_add_topic_with_success(controller, mock_service):
    topic = TopicItem(name="topic 1", category="category 1")

    mock_service.add_topic.return_value = topic

    assert controller.add_topic(topic) == topic
