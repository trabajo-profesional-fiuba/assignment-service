import re

from src.api.exceptions import Duplicated, EntityNotFound
from src.api.users.model import User, Role
from src.api.auth.hasher import ShaHasher
from src.api.tutors.schemas import (
    PeriodRequest,
    PeriodResponse,
    TutorList,
    TutorPeriodResponse,
    TutorResponse,
    PeriodList,
)
from src.api.tutors.utils import TutorCsvFile
from src.api.tutors.exceptions import (
    InvalidPeriod,
    PeriodDuplicated,
    TutorDuplicated,
    TutorNotFound,
)
from src.api.tutors.model import Period


class TutorService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_tutors_from_string(self, csv: str, hasher: ShaHasher):
        try:
            tutors = []
            csv_file = TutorCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            for i in rows:
                name, last_name, id, email = i
                tutor = User(
                    id=int(id),
                    name=name,
                    last_name=last_name,
                    email=email,
                    password=hasher.hash(str(id)),
                    role=Role.TUTOR,
                )
                tutors.append(tutor)
            tutors = TutorList.model_validate(self._repository.add_tutors(tutors))

            return tutors
        except TutorDuplicated as e:
            raise Duplicated(str(e))
        except TutorNotFound as e:
            EntityNotFound(str(e))

    def _validate(self, id):
        # Regex pattern
        # ^[1|2]C20[0-9]{2}$
        # Matches cases where 1|2C20xx where xx are numbers from 0-9
        regex = re.compile("^[1|2]C20[0-9]{2}$")
        if regex.search(id) is not None:
            return True
        else:
            return False

    def add_period(self, period: PeriodRequest):
        try:
            valid = self._validate(period.id)
            if valid:
                period_db = Period(id=period.id)
                return PeriodResponse.model_validate(
                    self._repository.add_period(period_db)
                )
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def add_period_to_tutor(self, tutor_id, period_id):
        try:
            if self._repository.is_tutor(tutor_id):
                tutor = self._repository.add_tutor_period(tutor_id, period_id)
                return TutorResponse.model_validate(tutor)
            else:
                raise EntityNotFound(f"{tutor_id} was not found as TUTOR")
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def get_all_periods(self, order):
        return PeriodList.model_validate(self._repository.get_all_periods(order))

    def get_periods_by_tutor_id(self, tutor_id):
        try:
            return TutorResponse.model_validate(
                self._repository.get_all_periods_by_id(tutor_id)
            )
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def get_tutor_period_by_email(self, period, tutor_email):
        return TutorPeriodResponse.model_validate(
            self._repository.get_tutor_period_by_email(period, tutor_email)
        )
