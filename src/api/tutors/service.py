import re

from src.api.exceptions import Duplicated, EntityNotFound
from src.api.users.models import User, Role
from src.api.auth.hasher import ShaHasher
from src.api.tutors.schemas import (
    PeriodRequest,
    PeriodResponse,
    TutorList,
    TutorPeriodResponse,
    TutorRequest,
    TutorResponse,
    PeriodList,
    TutorWithTopicsList,
)
from src.api.tutors.utils import TutorCsvFile
from src.api.tutors.exceptions import (
    InvalidPeriod,
    PeriodDuplicated,
    TutorDuplicated,
    TutorNotFound,
    TutorNotInserted,
    TutorPeriodNotInserted,
)
from src.api.tutors.models import Period, TutorPeriod
from src.api.users.repository import UserRepository


class TutorService:

    def __init__(self, repository) -> None:
        self._repository = repository

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

    def _get_existing_ids(self, tutors_ids):
        tutors = self._repository.get_tutors()
        existing_tutors_id = []
        for tutor in tutors:
            if tutor.id in tutors_ids:
                existing_tutors_id.append(tutor.id)
        return existing_tutors_id

    def create_tutors_from_csv(
        self, csv: str, period: str, hasher: ShaHasher, user_repository
    ):
        try:
            """
            With a csv file as string, it
            make new tutors and override the existing ones
            """
            csv_file = TutorCsvFile(csv=csv)
            tutors_ids = csv_file.get_tutors_id()
            tutors_dtos = csv_file.get_tutors()
            existing_tutors_id = self._get_existing_ids(tutors_ids)

            remaining_ids = list(
                filter(lambda x: x not in existing_tutors_id, tutors_ids)
            )

            tutor_periods = []
            tutors = []
            for id in remaining_ids:
                tutor_dto = tutors_dtos[id]
                tutor = User(
                    id=int(tutor_dto.id),
                    name=tutor_dto.name,
                    last_name=tutor_dto.last_name,
                    email=tutor_dto.email,
                    password=hasher.hash(str(tutor_dto.id)),
                    role=Role.TUTOR,
                )
                tutors.append(tutor)

            for id in tutors_ids:
                tutor_dto = tutors_dtos[id]
                tutor_periods.append(
                    TutorPeriod(
                        period_id=period,
                        tutor_id=tutor_dto.id,
                        capacity=tutor_dto.capacity,
                    )
                )

            user_repository.add_tutors(tutors)

            # Clean if the tutor already contains a period asociated
            if len(existing_tutors_id) > 0:
                self._repository.remove_tutor_periods_by_tutor_ids(
                    period, existing_tutors_id
                )

            # Add new periods
            self._repository.add_tutor_periods(tutor_periods)
            tutors = self._repository.get_tutors_by_period_id(period)

            return tutors
        except TutorDuplicated as e:
            raise Duplicated(str(e))
        except (TutorNotFound, TutorPeriodNotInserted) as e:
            EntityNotFound(str(e))

    def add_tutor(self, tutor: TutorRequest, hasher: ShaHasher, userRepository: UserRepository):
        try:
            return userRepository.add_user(
                User(
                        id = tutor.id,
                        name = tutor.name,
                        last_name = tutor.last_name,
                        email = tutor.email,
                        password=hasher.hash(str(tutor.id)),
                        role=Role.TUTOR,
                )
            )
        except Duplicated:
            raise Duplicated("Duplicated tutor")
        except Exception:
            raise TutorNotInserted("Could not insert a tutor in the database")

    def _validate_period(self, period_id):
        """Validates that the period id
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
                return self._repository.add_period(period_db)
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
                return tutor
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
            return self._repository.get_tutor_by_tutor_id(tutor_id)
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def delete_tutor(self, tutor_id):
        """
        Deletes a tutor by id
        """
        try:
            return TutorResponse.model_validate(
                self._repository.delete_tutor_by_id(tutor_id)
            )
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def get_tutors_by_period_id(self, period_id):
        """From a period id, it retrieves all the tutors with their topics"""
        try:
            valid = self._validate_period(period_id)
            if valid:
                tutors = self._repository.get_tutors_by_period_id(period_id)
                return tutors
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def get_tutor_period_by_tutor_email(self, period, tutor_email):
        """
        Looks up for a tutor based on its email
        """
        try:
            return TutorPeriodResponse.model_validate(
                self._repository.get_tutor_period_by_tutor_email(period, tutor_email)
            )
        except TutorNotFound as e:
            raise EntityNotFound(message=str(e))

    def get_tutor_periods_by_period_id(self, period_id):
        try:
            return self._repository.get_tutor_periods_by_periods_id(period_id)
        except TutorNotFound as e:
            raise EntityNotFound(message=str(e))