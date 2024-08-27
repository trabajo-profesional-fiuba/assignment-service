from src.api.auth.jwt import JwtResolver
from src.config.database.database import create_tables, drop_tables, engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.tutors.models import Period, TutorPeriod

from src.api.users.repository import UserRepository
from src.api.users.models import User, Role

from src.api.auth.hasher import ShaHasher

class ApiHelper:
    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)
    hasher = ShaHasher()

    def __init__(self):
        self._user_repository = UserRepository(self.Session)
        self._tutor_repository = TutorRepository(self.Session)

    def create_period(self, period: str):
        self._tutor_repository.add_period(Period(id=period))
    
    def create_tutor(self, name, last_name, id, email):
        tutor = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.TUTOR,
        )

        self._user_repository.add_tutors([tutor])

    def create_student(self, name, last_name, id, email):
        student = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.STUDENT,
        )

        self._user_repository.add_students([student])

    def create_tutor_period(self, tutor_id, period_id, capacity = 1):
        period = TutorPeriod(
            tutor_id = tutor_id,
            period_id = period_id,
            capacity = capacity
        )
        self._tutor_repository.add_tutor_periods([period])

    def get_tutor_by_tutor_id(self, tutor_id):
        return self._tutor_repository.get_tutor_by_tutor_id(tutor_id)
    
    def create_admin_token(self):
        sub = {
            "id": 1,
            "name": "admin",
            "last_name": "admin",
            "role": "ADMIN",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "admin")
        return token