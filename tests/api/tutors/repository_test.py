import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.tutors.model import Period
from src.api.users.repository import UserRepository
from src.api.users.model import User, Role
from src.api.topic.repository import TopicRepository
from src.api.topic.models import Topic, Category
from src.api.tutors.exceptions import TutorNotFound, TutorPeriodNotFound
from src.api.topic.exceptions import TopicNotFound


class TestTutorRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="module")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_topic_tutor_period_with_tutor_not_found(self, tables):
        topics = [Topic(name="topic 1", category="category 1")]
        capacities = [2]

        t_repository = TutorRepository(self.Session)
        with pytest.raises(TutorNotFound):
            t_repository.add_topic_tutor_period("tutor2@com", topics, capacities)

    @pytest.mark.integration
    def test_add_tutors_with_success(self, tables):
        tutor = User(
            id=12345,
            name="Juan",
            last_name="Perez",
            email="tutor1@com",
            password="password",
            role=Role.TUTOR,
        )
        u_repository = UserRepository(self.Session)
        response = u_repository.add_tutors([tutor])
        assert len(response) == 1

    @pytest.mark.integration
    def test_add_topic_tutor_period_with_tutor_period_not_found(self, tables):
        topic_repository = TopicRepository(self.Session)
        topic_repository.add_categories([Category(name="category 1")])
        topics = topic_repository.add_topics(
            [Topic(name="topic 1", category="category 1")]
        )
        topics = [Topic(name="topic 1", category="category 1")]
        capacities = [2]

        t_repository = TutorRepository(self.Session)
        with pytest.raises(TutorPeriodNotFound):
            t_repository.add_topic_tutor_period("tutor1@com", topics, capacities)

    @pytest.mark.integration
    def test_add_topic_tutor_period_with_success(self, tables):
        t_repository = TutorRepository(self.Session)
        t_repository.add_period(Period(id="1C2024"))
        t_repository.add_tutor_period(12345, "1C2024")

        topics = [Topic(name="topic 1", category="category 1")]
        capacities = [2]
        response = t_repository.add_topic_tutor_period("tutor1@com", topics, capacities)
        assert len(response) == 1
        assert response[0].topic_id == 1
        assert response[0].tutor_period_id == 1
        assert response[0].capacity == 2

    @pytest.mark.integration
    def test_delete_tutors_with_success(self, tables):
        u_repository = UserRepository(self.Session)
        t_repository = TutorRepository(self.Session)

        response = t_repository.get_topic_tutor_period(1, 1)
        assert response is not None

        u_repository.delete_tutors()
        t_repository = TutorRepository(self.Session)
        response = t_repository.get_tutors()
        assert len(response) == 0

        with pytest.raises(TopicNotFound):
            t_repository.get_topic_tutor_period(1, 1)
