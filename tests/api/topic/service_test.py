import pytest
from unittest.mock import create_autospec
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
)
from src.api.topic.exceptions import TopicAlreadyExist


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(TopicRepository)


@pytest.fixture
def service(mock_repository):
    return TopicService(mock_repository)


@pytest.mark.integration
def test_add_new_category_success(service):
    categories = []

    result = service._add_category("category 1", categories)
    assert len(result) == 1
    assert result[0].name == "category 1"


@pytest.mark.integration
def test_add_already_exist_category_success(service):
    categories = [CategoryRequest(name="category 1")]

    result = service._add_category("category 1", categories)
    assert len(result) == 1


@pytest.mark.integration
def test_add_new_topic_success(service):
    topics = []

    result = service._add_topic("topic 1", "category 1", topics)
    assert len(result) == 1
    assert result[0].name == "topic 1"
    assert result[0].category == "category 1"


@pytest.mark.integration
def test_add_already_exist_topic_success(service):
    topics = [TopicRequest(name="topic 1", category="category 1")]

    with pytest.raises(TopicAlreadyExist):
        service._add_topic("topic 1", "category 1", topics)
