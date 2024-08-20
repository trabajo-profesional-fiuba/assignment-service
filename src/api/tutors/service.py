import re

from src.api.exceptions import Duplicated, EntityNotFound
from src.api.users.modelss import User, Role
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
from src.api.tutors.models import Period


class TutorService:

    def __init__(self, user_repository) -> None:
        self._user_repository = user_repository

    def _get_csv_content(self, csv: str):
        """
            Parse the row information from the
            csv of tutors
        """
        csv_file = TutorCsvFile(csv=csv)
        return csv_file.get_info_as_rows()

    def _make_tutors(self, rows, hasher: ShaHasher):
        """
            Instanciates new Users as tutors
            based on the rows with the necessary
            information.
            It also uses the hasher to create a hashed password.
        """
        tutors = []
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
        return tutors

    # FIXME: This needs to be fixed so we create a new tutor period and if the tutor does not
    # exists we create it.
    def create_tutors_from_string(self, csv: str, hasher: ShaHasher):
        try:
            """
                With a csv file as string, it 
                make new tutors and override the existing ones
            """
            csv_rows = self._get_csv_content(csv)
            tutors = self._make_tutors(csv_rows, hasher)
            self._repository.delete_tutors()
            return TutorList.model_validate(self._repository.add_tutors(tutors))
        except TutorDuplicated as e:
            raise Duplicated(str(e))
        except TutorNotFound as e:
            EntityNotFound(str(e))

    def _validate_period(self, period_id):
        """ Validates that the period id
            follows the expected pattern
            ^[1|2]C20[0-9]{2}$
            
            Matches cases where 1|2C20xx where xx are numbers from 0-9
        """
        regex = re.compile("^[1|2]C20[0-9]{2}$")
        if regex.search(period_id) is not None:
            return True
        else:
            return False

    def add_period(self, period: PeriodRequest):
        """
            Creates a nw global period
        """
        try:
            valid = self._validate_period(period.id)
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
        """
            Assigns an existing period to a tutor.
        """
        try:
            if self._repository.is_tutor(tutor_id):
                tutor = self._repository.add_tutor_period(tutor_id, period_id)
                return TutorResponse.model_validate(tutor)
            else:
                raise EntityNotFound(f"{tutor_id} was not found as TUTOR")
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def get_all_periods(self, order):
        """
            Returns the list of periods
        """
        return PeriodList.model_validate(self._repository.get_all_periods(order))

    def get_periods_by_tutor_id(self, tutor_id):
        """
            Returns the list of periods
            of a tutor based on its id
        """
        try:
            return TutorResponse.model_validate(
                self._repository.get_all_periods_by_id(tutor_id)
            )
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def get_tutor_period_by_email(self, period, tutor_email):
        """
            Looks up for a tutor based on its email
        """
        return TutorPeriodResponse.model_validate(
            self._repository.get_tutor_period_by_email(period, tutor_email)
        )
