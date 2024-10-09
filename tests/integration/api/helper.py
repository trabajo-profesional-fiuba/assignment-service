from src.api.auth.jwt import JwtResolver
from src.api.forms.repository import FormRepository
from src.api.groups.repository import GroupRepository
from src.api.topics.models import Category, Topic
from src.api.topics.repository import TopicRepository
from src.config.database.database import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.api.tutors.repository import TutorRepository
from src.api.periods.models import Period
from src.api.tutors.models import TutorPeriod
from src.api.users.repository import UserRepository
from src.api.users.models import User, Role

from src.api.auth.hasher import ShaHasher
import datetime as dt

from src.core.student_form_answer import StudentFormAnswer
from src.api.students.models import StudentPeriod
from src.api.students.repository import StudentRepository
from src.api.periods.repository import PeriodRepository


class ApiHelper:
    SessionFactory = sessionmaker(bind=engine)
    Session = scoped_session(SessionFactory)
    hasher = ShaHasher()

    def __init__(self):
        self._user_repository = UserRepository(self.Session)
        self._tutor_repository = TutorRepository(self.Session)
        self._topic_repository = TopicRepository(self.Session)
        self._groups_repository = GroupRepository(self.Session)
        self._form_repository = FormRepository(self.Session)
        self._student_repository = StudentRepository(self.Session)
        self._period_repository = PeriodRepository(self.Session)

    def create_period(self, period: str):
        self._period_repository.add_period(Period(id=period))

    def create_tutor(self, name: str, last_name: str, id: str, email: str):
        tutor = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.TUTOR,
        )

        self._user_repository.add_tutors([tutor])

    def create_student(self, name: str, last_name: str, id: str, email: str):
        student = User(
            id=int(id),
            name=name,
            last_name=last_name,
            email=email,
            password=self.hasher.hash(str(id)),
            role=Role.STUDENT,
        )

        self._user_repository.add_students([student])

    def create_tutor_period(self, tutor_id: int, period_id: str, capacity: int = 1):
        period = TutorPeriod(tutor_id=tutor_id, period_id=period_id, capacity=capacity)
        periods = self._tutor_repository.add_tutor_periods([period])
        return periods[0]

    def get_tutor_by_tutor_id(self, tutor_id):
        return self._tutor_repository.get_tutor_by_tutor_id(tutor_id)

    def create_admin_token(self):
        sub = {
            "id": 1,
            "name": "admin",
            "last_name": "admin",
            "role": "admin",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "admin")
        return token

    def create_student_token(self, id: int = 2):
        sub = {
            "id": id,
            "name": "student",
            "last_name": "student",
            "role": "student",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "student")
        return token

    def create_tutor_token(self, id: int = 2):
        sub = {
            "id": id,
            "name": "tutor",
            "last_name": "tutor",
            "role": "tutor",
        }
        jwt = JwtResolver()
        token = jwt.create_token(sub, "tutor")
        return token

    def create_topic(self, name: str, category_id: int = 1):
        topic = Topic(name=name, category_id=category_id)
        return self._topic_repository.add_topic(topic)

    def create_category(self, name: str):
        category = Category(name=name)
        self._topic_repository.add_category(category)

    def create_default_topics(self, topic_names):
        for name in topic_names:
            topic = Topic(name=name, category_id=1)
            self._topic_repository.add_topic(topic)

    def add_tutor_to_topic(
        self, period_id: str, tutor_email: str, topics: list[str], capacities: list[int]
    ):
        topics_db = [Topic(name=t, category_id=1) for t in topics]

        self._tutor_repository.add_topic_tutor_period(
            period_id, tutor_email, topics_db, capacities
        )

    def get_groups(self, period_id):
        return self._groups_repository.get_groups(period=period_id)

    def register_answer(self, ids, topics):
        today = dt.datetime.today().isoformat()
        all_topics = self._topic_repository.get_topics()
        all_topics_dict = dict()
        for topic in all_topics:
            all_topics_dict[topic.name] = topic.id

        answers = []
        for id in ids:
            answer = StudentFormAnswer(
                id=id,
                answer_id=today,
                topics=topics,
            )
            answers.append(answer)
        self._form_repository.add_answers(answers, topics, ids)

    def create_student_period(self, student_id: int, period_id: str):
        period = StudentPeriod(period_id=period_id, student_id=student_id)
        self._student_repository.add_student_period(period)

    def create_basic_group(
        self, ids: list[int], topics: list[int], period_id: str = None
    ):
        return self._groups_repository.add_group(
            ids=ids, preferred_topics=topics, period_id=period_id
        )

    def create_group(
        self,
        ids: list[int],
        tutor_period_id: int,
        topic_id,
        period_id: str = None,
    ):
        return self._groups_repository.add_group(
            ids=ids,
            tutor_period_id=tutor_period_id,
            period_id=period_id,
            topic_id=topic_id,
        )
    
    def assign_reviewer(self, reviewer_id:int, group_id:int):
        attributes = {
            'reviewer_id':reviewer_id
        }
        self._groups_repository.update(group_id, attributes=attributes)
