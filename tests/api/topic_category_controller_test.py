import pytest
from api.models import TopicCategoryItem
from api.controllers.topic_category_controller import TopicCategoryController

controller = TopicCategoryController()

@pytest.mark.integration
def test_add_topic_category_success():
    new_item = TopicCategoryItem(
        name="data science",
    )

    assert controller.add_topic_category(new_item) == new_item
