import pytest

from src.api.student.service import StudentService
from src.api.student.repository import StudentRepository
from src.api.student.exceptions import CsvNotLoaded
from src.api.auth.hasher import ShaHasher


class TestStudentService:

    @pytest.fixture
    def csv(self):
        with open('tests/api/student/test_data.csv', 'rb') as file:
            content = file.read()
        return content.decode("utf-8")

    @pytest.mark.unit
    def tests_create_3_students_from_string(self, mocker, csv):
        repo = StudentRepository(None)
        mocker.patch.object(repo, "add_students", return_value=None)
        service = StudentService(repo)

        students = service.create_students_from_string(csv,ShaHasher())

        assert len(students) == 3

    
    @pytest.mark.unit
    def tests_create_students_from_string(self, mocker, csv):
        repo = StudentRepository(None)
        mocker.patch.object(repo, "add_students", return_value=None)
        hash = ShaHasher()
        service = StudentService(repo)
        password = hash.hash("123456789")


        students = service.create_students_from_string(csv,hash)

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

        with pytest.raises(CsvNotLoaded):
            _ = service.create_students_from_string("bla,bla,bla",hash)
