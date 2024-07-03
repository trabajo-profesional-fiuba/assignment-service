import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem
from api.services.topic_category_service import TopicCategoryService
from api.repositories.topic_category_repository import TopicCategoryRepository


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicCategoryRepository)


@pytest.fixture
def service(mock_repository):
    return TopicCategoryService(mock_repository)


@pytest.mark.integration
def test_add_topic_category_success(service, mock_repository):
    new_item = TopicCategoryItem(
        name="data science",
    )

    mock_repository.add_topic_category.return_value = {"id": 1, "name": "data science"}
    assert service.add_topic_category(new_item) == {"id": 1, "name": "data science"}
