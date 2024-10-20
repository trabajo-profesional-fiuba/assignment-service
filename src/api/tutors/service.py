import re

from src.api.exceptions import Duplicated, EntityNotFound
from src.api.groups.repository import GroupRepository
from src.api.users.models import User, Role
from src.api.auth.hasher import ShaHasher
from src.api.tutors.schemas import TutorPeriodResponse, TutorRequest, TutorResponse
from src.api.tutors.utils import TutorCsvFile
from src.api.periods.exceptions import InvalidPeriod, PeriodDuplicated
from src.api.tutors.exceptions import (
    TutorNotFound,
    TutorNotInserted,
    TutorPeriodNotInserted,
    TutorDuplicated,
)
from src.api.tutors.models import TutorPeriod
from src.api.users.repository import UserRepository
from src.core.group import AssignedGroup


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
        self, csv: str, period: str, hasher: ShaHasher, user_repository: UserRepository
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

    def add_tutor(
        self, tutor: TutorRequest, hasher: ShaHasher, userRepository: UserRepository
    ):
        try:
            new_tutor = User(
                id=tutor.id,
                name=tutor.name,
                last_name=tutor.last_name,
                email=tutor.email,
                password=hasher.hash(str(tutor.id)),
                role=Role.TUTOR,
            )

            tutor_period = TutorPeriod(
                period_id=tutor.period,
                tutor_id=tutor.id,
                capacity=tutor.capacity,
            )
            tutor_response = userRepository.add_user(new_tutor)
            self._repository.add_tutor_period_with_capacity(tutor_period)

            return tutor_response
        except PeriodDuplicated as e:
            raise Duplicated(str(e))
        except Duplicated:
            raise Duplicated("Duplicated tutor")
        except Exception as e:
            print(str(e))
            raise TutorNotInserted("Could not insert a tutor in the database")

    def _validate_period(self, period_id: str):
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

    def add_period_to_tutor(self, tutor_id: int, period_id: str):
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

    def get_periods_by_tutor_id(self, tutor_id: int):
        """
        Returns the list of periods
        of a tutor based on its id
        """
        try:
            return self._repository.get_tutor_by_tutor_id(tutor_id)
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def delete_tutor(self, tutor_id: int):
        """
        Deletes a tutor by id
        """
        try:
            return TutorResponse.model_validate(
                self._repository.delete_tutor_by_id(tutor_id)
            )
        except TutorNotFound as e:
            raise EntityNotFound(str(e))

    def get_tutors_by_period_id(self, period_id: str):
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

    def get_tutor_period_by_tutor_email(self, period: str, tutor_email: str):
        """
        Looks up for a tutor based on its email
        """
        try:
            return TutorPeriodResponse.model_validate(
                self._repository.get_tutor_period_by_tutor_email(period, tutor_email)
            )
        except TutorNotFound as e:
            raise EntityNotFound(message=str(e))

    def get_tutor_period_by_tutor_id(self, period: str, tutor_id: int) -> TutorPeriod:
        """
        Looks up for a tutor based on its email
        """
        try:
            return self._repository.get_tutor_period_by_tutor_id(period, tutor_id)
        except TutorNotFound as e:
            raise EntityNotFound(message=str(e))

    def get_tutor_periods_by_period_id(self, period_id: str) -> list[TutorPeriod]:
        try:
            return self._repository.get_tutor_periods_by_periods_id(period_id)
        except TutorNotFound as e:
            raise EntityNotFound(message=str(e))

    def get_groups_from_tutor_id(
        self, tutor_id: int, period_id: str, group_repository: GroupRepository
    ):
        period = self.get_tutor_period_by_tutor_id(period_id, tutor_id)
        groups = group_repository.get_groups_by_period_id(
            tutor_period_id=period.id, load_topic=True
        )
        return groups

    def get_groups_from_reviewer_id(
        self, reviewer_id: int, period_id: str, group_repository: GroupRepository
    ):
        try:
            groups = group_repository.get_groups_by_reviewer_id(
                reviewer_id=reviewer_id, period_id=period_id, load_topic=True
            )
            return groups
        except Exception as e:
            raise EntityNotFound(message=str(e))

    def notify_students(
        self, sender_id: int, group: AssignedGroup, email_sender: str, message: str
    ):
        try:
            sender = self._repository.get_tutor_by_tutor_id(sender_id)
            to = group.emails()

            if group.reviewer_id and sender.id == group.reviewer_id:
                tutor = self._repository.get_tutor_by_tutor_id(group.tutor_id())
                to.extend([tutor.email, sender.email])
                subject = "Tienes un nuevo mensaje de tu revisor"
            else:
                to.append(sender.email)
                subject = "Tienes un nuevo mensaje de tu tutor"

            body = f"Mensaje:\n\n{message}\n\nGracias"
            cc = "avillores@fi.uba.ar"
            response = email_sender.send_emails(
                to=to, subject=subject, body=body, cc=cc
            )

            return response
        except Exception as e:
            raise EntityNotFound(message=str(e))

    def get_tutors_with_dates(self, period_id: str):
        """From a period id, it retrieves all the tutors with their topics"""
        try:
            valid = self._validate_period(period_id)
            if valid:
                tutors = self._repository.get_tutors_by_period_id_with_dates(period_id)
                return tutors
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def get_evaluators_with_dates(self, period_id: str):
        """From a period id, it retrieves all the tutors with their topics"""
        try:
            valid = self._validate_period(period_id)
            if valid:
                evaluators = self._repository.get_evaluators_by_period_id_with_dates(period_id)
                return evaluators
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            raise Duplicated(str(e))