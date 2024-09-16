import pytest

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.tutors.models import Period, TutorPeriod
from src.api.users.repository import UserRepository
from src.api.users.models import User, Role
from src.api.topics.repository import TopicRepository
from src.api.topics.models import Topic, Category
from src.api.tutors.exceptions import TutorNotFound, TutorPeriodNotFound
from tests.integration.api.helper import ApiHelper
from src.api.periods.repository import PeriodRepository


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
        topics = [Topic(name="topic 1", category_id=2)]
        capacities = [2]

        t_repository = TutorRepository(self.Session)
        with pytest.raises(TutorNotFound):
            t_repository.add_topic_tutor_period(
                "1C2024", "tutor2@com", topics, capacities
            )

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
    def test_get_tutor_by_id(self, tables):
        t_repository = TutorRepository(self.Session)
        response = t_repository.get_tutor_by_tutor_id(12345)
        assert response.id == 12345
        assert response.tutor_periods == []

    @pytest.mark.integration
    def test_add_topic_tutor_period_with_tutor_period_not_found(self, tables):
        topic_repository = TopicRepository(self.Session)
        topic_repository.add_categories([Category(name="category 1")])
        topic = topic_repository.add_topic_with_category(
            Topic(name="topic 1"), "category 1"
        )
        capacities = [2]

        t_repository = TutorRepository(self.Session)
        with pytest.raises(TutorPeriodNotFound):
            t_repository.add_topic_tutor_period(
                "1C2024", "tutor1@com", [topic], capacities
            )

    @pytest.mark.integration
    def test_add_topic_tutor_period_with_success(self, tables):
        p_repository = PeriodRepository(self.Session)
        p_repository.add_period(Period(id="1C2024"))

        t_repository = TutorRepository(self.Session)
        t_repository.add_tutor_period(12345, "1C2024")

        topics = [Topic(name="topic 1", category_id=2)]
        capacities = [2]
        response = t_repository.add_topic_tutor_period(
            "1C2024", "tutor1@com", topics, capacities
        )
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
        # only the default admin
        assert len(response) == 1

        with pytest.raises(TutorPeriodNotFound):
            t_repository.get_topic_tutor_period(1, 1)

    @pytest.mark.integration
    def test_delete_tutors_by_also_deletes_tutor_periods(self, tables):
        t_repository = TutorRepository(self.Session)
        tutor = User(
            id=11111,
            name="Juan",
            last_name="Perez",
            email="tutor1@com",
            password="password",
            role=Role.TUTOR,
        )
        u_repository = UserRepository(self.Session)
        _ = u_repository.add_tutors([tutor])

        p_repository = PeriodRepository(self.Session)
        p_repository.add_period(Period(id="1C2025"))

        t_repository.add_tutor_period(11111, "1C2024")
        t_repository.add_tutor_period(11111, "1C2025")

        with self.Session() as sess:
            tutor_periods = sess.query(TutorPeriod).all()
            assert len(tutor_periods) == 2

        _ = t_repository.delete_tutor_by_id(11111)

        with self.Session() as sess:
            tutor_periods = sess.query(TutorPeriod).all()
            assert len(tutor_periods) == 0

    @pytest.mark.integration
    def test_get_full_tutor_by_id(self, tables):
        helper = ApiHelper()
        helper.create_tutor("Carlos", "Fontela", "100", "cfontela@fi.uba.ar")
        u_repository = UserRepository(self.Session)

        tutor = u_repository.get_tutor_by_id(100)

        assert tutor.id == 100
        assert tutor.name == "Carlos"
        assert tutor.last_name == "Fontela"
        assert tutor.email == "cfontela@fi.uba.ar"
