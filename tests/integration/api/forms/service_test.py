import pytest
from unittest.mock import create_autospec
from datetime import datetime

from src.api.form.service import FormService
from src.api.form.repository import FormRepository
from src.api.form.schemas import UserAnswerResponse, GroupAnswerResponse
from src.api.topic.repository import TopicRepository
from src.api.topic.models import Topic


@pytest.fixture
def mock_form_repository(mocker):
    return create_autospec(FormRepository)


@pytest.fixture
def mock_topic():
    def _create_mock_topic(name, category):
        mock = create_autospec(Topic)
        mock.name = name
        mock.category = category
        return mock

    return _create_mock_topic


@pytest.fixture
def mock_topic_repository(mocker, mock_topic):
    repository = create_autospec(TopicRepository)

    mock_topic_1 = mock_topic(name="topic 1", category=2)
    mock_topic_2 = mock_topic(name="topic 2", category=3)
    mock_topic_3 = mock_topic(name="topic 3", category=4)

    # retrieve topics in expected order}
    repository.get_topic_by_id.side_effect = [mock_topic_1, mock_topic_2, mock_topic_3]

    return repository


@pytest.fixture
def service(mock_form_repository):
    return FormService(mock_form_repository)


@pytest.mark.integration
def test_filter_user_ids_without_none_user_ids(service):
    user_ids = [111111, 111112, 111113, 111114]
    result = service._filter_user_ids(user_ids)

    assert len(result) == 4
    assert result == user_ids


@pytest.mark.integration
def test_filter_user_ids_with_some_none_user_ids(service):
    user_ids = [111111, 111112, None, None]
    result = service._filter_user_ids(user_ids)

    assert len(result) == 2
    assert result == [111111, 111112]


@pytest.mark.integration
def test_filter_user_ids_with_all_none_user_ids(service):
    user_ids = [None, None, None, None]
    result = service._filter_user_ids(user_ids)

    assert len(result) == 0
    assert result == []


@pytest.mark.integration
def test_get_answers_empty(service, mock_form_repository, mock_topic_repository):
    mock_form_repository.get_answers.return_value = []
    expected_result = []

    result = service.get_answers(mock_topic_repository)
    assert result == expected_result


@pytest.mark.integration
def test_get_answers_single_group(service, mock_form_repository, mock_topic_repository):
    answer_id_1 = datetime(2024, 8, 1)
    mock_form_repository.get_answers.return_value = [
        UserAnswerResponse(
            answer_id=answer_id_1,
            email="student1@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        UserAnswerResponse(
            answer_id=answer_id_1,
            email="student2@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
    ]

    result = service.get_answers(mock_topic_repository)
    expected_result = [
        GroupAnswerResponse(
            answer_id=answer_id_1,
            students=["student1@example.com", "student2@example.com"],
            topics=["topic 1", "topic 2", "topic 3"],
        )
    ]
    for res in result:
        res.topics.sort()
    for exp in expected_result:
        exp.topics.sort()

    assert result == expected_result


@pytest.mark.integration
def test_get_answers_multiple_groups(
    service, mock_form_repository, mock_topic_repository
):
    answer_id_1 = datetime(2024, 8, 1)
    answer_id_2 = datetime(2024, 8, 2)
    mock_form_repository.get_answers.return_value = [
        UserAnswerResponse(
            answer_id=answer_id_1,
            email="student1@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        UserAnswerResponse(
            answer_id=answer_id_1,
            email="student2@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        UserAnswerResponse(
            answer_id=answer_id_2,
            email="student3@example.com",
            topic_1="topic 2",
            topic_2="topic 3",
            topic_3="topic 1",
        ),
    ]

    result = service.get_answers(mock_topic_repository)
    expected_result = [
        GroupAnswerResponse(
            answer_id=answer_id_1,
            students=["student1@example.com", "student2@example.com"],
            topics=["topic 1", "topic 2", "topic 3"],
        ),
        GroupAnswerResponse(
            answer_id=answer_id_2,
            students=["student3@example.com"],
            topics=["topic 2", "topic 3", "topic 1"],
        ),
    ]

    for res in result:
        res.topics.sort()
    for exp in expected_result:
        exp.topics.sort()

    assert result == expected_result
