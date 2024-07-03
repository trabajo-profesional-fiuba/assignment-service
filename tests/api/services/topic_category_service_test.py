import pytest
from api.models import TopicCategoryItem
from api.services.topic_category_service import TopicCategoryService


@pytest.fixture
def service():
    return TopicCategoryService()


@pytest.mark.integration
def test_add_topic_category_success(service):
    new_item = TopicCategoryItem(
        name="data science",
    )

    assert service.add_topic_category(new_item) == new_item
