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