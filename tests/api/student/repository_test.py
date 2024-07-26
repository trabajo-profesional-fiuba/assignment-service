import pytest

from src.api.student.repository import StudentRepository
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserResponse

from src.config.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session


class TestStudentRepository:

    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)

    @pytest.fixture(scope="session")
    def tables(self):
        # Create all tables
        create_tables()
        yield
        # Drop all tables
        drop_tables()

    @pytest.mark.integration
    def test_add_students(self, tables):
        student1 = UserResponse(id=12345, name="Juan", last_name="Perez",
                               email="email@fi,uba.ar", password="password")
        student2 = UserResponse(id=54321, name="Pedro", last_name="Pipo",
                               email="email2@fi,uba.ar", password="password1")
        students = [student1, student2]


        u_repository = UserRepository(self.Session)
        u_repository.add_students(students)
        repository = StudentRepository(self.Session)
        response = repository.get_students()
        assert len(response) == 2

    @pytest.mark.integration
    def test_no_student_returns_empty_list(self, tables):
        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([1, 2])

        assert response == []

    @pytest.mark.integration
    def test_get_student_by_id(self, tables):
        student1 = UserResponse(id=12345, name="Juan", last_name="Perez",
                               email="email@fi,uba.ar", password="password")
        student2 = UserResponse(id=54321, name="Pedro", last_name="Pipo",
                               email="email2@fi,uba.ar", password="password1")
        students = [student1, student2]

        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([12345, 54321])

        assert all(e in response for e in students)

    @pytest.mark.integration
    def test_get_student_by_id_with_extra_one(self, tables):
        student1 = UserResponse(id=12345, name="Juan", last_name="Perez",
                               email="email@fi,uba.ar", password="password")
        student2 = UserResponse(id=54321, name="Pedro", last_name="Pipo",
                               email="email2@fi,uba.ar", password="password1")
        student3 = UserResponse(id=11111, name="Pepe", last_name="Bla",
                               email="email3@fi,uba.ar", password="password1")
        students = [student3]
        students_expected = [student1, student3]


        u_repository = UserRepository(self.Session)
        _ = u_repository.add_students(students)
        repository = StudentRepository(self.Session)
        response = repository.get_students_by_ids([12345, 11111])

        assert all(e in response for e in students_expected)
