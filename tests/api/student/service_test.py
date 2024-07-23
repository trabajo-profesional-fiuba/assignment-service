import pytest

from src.api.student.service import StudentService
from src.api.student.repository import StudentRepository
from src.api.student.exceptions import InvalidStudentCsv, StudentNotFound
from src.api.student.schemas import StudentBase

from src.api.auth.hasher import ShaHasher


class TestStudentService:

    @pytest.fixture
    def csv(self):
        with open("tests/api/student/test_data.csv", "rb") as file:
            content = file.read()
        return content.decode("utf-8")

    @pytest.mark.unit
    def tests_create_3_students_from_string(self, mocker, csv):
        repo = StudentRepository(None)
        mocker.patch.object(repo, "add_students", return_value=None)
        service = StudentService(repo)

        students = service.create_students_from_string(csv, ShaHasher())

        assert len(students) == 3

    @pytest.mark.unit
    def tests_create_students_from_string(self, mocker, csv):
        repo = StudentRepository(None)
        mocker.patch.object(repo, "add_students", return_value=None)
        hash = ShaHasher()
        service = StudentService(repo)
        password = hash.hash("123456789")

        students = service.create_students_from_string(csv, hash)

        assert students[0].name == "nombre"
        assert students[0].last_name == "apellido"
        assert students[0].email == "mail@fi.uba.ar"
        assert students[0].password == password

    @pytest.mark.unit
    def tests_bad_csv_raise_exception(self, mocker):
        repo = StudentRepository(None)
        mocker.patch.object(repo, "add_students", return_value=None)
        hash = ShaHasher()
        service = StudentService(repo)

        with pytest.raises(InvalidStudentCsv):
            _ = service.create_students_from_string("bla,bla,bla", hash)

    @pytest.mark.unit
    def test_get_student_by_ids(self, mocker):
        student1 = StudentBase(uid=12345, name="Juan", last_name="Perez",
                               email="email@fi,uba.ar", password="password")
        student2 = StudentBase(uid=54321, name="Pedro", last_name="Pipo",
                               email="email2@fi,uba.ar", password="password1")
        student3 = StudentBase(uid=11111, name="Pepe", last_name="Bla",
                               email="email3@fi,uba.ar", password="password1")
        students = [student1, student2, student3]

        repo = StudentRepository(None)
        mocker.patch.object(repo, "get_students_by_ids", return_value=students)
        service = StudentService(repo)
        response = service.get_students_by_ids([12345, 54321, 11111])

        assert all(e in response for e in students)

    @pytest.mark.unit
    def tests_student_not_found_trying_to_get_students_by_ids(self, mocker):
        student1 = StudentBase(uid=12345, name="Juan", last_name="Perez",
                               email="email@fi,uba.ar", password="password")
        student2 = StudentBase(uid=54321, name="Pedro", last_name="Pipo",
                               email="email2@fi,uba.ar", password="password1")
        students = [student1, student2]
        repo = StudentRepository(None)
        mocker.patch.object(repo, "get_students_by_ids", return_value=students)
        service = StudentService(repo)

        with pytest.raises(StudentNotFound) as e:
            _ = service.get_students_by_ids([12345, 54321, 11111])
            assert str(e) == "11111, is not registered in the database" 