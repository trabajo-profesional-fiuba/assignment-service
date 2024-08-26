import src.exceptions as e


class Tutor:
    """
    This class represents a Tutor during a specific Period. 
    Although a tutor may be active in multiple periods, this abstraction considers each tutor within the context of a single period.
    Thus, each period has its tutors as a subset of objects that exist only within that period. 
    """

    def __init__(self, id: int,
                 email: str,
                 name: str,
                 last_name: str,
                 capacity: int = 0,
                 groups=[],
                 topics=[]
                 ) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._last_name = last_name
        self._capacity = capacity
        self._groups = groups
        self._topics = topics

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

    @property
    def capacity(self) -> int:
        return self._capacity
