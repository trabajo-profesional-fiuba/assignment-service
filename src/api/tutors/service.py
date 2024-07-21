from src.api.tutors.utils import TutorCsvFile
from src.api.tutors.schemas import Tutor
from src.api.tutors.repository import TutorRepository
from src.api.auth.hasher import ShaHasher


class TutorService:

    def __init__(self, repository: TutorRepository) -> None:
        self._repository = repository

    def create_tutors_from_string(self, csv: str, hasher: ShaHasher):
        tutors = []
        csv_file = TutorCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        for i in rows:
            name, last_name, uid, email = i
            tutor = Tutor(
                name=name,
                last_name=last_name,
                dni=int(uid),
                email=email,
                password=hasher.hash(str(uid)),
            )
            tutors.append(tutor)

        print(tutors)
        self._repository.add_tutors(tutors)

        return tutors
