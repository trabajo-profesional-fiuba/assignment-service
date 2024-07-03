import pytest
from unittest.mock import create_autospec
from api.models import TopicCategoryItem
from api.services.topic_service import TopicService
from api.repositories.topic_repository import TopicRepository
from api.exceptions import TopicCategoryDuplicated


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_repository):
    return TopicService(mock_repository)


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
