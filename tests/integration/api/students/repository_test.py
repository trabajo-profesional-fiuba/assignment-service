import pytest

from src.api.students.repository import StudentRepository
from src.api.users.repository import UserRepository
from src.api.users.models import User, Role

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
            email="email@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student2 = User(
            id=54321,
            name="Pedro",
            last_name="Pipo",
            email="email2@fi.uba.ar",
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
            email="email3@fi.uba.ar",
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
    def test_get_all_students(self, tables):
        student4 = User(
            id=44444,
            name="Pepe",
            last_name="Bla",
            email="44444@fi,uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        students = [student4]

        u_repository = UserRepository(self.Session)
        _ = u_repository.add_students(students)
        repository = StudentRepository(self.Session)
        response = repository.get_students()

        assert len(response) == 4

    @pytest.mark.integration
    def test_upsert_students(self, tables):
        student1 = User(
            id=121212,
            name="Juan",
            last_name="Perez",
            email="121212@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student2 = User(
            id=131313,
            name="Pedro",
            last_name="Pipo",
            email="131313@fi.uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        students = [student1, student2]

        u_repository = UserRepository(self.Session)
        u_repository.add_students(students)

        student3 = User(
            id=121212,
            name="Alejo",
            last_name="Buenisimo",
            email="121212@fi.uba.ar",
            password="password",
            role=Role.STUDENT,
        )
        student4 = User(
            id=141414,
            name="Pedro",
            last_name="Pipo",
            email="141414@fi.uba.ar",
            password="password1",
            role=Role.STUDENT,
        )
        students = u_repository.upsert_students([student3, student4])
        repository = StudentRepository(self.Session)
        response = repository.get_students()

        student_changed = list(filter(lambda x: x.id == 121212, response))[0]

        assert len(response) == 7
        assert student_changed.name == "Alejo"
        assert student_changed.last_name == "Buenisimo"
