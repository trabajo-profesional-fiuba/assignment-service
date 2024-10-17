from src.api.users.models import User


class Student:

    def __init__(
        self,
        id: int,
        email: str,
        name: str,
        last_name: str,
    ) -> None:
        self._id = id
        self._name = name
        self._last_name = last_name
        self._email = email

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email


class StudentMapper:

    def map_models_to_students(self, users: list[User]) -> list[Student]:
        students = [
            Student(
                id=user.id, email=user.email, name=user.name, last_name=user.last_name
            )
            for user in users
        ]

        return students
