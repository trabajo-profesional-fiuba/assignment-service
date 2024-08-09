import pytest
from unittest.mock import create_autospec

from src.api.tutors.service import TutorService
from src.api.tutors.repository import TutorRepository
from src.api.tutors.model import TutorPeriod
from src.api.topic.models import Topic


class TestTutorService:
    def mock_tutor_repository(self):
        return create_autospec(TutorRepository)

    def tutor_service(self, mock_tutor_repository):
        return TutorService(mock_tutor_repository)

    @pytest.mark.integration
    def test_add_topics_to_period_success(self):
        tutor_email = "email@fi.uba.ar"
        topics = [Topic(name="topic 1", category="category 1")]

        mock_tutor_repository = self.mock_tutor_repository()
        tutor_service = self.tutor_service(mock_tutor_repository)

        mock_tutor_repository.add_topics_to_period.return_value = "mocked_result"
        result = tutor_service.add_topics_to_period(tutor_email, topics)
        assert result == "mocked_result"
