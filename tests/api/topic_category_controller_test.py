import pytest
from api.models import TopicCategoryItem
from api.controllers.topic_category_controller import TopicCategoryController
from api.services.topic_category_service import TopicCategoryService


@pytest.fixture
def service():
    return TopicCategoryService()


@pytest.fixture
def controller(service):
    return TopicCategoryController(service)


@pytest.mark.integration
def test_add_topic_category_success(controller):
    new_item = TopicCategoryItem(
        name="data science",
    )

    assert controller.add_topic_category(new_item) == new_item
