from src.api.tutors.utils import TutorCsvFile
from src.api.users.schemas import UserResponse
from src.api.auth.hasher import ShaHasher
from src.api.tutors.schemas import PeriodRequest


class TutorService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_tutors_from_string(self, csv: str, hasher: ShaHasher):
        tutors = []
        csv_file = TutorCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        for i in rows:
            name, last_name, id, email = i
            tutor = UserResponse(
                name=name,
                last_name=last_name,
                id=int(id),
                email=email,
                password=hasher.hash(str(id)),
            )
            tutors.append(tutor)
        self._repository.add_tutors(tutors)

        return tutors

    def add_period(self, period: PeriodRequest):
        return self._repository.add_period(period)

    def get_all_periods(self, tutor_id, order):

        if tutor_id is None:
            return self._repository.get_all_periods(order)
        else:
            return self._repository.get_all_periods_by_id(tutor_id, order)
