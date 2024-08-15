import src.exceptions as e


# To evoid circular importing
# https://peps.python.org/pep-0484/#forward-references
import src.core.period as period


class Tutor:

    def __init__(self, id: int, email: str, name: str) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._periods = {}

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def periods(self) -> dict[str, "period.TutorPeriod"]:
        return self._periods

    def add_period(self, period: "period.TutorPeriod"):
        period_key = period.period_name()
        if period_key in self._periods:
            raise e.PeriodAlreadyExists(f"{period_key} already in tutor's periods")

        self._periods[period_key] = period
        period.add_parent(self)

    def get_period(self, period_name: str):
        if period_name not in self._periods:
            raise e.PeriodNotFound(f"{period_name} is not part of tutor's periods")

        return self._periods.get(period_name)

    def add_groups_to_period(self, groups, period_name):
        period = self.get_period(period_name)
        for g in groups:
            g.assign_tutor(self)
        period.add_groups(groups)