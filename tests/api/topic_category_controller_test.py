import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem
from api.controllers.topic_category_controller import TopicCategoryController
from api.services.topic_category_service import TopicCategoryService


@pytest.fixture
def mock_service(mocker):
    return create_autospec(TopicCategoryService)


@pytest.fixture
def controller(mock_service):
    return TopicCategoryController(mock_service)


@pytest.mark.integration
def test_add_topic_category_success(controller, mock_service):
    new_item = TopicCategoryItem(
        name="data science",
    )

    mock_service.add_topic_category.return_value = TopicCategoryItem(
        name="data science",
    )

    assert controller.add_topic_category(new_item) == {"name": "data science"}
