import re

from src.api.users.schemas import UserResponse
from src.api.auth.hasher import ShaHasher
from src.api.tutors.schemas import PeriodRequest
from src.api.tutors.utils import TutorCsvFile
from src.api.tutors.exceptions import InvalidPeriodId

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
    
    def _validate(self, id):
        # Regex pattern
        # ^[1|2]C20[0-9]{2}$
        # Matches cases where 1|2C20xx where xx are numbers from 0-9
        regex = re.compile('^[1|2]C20[0-9]{2}$') 
        if regex.search(id) != None:
            return True
        else:
            return False
        
    def add_period(self, period: PeriodRequest):
        valid = self._validate(period.id)
        if valid:
            return self._repository.add_period(period)
        else:
            raise InvalidPeriodId(message="Period id should follow patter nC20year, ie. 1C2024")

    def add_period_to_tutor(self, tutor_id, period_id):
        return self._repository.add_tutor_period(tutor_id, period_id)

    def get_all_periods(self, order):
        return self._repository.get_all_periods(order)

    def get_periods_by_id(self, tutor_id):    
        return self._repository.get_all_periods_by_id(tutor_id)
