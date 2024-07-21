import pytest
from unittest.mock import create_autospec
from src.api.form.service import FormService
from src.api.form.repository import FormRepository


@pytest.fixture
def mock_topic_repository(mocker):
    return create_autospec(FormRepository)


@pytest.fixture
def service(mock_topic_repository):
    return FormService(mock_topic_repository)


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
