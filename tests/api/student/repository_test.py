import pytest

from src.api.student.repository import StudentRepository
from src.api.topic.models import Category, Topic
from src.api.topic.repository import TopicRepository
from src.api.tutors.model import Period
from src.api.tutors.repository import TutorRepository
from src.api.users.repository import UserRepository
from src.api.users.model import User, Role

from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session


@pytest.fixture(scope="module")
def tables():
    # Create all tables
    create_tables()
    yield
    # Drop all tables
    drop_tables()


class TestStudentRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.mark.integration
    def test_add_students(self, tables):
        student1 = User(
            id=12345,
            name="Juan",
            last_name="Perez",
            email="email@fi,uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student2 = User(
            id=54321,
            name="Pedro",
            last_name="Pipo",
            email="email2@fi,uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        students = [student1, student2]

        u_repository = UserRepository(self.Session)
        s_repository = StudentRepository(self.Session)
        u_repository.add_students(students)
        response = s_repository.get_students()
        assert len(response) == 2

    @pytest.mark.integration
    def test_no_student_returns_empty_list(self, tables):
        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([1, 2])

        assert response == []

    @pytest.mark.integration
    def test_get_student_by_id(self, tables):
        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([12345, 54321])

        assert len(response) == 2

    @pytest.mark.integration
    def test_get_student_by_id_with_extra_one(self, tables):
        student3 = User(
            id=11111,
            name="Pepe",
            last_name="Bla",
            email="email3@fi,uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        students = [student3]

        u_repository = UserRepository(self.Session)
        _ = u_repository.add_students(students)
        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([12345, 11111])

        assert len(response) == 2

    @pytest.mark.integration
    def test_add_new_group(self, tables):
        topic_repository = TopicRepository(self.Session)
        tutor_repository = TutorRepository(self.Session)
        repository = StudentRepository(self.Session)
        u_repository = UserRepository(self.Session)

        topic_repository.add_categories([Category(name="cat1")])
        topic_repository.add_topics([Topic(name="nombre", category="cat1")])
        tutor_repository.add_period(Period(id="1C2025"))
        tutor = User(
            id=5,
            name="Pedro",
            last_name="Pipo",
            email="tutor@fi,uba.ar",
            password="password1",
            role=Role.TUTOR,
        )
        student1 = User(
            id=1,
            name="Juan",
            last_name="Perez",
            email="1@fi,uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student2 = User(
            id=2,
            name="Pedro",
            last_name="Pipo",
            email="2@fi,uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        u_repository.add_tutors([tutor])
        u_repository.add_students([student1, student2])
        tutor_repository.add_tutor_period(5, "1C2025")

        uids = [1, 2]
        period_id = 1
        topic_id = 1

        group = repository.add_group(uids, period_id, topic_id)
        ids = [user.id for user in group.students]

        assert ids == uids
        assert group.tutor_period.id == period_id
        assert group.topic.id == topic_id
