from src.api.auth.hasher import ShaHasher
from src.api.forms.repository import FormRepository
from src.api.groups.repository import GroupRepository
from src.api.students.schemas import PersonalInformation
from src.api.students.utils import StudentCsvFile
from src.api.students.exceptions import (
    StudentDuplicated,
    StudentNotFound,
    StudentNotInserted,
)

from src.api.users.models import User, Role
from src.api.users.repository import UserRepository
from src.api.users.schemas import UserList, UserResponse

from src.api.exceptions import Duplicated, EntityNotFound, EntityNotInserted, InvalidCsv
from src.api.students.repository import StudentRepository
from src.api.students.models import StudentPeriod


class StudentService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _get_csv_rows(self, csv: str):
        csv_file = StudentCsvFile(csv=csv)
        return csv_file.get_info_as_rows()

    def _get_students_and_periods(self, rows, hasher: ShaHasher, period: str):
        students = []
        periods = []
        for i in rows:
            name, last_name, student_id, email = i
            students.append(
                User(
                    name=name,
                    last_name=last_name,
                    id=int(student_id),
                    email=email,
                    password=hasher.hash(str(student_id)),
                    role=Role.STUDENT,
                )
            )
            periods.append(StudentPeriod(period_id=period, student_id=student_id))
        return students, periods

    def create_students_from_string(
        self, csv: str, hasher: ShaHasher, repository: UserRepository, period: str
    ):
        try:
            rows = self._get_csv_rows(csv)
            students, student_periods = self._get_students_and_periods(
                rows, hasher, period
            )
            students_saved = repository.upsert_students(students)
            self._repository.upsert_student_periods(student_periods)
            return UserList.model_validate(students_saved)
        except InvalidCsv as e:
            raise e
        except StudentDuplicated as e:
            raise Duplicated(str(e))
        except StudentNotInserted as e:
            raise EntityNotInserted(str(e))

    def get_students_by_ids(self, ids: list[int]):
        try:
            if len(list(set(ids))) != len(list(ids)):
                raise StudentDuplicated("Query params udis contain duplicates")

            if len(ids) > 0:
                students_db = self._repository.get_students_by_ids(ids)
            else:
                students_db = self._repository.get_students()

            students = UserList.model_validate(students_db)
            udis_from_db = [student.id for student in students]
            for id in ids:
                if id not in udis_from_db:
                    raise StudentNotFound(f"{id}, is not registered in the database")

            return students
        except StudentNotFound as e:
            raise EntityNotFound(str(e))
        except StudentDuplicated as e:
            raise Duplicated(str(e))

    def get_personal_info_by_id(
        self,
        id: int,
        form_repository: FormRepository,
        repository: UserRepository,
        group_repository: GroupRepository,
        student_repository: StudentRepository,
    ):

        form_answers = form_repository.get_answers_by_user_id(id)
        
        form_answered = len(form_answers) > 0

        groups_without_preferred_topics = (
            group_repository.get_groups_without_preferred_topics()
        )
        student_in_groups_without_preferred_topics = False

        for group in groups_without_preferred_topics:
            student_ids = [student.id for student in group.students]
            if id in student_ids:
                student_in_groups_without_preferred_topics = True

        personal_information = PersonalInformation(
            id=id,
            form_answered=form_answered,
            group_id=0,
            tutor="",
            topic="",
            teammates=[],
            period_id=student_repository.get_period_by_student_id(id).period_id,
        )

        if (not student_in_groups_without_preferred_topics) and (not form_answered):
            return personal_information

        student_info_db = self._repository.get_student_info(id)

        if student_info_db is None:
            return personal_information

        tutor = repository.get_tutor_by_id(student_info_db.tutor_id)

        teammates = self._repository.get_teammates(id, student_info_db.group_id)
        personal_information.group_id = student_info_db.group_id
        personal_information.tutor = f"{tutor.name} {tutor.last_name}"
        personal_information.topic = student_info_db.topic_name
        personal_information.teammates = list(map(lambda x: x.email, teammates))

        return personal_information

    def add_student(
        self, student: UserResponse, hasher: ShaHasher, userRepository: UserRepository
    ):
        try:
            return userRepository.add_user(
                User(
                    id=student.id,
                    name=student.name,
                    last_name=student.last_name,
                    email=student.email,
                    password=hasher.hash(str(student.id)),
                    role=Role.STUDENT,
                )
            )
        except Duplicated:
            raise Duplicated("Duplicated student")
        except Exception:
            raise StudentNotInserted("Could not insert a student in the database")
