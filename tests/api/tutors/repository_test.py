import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.tutors.model import Period
from src.api.users.repository import UserRepository
from src.api.users.model import User, Role
from src.api.topic.repository import TopicRepository
from src.api.topic.models import Topic, Category


class TestTutorRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="function")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_topics_to_period(self, tables):
        tutor = User(
            id=12345,
            name="Juan",
            last_name="Perez",
            email="email@fi,uba.ar",
            password="password",
            role=Role.TUTOR,
        )
        u_repository = UserRepository(self.Session)
        u_repository.add_students([tutor])

        topic_repository = TopicRepository(self.Session)
        topic_repository.add_categories([Category(name="category 1")])
        # topic_repository.add_topics([Topic(name="topic 1", category="category 1")])

        t_repository = TutorRepository(self.Session)
        t_repository.add_period(Period(id="1C2024"))
        t_repository.add_tutor_period(12345, "1C2024")

        topics = [Topic(name="topic 1", category="category 1")]
        response = t_repository.add_topics_to_period("email@fi,uba.ar", topics)
        assert len(response.topics) == 1
        assert response.topics[0].name == "topic 1"
        assert response.topics[0].category == "category 1"
