import pytest
from unittest.mock import create_autospec
from src.api.topic.service import TopicService
from src.api.topic.repository import TopicRepository
from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
)


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
    result_topics = result[0]
    assert len(result_topics) == 1
    assert result_topics[0].name == "topic 1"
    assert result_topics[0].category == "category 1"


@pytest.mark.integration
def test_add_duplicated_topic_success(service):
    new_topic = TopicRequest(name="topic 1", category="category 1")
    topics = [new_topic]

    result = service._add_topic("topic 1", "category 1", topics)
    result_topics = result[0]
    assert len(result_topics) == 1


@pytest.mark.integration
def test_add_diff_topics_with_same_category_topic_success(service):
    new_topic = TopicRequest(name="topic 1", category="category 1")
    topics = [new_topic]

    result = service._add_topic("topic 2", "category 1", topics)
    result_topics = result[0]
    assert len(result_topics) == 2


@pytest.mark.integration
def test_get_topics_by_tutor_success(service):
    topic_by_tutor = {}
    new_topic = TopicRequest(name="topic 1", category="category 1")

    result = service._add_topic_by_tutor("tutor1@com", topic_by_tutor, new_topic)
    assert len(result) == 1
    assert len(result["tutor1@com"]) == 1
    assert result["tutor1@com"][0].name == "topic 1"
    assert result["tutor1@com"][0].category == "category 1"


@pytest.mark.integration
def test_get_topics_by_tutor_with_many_topics_success(service):
    existent_topic = TopicRequest(name="topic 1", category="category 1")
    topic_by_tutor = {"tutor1@com": [existent_topic]}
    new_topic = TopicRequest(name="topic 2", category="category 1")

    result = service._add_topic_by_tutor("tutor1@com", topic_by_tutor, new_topic)
    assert len(result) == 1
    assert len(result["tutor1@com"]) == 2
    assert result["tutor1@com"][1].name == "topic 2"
    assert result["tutor1@com"][1].category == "category 1"
