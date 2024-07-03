import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem
from api.services.topic_category_service import TopicCategoryService
from api.repositories.topic_category_repository import TopicCategoryRepository
from api.exceptions import TopicCategoryDuplicated


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicCategoryRepository)


@pytest.fixture
def service(mock_repository):
    return TopicCategoryService(mock_repository)


@pytest.mark.integration
def test_add_topic_category_success(service, mock_repository):
    topic_category = TopicCategoryItem(
        name="data science",
    )

    mock_repository.get_topic_category_by_name.return_value = None
    mock_repository.add_topic_category.return_value = {"id": 1, "name": "data science"}

    assert service.add_topic_category(topic_category) == {
        "id": 1,
        "name": "data science",
    }


@pytest.mark.integration
def test_add_topic_category_duplicated(service, mock_repository):
    topic_category = TopicCategoryItem(
        name="data science",
    )

    mock_repository.get_topic_category_by_name.return_value = {
        "id": 1,
        "name": "data science",
    }
    mock_repository.add_topic_category.side_effect = TopicCategoryDuplicated()

    with pytest.raises(TopicCategoryDuplicated):
        service.add_topic_category(topic_category)
