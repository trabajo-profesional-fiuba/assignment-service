import pytest
from unittest.mock import create_autospec

from src.api.forms.service import FormService
from src.api.forms.repository import FormRepository
from src.api.topics.repository import TopicRepository
from src.api.topics.models import Topic


@pytest.fixture
def mock_form_repository(mocker):
    return create_autospec(FormRepository)


@pytest.fixture
def mock_topic():
    def _create_mock_topic(name, category_id):
        mock = create_autospec(Topic)
        mock.name = name
        mock.category_id = category_id
        return mock

    return _create_mock_topic


@pytest.fixture
def mock_topic_repository(mocker, mock_topic):
    repository = create_autospec(TopicRepository)

    mock_topic_1 = mock_topic(name="topic 1", category_id=2)
    mock_topic_2 = mock_topic(name="topic 2", category_id=3)
    mock_topic_3 = mock_topic(name="topic 3", category_id=4)

    # retrieve topics in expected order}
    repository.get_topic_by_id.side_effect = [mock_topic_1, mock_topic_2, mock_topic_3]

    return repository


@pytest.fixture
def service(mock_form_repository):
    return FormService(mock_form_repository)


@pytest.mark.integration
def test_filter_user_ids_without_none_user_ids(service):
    user_ids = [111111, 111112, 111113, 111114]
    result = list(filter(lambda x: x is not None, user_ids))

    assert len(result) == 4
    assert result == user_ids


@pytest.mark.integration
def test_filter_user_ids_with_some_none_user_ids(service):
    user_ids = [111111, 111112, None, None]
    result = list(filter(lambda x: x is not None, user_ids))

    assert len(result) == 2
    assert result == [111111, 111112]


@pytest.mark.integration
def test_filter_user_ids_with_all_none_user_ids(service):
    user_ids = [None, None, None, None]
    result = list(filter(lambda x: x is not None, user_ids))

    assert len(result) == 0
    assert result == []


@pytest.mark.integration
def test_get_answers_empty(service, mock_form_repository, mock_topic_repository):
    mock_form_repository.get_answers.return_value = []
    expected_result = []

    result = service.get_answers(mock_topic_repository)
    assert result == expected_result
