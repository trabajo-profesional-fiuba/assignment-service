import pytest
from unittest.mock import create_autospec
from datetime import datetime

from src.api.form.service import FormService
from src.api.form.repository import FormRepository
from src.api.form.schemas import GroupAnswerResponse


@pytest.fixture
def mock_repository(mocker):
    return create_autospec(FormRepository)


@pytest.fixture
def service(mock_repository):
    return FormService(mock_repository)


@pytest.mark.integration
def test_filter_uids_without_none_uids(service):
    uids = [111111, 111112, 111113, 111114]
    result = service._filter_uids(uids)

    assert len(result) == 4
    assert result == uids


@pytest.mark.integration
def test_filter_uids_with_some_none_uids(service):
    uids = [111111, 111112, None, None]
    result = service._filter_uids(uids)

    assert len(result) == 2
    assert result == [111111, 111112]


@pytest.mark.integration
def test_filter_uids_with_all_none_uids(service):
    uids = [None, None, None, None]
    result = service._filter_uids(uids)

    assert len(result) == 0
    assert result == []


@pytest.mark.integration
def test_get_answers_empty(service, mock_repository):
    mock_repository.get_answers.return_value = []
    expected_result = []

    result = service.get_answers()
    assert result == []


@pytest.mark.integration
def test_get_answers_single_group(service, mock_repository):
    answer_id_1 = datetime(2024, 8, 1)
    mock_repository.get_answers.return_value = [
        GroupAnswerResponse(
            answer_id=answer_id_1,
            email="student1@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        GroupAnswerResponse(
            answer_id=answer_id_1,
            email="student2@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
    ]
    expected_result = [
        {
            "answer_id": answer_id_1,
            "students": ["student1@example.com", "student2@example.com"],
            "topics": ["topic 1", "topic 2", "topic 3"],
        }
    ]

    result = service.get_answers()
    for res in result:
        res["topics"].sort()
    for exp in expected_result:
        exp["topics"].sort()
    assert result == expected_result


@pytest.mark.integration
def test_get_answers_multiple_groups(service, mock_repository):
    answer_id_1 = datetime(2024, 8, 1)
    answer_id_2 = datetime(2024, 8, 2)
    mock_repository.get_answers.return_value = [
        GroupAnswerResponse(
            answer_id=answer_id_1,
            email="student1@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        GroupAnswerResponse(
            answer_id=answer_id_1,
            email="student2@example.com",
            topic_1="topic 1",
            topic_2="topic 2",
            topic_3="topic 3",
        ),
        GroupAnswerResponse(
            answer_id=answer_id_2,
            email="student3@example.com",
            topic_1="topic 2",
            topic_2="topic 3",
            topic_3="topic 1",
        ),
    ]
    expected_result = [
        {
            "answer_id": answer_id_1,
            "students": ["student1@example.com", "student2@example.com"],
            "topics": ["topic 1", "topic 2", "topic 3"],
        },
        {
            "answer_id": answer_id_2,
            "students": ["student3@example.com"],
            "topics": ["topic 2", "topic 3", "topic 1"],
        },
    ]

    result = service.get_answers()
    for res in result:
        res["topics"].sort()
    for exp in expected_result:
        exp["topics"].sort()
    assert result == expected_result
